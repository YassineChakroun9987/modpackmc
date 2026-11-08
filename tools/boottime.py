"""Report on the last server start, from server/logs/latest.log.

Usage:  python -I tools/boottime.py

Prints the NeoForge version, loaded mods, boot time, ERROR lines and any WARN lines
that aren't on the known-harmless list below.
"""
import re
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows console defaults to cp1252

LOG = Path(__file__).resolve().parent.parent / "server" / "logs" / "latest.log"
TS = re.compile(r"^\[(\d{2}\w{3}\d{4} \d{2}:\d{2}:\d{2}\.\d{3})\]")

# WARN lines we've already analysed and decided are harmless (see MODLIST.md notes).
KNOWN_HARMLESS = [
    r"VanillaPackResourcesBuilder/\]: Assets URL",               # always printed by NeoForge servers
    r"OFFLINE/INSECURE MODE|no attempt to authenticate|hackers to connect|\"online-mode\" to \"true\"",
    r"ModernFix/\]: (Dedicated server took|Initial datapack load took)",  # timing info
    r"modernfix\.perf_mod_warning",                               # "how to silence ModernFix nudges"
    r"mixin/\]: Reference map .* could not be read",               # NeoForge 1.21 runs Mojang names; refmaps unused
    r"mixin/\]: Static binding violation: PRIVATE @Overwrite method .* from mod modernfix",  # mixin widens visibility itself
    r"KubeJS/\]: Plugin .*BuiltinKubeJSClientPlugin does not load on server side",          # client part, expected
    r"KubeJS/\]: Plugin .* does not have required mod '\w+' loaded, skipping",              # optional integration
    r"mixin/\]: Redundant @Unique on injector method netherexp\$",                           # JNE dev-only notice
    r"Not all defined tags for registry .* are present in data pack: netherexp:",            # JNE empty tag defs
    r"ModConfigSpec/CORE\]: .*heatDistortionLavaMinDistance",                                # JNE config default quirk
    r"yungsapi/\]: WARNING: block .* added to BlockStateRandomizer exceeds max probabiltiy",  # YUNG's data quirk
    r"AttributeMap/\]: Ignoring unknown attribute 'forge:",       # old Forge attributes saved in structure mobs
    r"mixin/\]: Error loading class: com/simibubi/create/",       # Lootr's optional Create compat (gone once Create is in)
    r"spark/\]: Timed out waiting for world statistics",          # spark stats while the server is busy generating
    r"JarSelector/\]: Attempted to select a dependency jar for JarJar which was passed in as source",  # lib shipped twice; real file wins
    r"azurelib/IO\]: Correcting config value",                    # AzureLib fixes its own default
    r"Jupiter/\]: Notice: Jupiter cannot resolve",                # Jupiter info notice
    r"mixin/\]: Error loading class: org/jetbrains/annotations/",  # compile-time annotation, absent at runtime
    r"mixin/\]: (Error loading class: |@Mixin target .* was not found)",  # optional compat mixins for mods we don't run
    r"draconicevolution/\]: (Reactor detonation initiated|Calculating explosion ETA|\*\*Explosion Imminent)",  # DE startup log noise
    r"ReloadableServerRegistries/\]: Found loot table element validation problem",  # entries for missing items are skipped
]


# ERROR lines we've traced to a cause and judged harmless. They're still COUNTED and shown as "known",
# never hidden, and they don't fail a boot test. Every entry needs its reason.
KNOWN_ERRORS = [
    (r"BlockAttachedEntity/\]: Block-attached entity at invalid position",
     "a structure template hangs a painting/item frame where no wall survived; the game drops it "
     "(traced to philipsruins:ancient_dungeon on our seed; also seen from YUNG's on another seed)"),
    (r"Jupiter/\]: Failed to load config: \./config/",
     "Jupiter (Ice and Fire's config lib) reads its config before creating it; only on the very first boot"),
    (r"RuntimeDistCleaner/DISTXFORM\]: Attempted to load class net/minecraft/client/",
     "a mod's client-only mixin (FamiliarsLib ItemRenderer) is tried on the dedicated server and skipped; clients are unaffected"),
]


def ts(line):
    m = TS.match(line)
    return datetime.strptime(m.group(1), "%d%b%Y %H:%M:%S.%f") if m else None


def report(log=LOG):
    lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
    start = next(t for t in map(ts, lines) if t)
    done = next((l for l in lines if "]: Done (" in l), None)
    nf = next((re.search(r"--fml\.neoForgeVersion, ([\d.]+)", l) for l in lines if "fml.neoForgeVersion" in l), None)
    mods = [l.strip() for l in lines if l.startswith("\t\t") and not l.strip().startswith("Name Version")]
    all_errors = [l for l in lines if "/ERROR]" in l]
    known = [l for l in all_errors if any(re.search(p, l) for p, _ in KNOWN_ERRORS)]
    errors = [l for l in all_errors if l not in known]
    warns = [l for l in lines if "/WARN]" in l and not any(re.search(p, l) for p in KNOWN_HARMLESS)]

    print("NeoForge:  ", nf.group(1) if nf else "?")
    print(f"Mods ({len(mods)}):", ", ".join(mods))
    if done:
        world = re.search(r"Done \(([\d.]+s)", done).group(1)
        print(f"Boot time:  {(ts(done) - start).total_seconds():.1f}s total  (world load: {world})")
    else:
        print("Boot time:  server did not finish starting (no 'Done' line)")
    print(f"ERROR lines: {len(errors)}" + (f"   (+{len(known)} known & explained, see KNOWN_ERRORS)" if known else ""))
    for l in errors[:15]:
        print("   ", l[:240])
    for pattern, reason in KNOWN_ERRORS:
        n = sum(1 for l in known if re.search(pattern, l))
        if n:
            print(f"    known x{n}: {reason}")
    print(f"Unreviewed WARN lines: {len(warns)}")
    for l in warns[:15]:
        print("   ", l[:240])
    return bool(done), len(errors)


if __name__ == "__main__":
    report()
