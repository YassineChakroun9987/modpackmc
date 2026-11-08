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
    errors = [l for l in lines if "/ERROR]" in l]
    warns = [l for l in lines if "/WARN]" in l and not any(re.search(p, l) for p in KNOWN_HARMLESS)]

    print("NeoForge:  ", nf.group(1) if nf else "?")
    print(f"Mods ({len(mods)}):", ", ".join(mods))
    if done:
        world = re.search(r"Done \(([\d.]+s)", done).group(1)
        print(f"Boot time:  {(ts(done) - start).total_seconds():.1f}s total  (world load: {world})")
    else:
        print("Boot time:  server did not finish starting (no 'Done' line)")
    print(f"ERROR lines: {len(errors)}")
    for l in errors[:15]:
        print("   ", l[:240])
    print(f"Unreviewed WARN lines: {len(warns)}")
    for l in warns[:15]:
        print("   ", l[:240])
    return bool(done), len(errors)


if __name__ == "__main__":
    report()
