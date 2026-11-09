"""Turn server/kubejs/exported/gear.json (from `/gl_dev exportgear`) into the rows of the armour and
weapons document: English names from every mod's lang file, stats computed the way the tooltip shows
them, armour pieces grouped into sets. Writes tools/gear_rows.json for tools/gear_doc.js.

Usage:  python -I tools/gear_data.py
"""
import io
import json
import os
import re
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEAR = ROOT / "server" / "kubejs" / "exported" / "gear.json"
OUT = ROOT / "tools" / "gear_rows.json"
JARS = list((ROOT / "server" / "mods").glob("*.jar")) + list((ROOT / "client-only").glob("*.jar"))
VANILLA = Path(os.environ["APPDATA"]) / ".minecraft" / "versions" / "greenlanterns" / "greenlanterns.jar"

# Not weapons, despite having attack damage.
EXCLUDE = {"twilightforest:stale_bread", "alshanex_familiars:familiar_idol"}

# Mod names as the Word mod list writes them (jar metadata is inconsistent).
MOD_NAMES = {
    "minecraft": "Minecraft (vanilla)", "ae2": "Applied Energistics 2", "aeronautics": "Create Aeronautics",
    "alexsmobs": "Alex's Mobs Continued", "alshanex_familiars": "Alshanex's Familiars", "born_in_chaos_v1": "Born in Chaos",
    "bosses_of_mass_destruction": "Bosses of Mass Destruction", "cataclysm": "L_Ender's Cataclysm",
    "cataclysm_spellbooks": "Cataclysm: Spellbooks", "companions": "Companions!", "create": "Create",
    "discerning_the_eldritch": "Discerning the Eldritch", "draconicevolution": "Draconic Evolution",
    "eternalnether": "Eternal Nether", "farmersdelight": "Farmer's Delight", "galosphere": "Galosphere",
    "galosphere_spellbooks": "Galosphere Spellbooks", "graveyard": "The Graveyard",
    "iceandfire": "Ice and Fire: Community Edition", "irons_spellbooks": "Iron's Spells 'n Spellbooks",
    "kingsandmonsters": "Kings & Monsters", "legendary_monsters": "Legendary Monsters", "magistuarmory": "Epic Knights",
    "mekanism": "Mekanism", "minecraftdungeonsv1": "Dungeons Weapons", "mowziesmobs": "Mowzie's Mobs",
    "mutantmonsters": "Mutant Monsters", "netherexp": "Jaden's Nether Expansion", "rocketnautics": "Create Cosmonautics",
    "shieldexp": "Shield Expansion", "simplyswords": "Simply Swords", "twilightforest": "The Twilight Forest",
}

SLOT_ORDER = ["HELMET", "CHESTPLATE", "LEGGINGS", "BOOTS"]
SLOT_WORDS = r"(helmet|helm|hat|hood|cap|crown|mask|cowl|coif|chestplate|chest|tunic|robes?|jacket|vest|shirt|cuirass|" \
             r"leggings|pants|legs|skirt|trousers|chausses|boots|shoes|sandals|sabatons|greaves)"


# ---------------------------------------------------------------- names
def read_jar(zf, lang, mods):
    for n in zf.namelist():
        if re.fullmatch(r"assets/[^/]+/lang/en_us\.json", n):
            try:
                lang.update(json.loads(zf.read(n).decode("utf-8-sig")))
            except Exception:
                pass
        elif n == "META-INF/neoforge.mods.toml":
            t = zf.read(n).decode("utf-8", "replace")
            for block in re.split(r"\[\[mods\]\]", t)[1:]:
                mid = re.search(r'modId\s*=\s*["\']([^"\']+)', block)
                dn = re.search(r'displayName\s*=\s*["\']([^"\']+)', block)
                if mid and dn:
                    mods[mid.group(1)] = dn.group(1)
        elif n.startswith("META-INF/jarjar/") and n.endswith(".jar"):
            with zipfile.ZipFile(io.BytesIO(zf.read(n))) as inner:
                read_jar(inner, lang, mods)


def load_names():
    lang, mods = {}, {}
    with zipfile.ZipFile(VANILLA) as zf:
        lang.update(json.loads(zf.read("assets/minecraft/lang/en_us.json")))
    for j in JARS:
        try:
            with zipfile.ZipFile(j) as zf:
                read_jar(zf, lang, mods)
        except zipfile.BadZipFile:
            pass
    return lang, mods


def pretty(s):
    return " ".join(w.capitalize() for w in re.split(r"[_/.]", s) if w)


STRIP = re.compile(r"§.")


def item_name(lang, iid):
    ns, path = iid.split(":", 1)
    for k in (f"item.{ns}.{path}", f"block.{ns}.{path}"):
        if k in lang:
            return STRIP.sub("", lang[k])
    return pretty(path)


RENAME = {"Entity Interaction Range": "Reach", "Block Interaction Range": "Block Reach"}


def attr_name(lang, aid):
    n = _attr_name(lang, aid)
    return RENAME.get(n, n)


def _attr_name(lang, aid):
    ns, path = aid.split(":", 1)
    for k in (f"attribute.name.{path}", f"attribute.name.{ns}.{path}", f"attribute.{ns}.{path}", f"attribute.name.{ns}.{path.replace('generic.', '')}"):
        if k in lang:
            return STRIP.sub("", lang[k])
    return pretty(path.replace("generic.", "").replace("player.", ""))


# ---------------------------------------------------------------- stats
def fmt(x):
    return f"{x:.1f}".rstrip("0").rstrip(".") if abs(x - round(x)) > 1e-6 else str(int(round(x)))


def bonus_text(lang, mods):
    """Sum modifiers per (attribute, operation) and write them like the tooltip."""
    acc = defaultdict(float)
    for m in mods:
        acc[(m["attr"], m["op"])] += m["amount"]
    parts = []
    for (attr, op), amt in sorted(acc.items()):
        if abs(amt) < 1e-9:
            continue
        name = attr_name(lang, attr)
        if attr.endswith("knockback_resistance"):
            amt *= 10
        if op == "ADD_VALUE":
            parts.append(f"{'+' if amt > 0 else ''}{fmt(amt)} {name}")
        else:
            parts.append(f"{'+' if amt > 0 else ''}{fmt(amt * 100)}% {name}")
    return ", ".join(parts)


def melee_row(lang, e):
    main = [m for m in e["mods"] if m["slot"] in ("MAINHAND", "HAND", "ANY")]
    dmg_add = sum(m["amount"] for m in main if m["attr"] == "minecraft:generic.attack_damage" and m["op"] == "ADD_VALUE")
    dmg_mul = sum(m["amount"] for m in main if m["attr"] == "minecraft:generic.attack_damage" and m["op"] == "ADD_MULTIPLIED_BASE")
    spd_add = sum(m["amount"] for m in main if m["attr"] == "minecraft:generic.attack_speed" and m["op"] == "ADD_VALUE")
    dmg = (1 + dmg_add) * (1 + dmg_mul)
    spd = max(0.1, 4 + spd_add)
    rest = [m for m in e["mods"] if not (m in main and m["attr"] in ("minecraft:generic.attack_damage", "minecraft:generic.attack_speed")
                                          and m["op"] in ("ADD_VALUE", "ADD_MULTIPLIED_BASE"))]
    bc = e.get("bc") or {}
    if bc.get("category"):
        kind = pretty(bc["category"])
    elif e.get("trident"):
        kind = "Trident"
    elif e.get("mace"):
        kind = "Mace"
    elif e["tags"]["sword"]:
        kind = "Sword"
    elif e["tags"]["axe"]:
        kind = "Axe"
    else:
        kind = "Melee"
    notes = []
    if e.get("mace"):
        notes.append("Smash attack: more damage the further you fall")
    if e.get("trident"):
        notes.append("Can be thrown")
    bonus = ", ".join([b for b in [bonus_text(lang, rest)] if b] + notes)
    if not main and not rest:   # no fixed stats: the item computes them itself
        why = "Stats depend on the modules you install" if e["id"].startswith("draconicevolution:") else "Stats are set by the item itself"
        return {"name": item_name(lang, e["id"]), "type": kind, "damage": "—", "speed": "—", "dps": "—",
                "two_handed": "Yes" if bc.get("twoHanded") else "", "durability": str(e["durability"]) if e["durability"] else "Unbreakable",
                "bonuses": why, "_sort": (kind, 999)}
    return {
        "name": item_name(lang, e["id"]), "type": kind, "damage": fmt(dmg), "speed": fmt(spd), "dps": fmt(dmg * spd),
        "two_handed": "Yes" if bc.get("twoHanded") else "",
        "durability": str(e["durability"]) if e["durability"] else "Unbreakable", "bonuses": bonus,
        "_sort": (kind, dmg),
    }


def armor_stats(piece):
    a = t = k = 0.0
    other = []
    for m in piece["mods"]:
        if m["op"] == "ADD_VALUE" and m["attr"] == "minecraft:generic.armor":
            a += m["amount"]
        elif m["op"] == "ADD_VALUE" and m["attr"] == "minecraft:generic.armor_toughness":
            t += m["amount"]
        elif m["op"] == "ADD_VALUE" and m["attr"] == "minecraft:generic.knockback_resistance":
            k += m["amount"] * 10
        else:
            other.append(m)
    return a, t, k, other


def stem(path):
    s = re.sub(r"(^|_)" + SLOT_WORDS + r"(?=_|$)", "", path)
    return s.strip("_") or path


def set_name(names):
    words = [n.split() for n in names]
    common = []
    for ws in zip(*words):
        if len(set(w.lower() for w in ws)) == 1:
            common.append(ws[0])
        else:
            break
    return " ".join(common)


def armor_sets(lang, pieces):
    groups = defaultdict(list)
    for e in pieces:
        ns, path = e["id"].split(":", 1)
        groups[(ns, e.get("material", "?"), stem(path))].append(e)
    rows = []
    for (ns, material, st), ps in groups.items():
        cells = {}
        total = [0.0, 0.0, 0.0]
        other = []
        durs = []
        for p in sorted(ps, key=lambda p: SLOT_ORDER.index(p["slot"]) if p["slot"] in SLOT_ORDER else 9):
            a, t, k, o = armor_stats(p)
            cells.setdefault(p["slot"], []).append(fmt(a))
            total[0] += a; total[1] += t; total[2] += k
            other += o
            if p["durability"]:
                durs.append(p["durability"])
        names = [item_name(lang, p["id"]) for p in ps]
        nm = set_name(names) if len(ps) > 1 else names[0]
        if not nm:
            nm = pretty(st)
        rows.append({
            "name": nm, "pieces": len(ps),
            "head": "/".join(cells.get("HELMET", [])), "chest": "/".join(cells.get("CHESTPLATE", [])),
            "legs": "/".join(cells.get("LEGGINGS", [])), "feet": "/".join(cells.get("BOOTS", [])),
            "armor": fmt(total[0]), "toughness": fmt(total[1]) if total[1] else "", "kb": fmt(total[2]) if total[2] else "",
            "durability": (f"{min(durs)}–{max(durs)}" if durs and min(durs) != max(durs) else (str(durs[0]) if durs else "Unbreakable")),
            "bonuses": bonus_text(lang, other) or ("Utility gear: no armour value" if total[0] == 0 else ""),
            "_sort": (total[0], total[1]),
        })
    return rows


def main():
    lang, modnames = load_names()
    gear = [e for e in json.loads(GEAR.read_text(encoding="utf-8"))["gear"] if e["id"] not in EXCLUDE]
    by_mod = defaultdict(lambda: {"armor": [], "body": [], "melee": [], "ranged": [], "shield": []})
    for e in gear:
        ns = e["id"].split(":")[0]
        if e["kind"] == "armor":
            by_mod[ns]["body" if e.get("slot") == "BODY" else "armor"].append(e)
        else:
            by_mod[ns][e["kind"]].append(e)
    out = []
    for ns in sorted(by_mod, key=lambda n: (n != "minecraft", (MOD_NAMES.get(n) or n).lower())):
        g = by_mod[ns]
        sets = sorted(armor_sets(lang, g["armor"]), key=lambda r: r["_sort"])
        melee = sorted((melee_row(lang, e) for e in g["melee"]), key=lambda r: r["_sort"])
        ranged = sorted(({"name": item_name(lang, e["id"]), "durability": str(e["durability"]) if e["durability"] else "Unbreakable",
                          "enchantability": str(e["enchantability"]), "bonuses": bonus_text(lang, e["mods"])} for e in g["ranged"]),
                        key=lambda r: r["name"])
        shields = sorted(({"name": item_name(lang, e["id"]), "durability": str(e["durability"]) if e["durability"] else "Unbreakable",
                           "bonuses": bonus_text(lang, e["mods"])} for e in g["shield"]), key=lambda r: r["name"])
        body = sorted(({"name": item_name(lang, e["id"]), "armor": fmt(armor_stats(e)[0]), "durability": str(e["durability"]) if e["durability"] else "—",
                        "bonuses": bonus_text(lang, armor_stats(e)[3])} for e in g["body"]), key=lambda r: r["name"])
        for r in sets + melee:
            r.pop("_sort", None)
        out.append({"ns": ns, "mod": MOD_NAMES.get(ns) or modnames.get(ns, pretty(ns)),
                    "sets": sets, "melee": melee, "ranged": ranged, "shields": shields, "body": body,
                    "counts": {"armor_pieces": len(g["armor"]), "melee": len(melee)}})
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    tot = lambda k: sum(len(m[k]) for m in out)
    print(f"{len(out)} mods: {tot('sets')} armour sets ({sum(m['counts']['armor_pieces'] for m in out)} pieces), {tot('melee')} melee, "
          f"{tot('ranged')} ranged, {tot('shields')} shields, {tot('body')} mount/pet armour -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
