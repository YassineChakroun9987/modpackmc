"""Check that every mod's required dependencies are present (with a compatible version).

Usage:  python -I tools/checkdeps.py --side server <mods_dir> [<mods_dir> ...]
        python -I tools/checkdeps.py --side client <mods_dir> [<mods_dir> ...]

Several dirs are checked as one set (e.g. server/mods + client-only for the client).
Reads META-INF/neoforge.mods.toml from every jar, including jar-in-jar libraries.
Deps marked side=CLIENT are skipped for --side server, and vice versa.
Version ranges are checked on their numeric parts only, which is good enough to catch real mismatches.
"""
import io
import re
import sys
import tomllib
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows console defaults to cp1252

MC = "1.21.1"  # the NeoForge version is read from server/start.bat
BUILTIN = {"minecraft", "neoforge", "forge", "fml", "javafml", "java"}

# (mod, dependency) version complaints we've checked and accepted. Keep the reason!
ACCEPTED = {
    ("jei", "minecraft"): "JEI 19.69 beta declares [1.21,1.21.1) - a typo; NeoForge loads it fine on 1.21.1",
    ("lodestone", "minecraft"): "Lodestone 1.8.2 declares [1.21,1.21.1) - same typo; loads fine in every boot test",
    ("dungeons_arise", "minecraft"): "WDA 2.1.68 declares [1.21,1.21.1) - same typo; loads fine in every boot test",
}


def nums(v):
    return tuple(int(x) for x in re.findall(r"\d+", str(v).split("+")[0].split("-")[0])) or (0,)


def in_range(version, rng):
    rng = (rng or "").strip()
    if not rng or rng == "*" or rng.startswith("${"):
        return True
    if rng[0] not in "[(":
        return True  # a bare version is a soft "recommended" requirement in Maven ranges
    for part in re.findall(r"[\[(][^\])]*[\])]", rng):
        lo_inc, hi_inc = part[0] == "[", part[-1] == "]"
        bounds = part[1:-1].split(",")
        if len(bounds) == 1:  # [1.0] exact
            if nums(version) == nums(bounds[0]):
                return True
            continue
        lo, hi = bounds[0].strip(), bounds[1].strip()
        v = nums(version)
        ok_lo = not lo or (v >= nums(lo) if lo_inc else v > nums(lo))
        ok_hi = not hi or (v <= nums(hi) if hi_inc else v < nums(hi))
        if ok_lo and ok_hi:
            return True
    return False


def read_jar(data, label, found):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = set(z.namelist())
        manifest_ver = None
        if "META-INF/MANIFEST.MF" in names:
            m = re.search(r"Implementation-Version:\s*(\S+)", z.read("META-INF/MANIFEST.MF").decode("utf-8", "replace"))
            manifest_ver = m.group(1) if m else None
        if "META-INF/neoforge.mods.toml" in names:
            try:
                toml = tomllib.loads(z.read("META-INF/neoforge.mods.toml").decode("utf-8", "replace"))
            except tomllib.TOMLDecodeError as e:
                print(f"   ?? {label}: unreadable neoforge.mods.toml ({e})")
                toml = {}
            for mod in toml.get("mods", []):
                ver = mod.get("version", "?")
                if "${" in str(ver):
                    ver = manifest_ver or ver
                found.setdefault(mod["modId"], []).append(
                    {"version": ver, "file": label, "deps": toml.get("dependencies", {}).get(mod["modId"], [])})
        for n in names:
            if n.startswith("META-INF/jarjar/") and n.endswith(".jar"):
                read_jar(z.read(n), f"{label} > {n.rsplit('/', 1)[-1]}", found)


def main():
    args = sys.argv[1:]
    if len(args) < 3 or args[0] != "--side" or args[1] not in ("server", "client"):
        sys.exit(__doc__)
    side, dirs = args[1].upper(), args[2:]
    start_bat = Path(__file__).resolve().parent.parent / "server" / "start.bat"
    nf = re.search(r'set "NEOFORGE=([\d.]+)"', start_bat.read_text()).group(1)

    found = {"minecraft": [{"version": MC, "file": "(game)", "deps": []}],
             "neoforge": [{"version": nf, "file": "(loader)", "deps": []}]}
    jars = [p for d in dirs for p in sorted(Path(d).glob("*.jar"))]
    for jar in jars:
        read_jar(jar.read_bytes(), jar.name, found)

    problems = 0
    print(f"Checked {len(jars)} jars as a {side.lower()} set ({len(found) - 2} mod ids, NeoForge {nf}).")
    for mod_id, entries in sorted(found.items()):
        top = [e for e in entries if " > " not in e["file"]]
        if len(top) > 1:
            print(f"   DUPLICATE  {mod_id}: " + ", ".join(e["file"] for e in top))
            problems += 1
        for e in entries:
            for d in e["deps"]:
                dep_side = str(d.get("side", "BOTH")).upper()
                kind = d.get("type", "required" if d.get("mandatory", False) else "optional").lower()
                if dep_side not in ("BOTH", side):
                    continue
                dep, rng = d.get("modId"), d.get("versionRange", "")
                have = found.get(dep)
                if kind == "required":
                    if not have:
                        print(f"   MISSING    {mod_id} needs {dep} {rng}   ({e['file']})")
                        problems += 1
                    elif not any(in_range(h["version"], rng) for h in have):
                        if (mod_id, dep) in ACCEPTED:
                            print(f"   accepted   {mod_id} needs {dep} {rng}: {ACCEPTED[(mod_id, dep)]}")
                            continue
                        print(f"   VERSION    {mod_id} needs {dep} {rng}, have {', '.join(str(h['version']) for h in have)}")
                        problems += 1
                elif kind in ("incompatible", "discouraged") and have and dep not in BUILTIN:
                    if any(in_range(h["version"], rng) for h in have):
                        print(f"   {kind.upper():<10} {mod_id} vs {dep} {rng}   {d.get('reason', '')}")
                        problems += 1
    print("No problems found." if not problems else f"{problems} problem(s).")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
