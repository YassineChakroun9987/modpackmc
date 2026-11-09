"""Collect everything for the story-and-classes review document into tools/classbook.json:
the main questline (prologue, Act I, finale), each class's quests by phase, its skill tree, how it
earns class XP, and the gear its quests point to per phase (with real stats from gear.json).

Usage:  python -I tools/classbook_data.py      then  node tools/classbook_doc.js
Needs server/kubejs/exported/gear.json (`/gl_dev exportgear`).
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "quests" / "src"
OUT = ROOT / "tools" / "classbook.json"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(Path(path).parent))
    spec.loader.exec_module(mod)
    return mod


gd = load_module("gear_data", ROOT / "tools" / "gear_data.py")
sk = load_module("gen_skills", ROOT / "tools" / "skills" / "gen_skills.py")
LANG, _ = gd.load_names()
GEAR = {e["id"]: e for e in json.loads(gd.GEAR.read_text(encoding="utf-8"))["gear"]}

CLASSES = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
STRIP = re.compile(r"&[0-9a-fk-or]")

# How each class earns class XP (from tools/skills/gen_skills.py experience_for()).
XP = {
    "adventurer": ["Every kill (more for tougher mobs) and every boss (a lot)",
                   "Travel: sprinting, swimming, riding and elytra flight (3 XP per 300 blocks)",
                   "Winning raids"],
    "red": ["Kills with melee, fire or blood magic; more with two-handed/heavy weapons, in the Nether, and when you're below 40% health",
            "Hitting enemies in melee while below 40% health",
            "Casting Fire and Blood spells"],
    "orange": ["Mining ores (diamond, emerald and ancient debris the most; not with Silk Touch); a little for stone and deepslate (capped)",
               "Kills in melee or with Nature magic; more in heavy armour (15+ armour) and with hammers or maces",
               "Selling to villagers for emeralds", "Casting Nature spells"],
    "yellow": ["Crafting technology at a crafting table (Create, Mekanism, AE2, airship and Lantern parts)",
               "Kills with swords; more with light blades (rapiers, katanas, twinblades) and lightning; more while you have Speed",
               "Casting Lightning and Technomancy spells"],
    "green": ["Winning raids (big), trading with villagers, curing zombie villagers, building iron golems",
              "Kills of raiders (full XP), other kills with melee, Evocation or Holy magic (half)",
              "Healing (spells and potions, not natural regeneration)", "Casting Evocation and Holy spells"],
    "blue": ["Kills with ice or freezing damage (most), cold mobs, and any kill in a cold biome",
             "Kills shared with other players (your share)", "Elytra flight (3 XP per 400 blocks)", "Casting Ice spells"],
    "indigo": ["Breeding animals and taming them", "Harvesting grown crops",
               "Kills by your tamed animals, and bow or crossbow kills", "Casting summoning spells (extra XP)"],
    "violet": ["Kills with melee, projectiles, Ender or Eldritch magic; more while sneaking or invisible, against undead, at night in the Overworld, in the End, and with daggers",
               "Casting Ender and Eldritch spells"],
}

STAGES = {
    "gl_started": "Log in for the first time", "gl_raid_won": "Win the Warband raid", "gl_warlord_slain": "Warlord Vex is slain",
    "gl_crash_seen": "Reach the crashed Lantern ship", "gl_lantern_heard": "Listen to the dying Lantern",
    "gl_ringbearer": "Get any ring from a ring trial", "gl_ring_white": "Receive the White ring", "gl_ring_black": "Receive the Black ring",
    "gl_chaos_slain": "Kill the Chaos Guardian", "gl_devourer_slain": "Kill the Devourer of Gods",
}


def stage_text(s):
    if s in STAGES:
        return STAGES[s]
    m = re.match(r"gl_(class|whisper|dream|trial|ring|ringed)_(\w+)", s)
    if m:
        what, c = m.groups()
        return {"class": f"Join {c.capitalize()}", "whisper": f"Reach {c.capitalize()} class level 10 (the light whispers)",
                "dream": f"Reach {c.capitalize()} class level 25 (the dream)", "trial": f"Kill {c.capitalize()}'s trial boss",
                "ring": f"Receive the {c.capitalize()} ring", "ringed": f"Finish {c.capitalize()}'s ring trial"}[what]
    return s


def name(kind, rid):
    ns, path = rid.split(":", 1)
    keys = {"entity": [f"entity.{ns}.{path}"], "biome": [f"biome.{ns}.{path}"]}.get(kind, [])
    for k in keys:
        if k in LANG:
            return STRIP.sub("", gd.STRIP.sub("", LANG[k]))
    return gd.pretty(path.split("/")[-1])


def task_text(t):
    ty = t["type"]
    cnt = t.get("count", 1)
    n = f"{cnt}× " if cnt and cnt > 1 else ""
    if ty == "item":
        return f"{'Have' if not t.get('consume') else 'Hand in'} {n}{gd.item_name(LANG, t['item'])}"
    if ty == "kill":
        who = t.get("custom_name") or name("entity", t["entity"])
        return f"Kill {n}{who}"
    if ty == "structure":
        return f"Find a {name('structure', t['structure'])}"
    if ty == "biome":
        return f"Visit {name('biome', t['biome'])}"
    if ty == "dimension":
        return f"Enter {name('dimension', t['dimension'])}"
    if ty == "advancement":
        return f"Advancement: {name('advancement', t['advancement'])}"
    if ty == "stage":
        return stage_text(t["stage"])
    if ty == "checkmark":
        return "Tick the checkbox"
    return ty


def reward_text(r):
    ty = r["type"]
    if ty == "item":
        c = r.get("count", 1)
        return f"{c}× {gd.item_name(LANG, r['item'])}" if c > 1 else gd.item_name(LANG, r["item"])
    if ty == "xp":
        return f"{r['xp']} XP"
    if ty == "xp_levels":
        return f"{r['levels']} levels"
    if ty == "skill_xp":
        return f"{r['amount']} {r['category'].capitalize()} class XP"
    if ty == "loot":
        m = re.search(r"tier_(\d)", r["table"])
        return f"Tier {m.group(1)} loot" if m else "Loot"
    if ty == "command":
        m = re.search(r"/gl class join \{p\} (\w+)", r["command"])
        if m:
            return f"Joins {m.group(1).capitalize()}"
        if "trial begin" in r["command"]:
            return "Starts the ring trial"
        return "Story event"
    if ty == "stage":
        return ""
    return ty


def desc(q, limit=320):
    lines = [STRIP.sub("", l).strip() for l in q.get("desc", []) if l.strip()]
    s = " ".join(lines)
    return s if len(s) <= limit else s[:limit].rsplit(" ", 1)[0] + "…"


def quest_row(q, chapter_keys):
    tasks = q.get("tasks", [])
    opt = all(t.get("optional") for t in tasks) and len(tasks) > 1
    tt = [task_text(t) for t in tasks]
    what = (" or ".join(tt) if opt else "; ".join(tt))
    deps = [d.split(":")[-1] if ":" in d else d for d in q.get("deps", [])]
    return {
        "key": q["key"], "title": STRIP.sub("", q["title"]) + (" (optional)" if q.get("optional") else ""),
        "desc": desc(q), "tasks": what, "rewards": ", ".join(x for x in (reward_text(r) for r in q.get("rewards", [])) if x),
        "after": ", ".join(chapter_keys.get(d, d) for d in q.get("deps", [])), "x": q.get("x", 0), "y": q.get("y", 0),
    }


def load(ch):
    return json.loads((SRC / f"{ch}.json").read_text(encoding="utf-8"))


ALL_TITLES = {}
for f in SRC.glob("*.json"):
    d = json.loads(f.read_text(encoding="utf-8"))
    for q in d["quests"]:
        ALL_TITLES[f"{d['id']}:{q['key']}"] = STRIP.sub("", q["title"])


def chapter(ch):
    d = load(ch)
    keys = {q["key"]: STRIP.sub("", q["title"]) for q in d["quests"]}
    keys.update(ALL_TITLES)
    rows = [quest_row(q, keys) for q in d["quests"]]
    # Book order: every quest after the quests that unlock it (longest unlock chain), then top to bottom.
    deps = {q["key"]: [x for x in q.get("deps", []) if ":" not in x] for q in d["quests"]}
    depth = {}
    def dep_depth(k, seen=()):
        if k not in depth:
            depth[k] = 0 if not deps.get(k) else 1 + max(dep_depth(x, seen + (k,)) for x in deps[k] if x not in seen)
        return depth[k]
    rows.sort(key=lambda r: (dep_depth(r["key"]), r["y"], r["x"]))
    return {"id": ch, "title": STRIP.sub("", d["title"]), "subtitle": STRIP.sub("", d.get("subtitle", "")), "quests": rows}


PHASES = [("Early", 0, 9), ("Mid", 9, 16.5), ("Trial and ring", 16.5, 23.26), ("Late", 23.26, 36.25), ("Legend", 36.25, 999)]


def phase_of(x):
    for n, lo, hi in PHASES:
        if lo <= x < hi:
            return n
    return "Early"


def gear_text(iid):
    e = GEAR.get(iid)
    nm = gd.item_name(LANG, iid)
    if not e:
        return nm if "spell_book" in iid or iid.endswith("_staff") else None
    if e["kind"] == "armor":
        a, t, k, o = gd.armor_stats(e)
        s = f"{gd.fmt(a)} armour" + (f", {gd.fmt(t)} toughness" if t else "")
        b = gd.bonus_text(LANG, o)
        return f"{nm} ({s}{'; ' + b if b else ''})"
    if e["kind"] == "melee":
        r = gd.melee_row(LANG, e)
        return f"{nm} ({r['damage']} dmg, {r['speed']} speed{', two-handed' if r['two_handed'] else ''})"
    return f"{nm} ({e['kind']})"


def class_gear(d):
    out = {}
    for q in d["quests"]:
        ph = phase_of(q.get("x", 0))
        items = [t["item"] for t in q.get("tasks", []) if t["type"] == "item"] + \
                [r["item"] for r in q.get("rewards", []) if r["type"] == "item"]
        for iid in items:
            g = gear_text(iid)
            if g and g not in out.setdefault(ph, []):
                out[ph].append(g)
    return [{"phase": n, "gear": out.get(n, [])} for n, _, _ in PHASES]


def tree(cat):
    spec = sk.TREES[cat]
    order = ["a1", "a2", "b1", "b2", "b3", "b4", "a3", "c1", "c2", "a4", "cap"] if cat != "adventurer" else ["a1", "b1", "b2", "a2", "c1", "c2", "cap"]
    layout = {s[0]: s for s in (sk.CLASS_BRANCH if cat != "adventurer" else sk.ADV_BRANCH)}
    eff = lambda mods: ", ".join(sk.describe(k, v).replace("\n", ", ") for k, v in mods)
    root = spec["root"]
    branches = []
    for bname, nodes in spec["branches"]:
        rows = []
        for slot in order:
            t, mods, _ = nodes[slot]
            rows.append({"node": t, "cost": str(layout[slot][4]), "kind": {"task": "", "goal": "Major", "challenge": "Capstone"}[layout[slot][3]],
                         "effect": eff(mods)})
        branches.append({"name": bname, "nodes": rows})
    m = sk.META[cat]
    return {"title": m["title"], "desc": m["desc"], "root": {"node": root[0], "effect": eff(root[1])}, "branches": branches}


def classes_core():
    t = (ROOT / "server" / "kubejs" / "server_scripts" / "story" / "00_core.js").read_text(encoding="utf-8")
    out = {}
    for c in CLASSES:
        m = re.search(rf"\b{c}:\s*\{{(.*?)\}}", t, re.S)
        body = m.group(1)
        get = lambda k: (re.search(rf"{k}:\s*'((?:[^'\\]|\\.)*)'", body) or [None, ""])[1].replace("\\'", "'")
        out[c] = {"name": get("name"), "ring": gd.item_name(LANG, get("ring")), "boss": get("bossName"),
                  "corps": get("corps"), "motto": get("motto")}
    return out


def main():
    core = classes_core()
    data = {
        "main": [chapter(c) for c in ("prologue", "act1", "finale")],
        "classes": [],
        "adventurer": {"tree": tree("adventurer"), "xp": XP["adventurer"]},
        "levels": {"class_limit": sk.CLASS_LEVEL_LIMIT, "class_spent": sk.CLASS_SPENT_LIMIT, "curve": sk.CLASS_CURVE,
                   "adv_limit": sk.ADV_LEVEL_LIMIT, "cap_spent": sk.CAP_REQUIRED_SPENT},
        "guides": [],
    }
    for c in CLASSES:
        ch = chapter(f"class_{c}")
        for q in ch["quests"]:
            q["phase"] = phase_of(q["x"])
        data["classes"].append({"id": c, **core[c], "chapter": ch, "tree": tree(c), "xp": XP[c],
                                "nemeses": [name("entity", e) for e in sk.NEMESIS[c]], "gear": class_gear(load(f"class_{c}"))})
    for f in sorted(SRC.glob("guide_*.json"), key=lambda p: json.loads(p.read_text(encoding="utf-8"))["order"]):
        d = json.loads(f.read_text(encoding="utf-8"))
        data["guides"].append({"title": STRIP.sub("", d["title"]), "subtitle": STRIP.sub("", d.get("subtitle", "")), "quests": len(d["quests"])})
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"main: {sum(len(c['quests']) for c in data['main'])} quests; classes: "
          + ", ".join(f"{c['id']} {len(c['chapter']['quests'])}" for c in data["classes"]) + f" -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
