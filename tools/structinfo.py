"""Scan mod jars for worldgen structures and conflicts between them.

Usage:  python -I tools/structinfo.py <jar|folder> [<jar|folder> ...]

For every jar it reports:
  - how many structures it adds and how they pick biomes:
      tag   = a biome tag (#c:..., #minecraft:...)  -> works with Terralith/Nullscape biomes
      ids   = fixed biome IDs; "vanilla-only" means it will be rarer under Terralith/Nullscape
  - terrain adaptation used (none = may float/cut into slopes)
  - every VANILLA worldgen file it overrides (data/minecraft/worldgen/...), e.g. a stronghold rewrite
Across all jars it reports:
  - CONFLICTS: the same data file shipped by two or more jars (only one of them will win)
"""
import io
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WG = re.compile(r"^data/([^/]+)/worldgen/(structure|structure_set|template_pool|processor_list)/(.+)\.json$")
BIOME_TAG = re.compile(r"^data/([^/]+)/tags/worldgen/biome/(.+)\.json$")
TAGS = re.compile(r"^data/[^/]+/tags/")  # tags merge across mods, so they're never conflicts
SHARED_OK = {"data/c/worldgen/biome_colors.json", "data/c/worldgen/structure_icons.json"}  # Stardust Labs shared files


def biome_kind(value):
    if isinstance(value, str):
        return ("tag", [value]) if value.startswith("#") else ("ids", [value])
    if isinstance(value, list):
        return ("ids", [v if isinstance(v, str) else v.get("id", "?") for v in value])
    return ("?", [])


def scan(jar_bytes, label, owners, results):
    with zipfile.ZipFile(io.BytesIO(jar_bytes)) as z:
        names = z.namelist()
        info = {"structures": 0, "tag": 0, "ids": 0, "vanilla_only_ids": 0, "adapt": Counter(), "overrides": [], "ns": Counter()}
        for n in names:
            if n.startswith("data/") and n.endswith(".json") and not TAGS.match(n) and n not in SHARED_OK:
                owners[n].append(label)
            m = WG.match(n)
            if not m:
                continue
            ns, kind, path = m.groups()
            if ns == "minecraft":
                info["overrides"].append(f"{kind}/{path}")
            if kind != "structure":
                continue
            try:  # Minecraft reads JSON leniently, so some mods ship // comments; strip full-line ones
                text = z.read(n).decode("utf-8", "replace")
                d = json.loads(re.sub(r"(?m)^\s*//.*$", "", text))
            except ValueError:
                info["unparsed"] = info.get("unparsed", 0) + 1
                continue
            info["structures"] += 1
            info["ns"][ns] += 1
            k, vals = biome_kind(d.get("biomes"))
            if k == "tag":
                info["tag"] += 1
            elif k == "ids":
                info["ids"] += 1
                if vals and all(v.startswith("minecraft:") for v in vals):
                    info["vanilla_only_ids"] += 1
            info["adapt"][d.get("terrain_adaptation", "none")] += 1
        for n in names:
            if n.startswith("META-INF/jarjar/") and n.endswith(".jar"):
                scan(z.read(n), f"{label} > {n.rsplit('/', 1)[-1]}", owners, results)
        if info["structures"] or info["overrides"]:
            results.append((label, info))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    jars = []
    for a in map(Path, sys.argv[1:]):
        jars += sorted(a.glob("*.jar")) if a.is_dir() else [a]
    owners, results = defaultdict(list), []
    for j in jars:
        scan(j.read_bytes(), j.name, owners, results)

    for label, i in results:
        adapt = ", ".join(f"{k}:{v}" for k, v in i["adapt"].most_common())
        print(f"== {label}")
        if i["structures"]:
            vanilla = f" ({i['vanilla_only_ids']} vanilla-only)" if i["vanilla_only_ids"] else ""
            print(f"   {i['structures']} structures ({', '.join(i['ns'])}) | biomes by tag: {i['tag']}, by ids: {i['ids']}{vanilla}")
            print(f"   terrain adaptation: {adapt}")
        if i["overrides"]:
            print(f"   OVERRIDES VANILLA ({len(i['overrides'])}): " + ", ".join(sorted(i["overrides"])[:12])
                  + (" ..." if len(i["overrides"]) > 12 else ""))
    conflicts = {n: o for n, o in owners.items() if len(set(x.split(" > ")[0] for x in o)) > 1}
    print(f"\n== CONFLICTS (same data file in 2+ jars): {len(conflicts)}")
    for n, o in sorted(conflicts.items())[:40]:
        print(f"   {n}\n      <- {' | '.join(sorted(set(o)))}")


if __name__ == "__main__":
    main()
