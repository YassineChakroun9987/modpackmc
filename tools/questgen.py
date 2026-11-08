"""Build the FTB Quests book from simple JSON chapter specs.

Usage:  python -I tools/questgen.py            (reads quests/src/*.json, writes server/config/ftbquests/quests/)
        python -I tools/questgen.py --check    (validate only: IDs against kubejs/exported, deps, keys)

Spec format: see quests/README.md. IDs are derived from "<chapter>:<key>", so they stay the same between
runs (player progress survives regenerating the book). Titles and descriptions go to lang/en_us.snbt,
like FTB Quests 2101 does itself.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "quests" / "src"
OUT = ROOT / "server" / "config" / "ftbquests" / "quests"
EXPORTED = ROOT / "server" / "kubejs" / "exported"

GROUPS = [("story", "&6The Story"), ("classes", "&bThe Seven Lights"), ("mods", "&aGuides & Adventures")]
SHAPES = {"circle", "square", "rsquare", "diamond", "pentagon", "hexagon", "octagon", "heart", "gear"}


def hid(*parts):
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:16].upper()


def snbt(v, ind=0):
    pad = "\t" * ind
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, Long):
        return f"{int(v)}L"
    if isinstance(v, Dbl):
        return f"{float(v)}d"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return f"{v}d"
    if isinstance(v, str):
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(v, list):
        if not v:
            return "[ ]"
        inner = "\n".join(pad + "\t" + snbt(x, ind + 1) for x in v)
        return "[\n" + inner + "\n" + pad + "]"
    if isinstance(v, dict):
        inner = "\n".join(f"{pad}\t{k}: {snbt(x, ind + 1)}" for k, x in v.items())
        return "{\n" + inner + "\n" + pad + "}"
    raise TypeError(type(v))


class Long(int):
    pass


class Dbl(float):
    pass


def load_ids():
    ids = {}
    for name in ("items", "entity_types", "structures", "biomes", "dimensions", "advancements_visible"):
        f = EXPORTED / f"{name}.json"
        ids[name] = set(json.loads(f.read_text(encoding="utf-8"))[name]) if f.exists() else None
    return ids


def task_snbt(t, tid, problems, where, ids):
    ty = t["type"]
    out = {"id": tid}
    def check(kind, val):
        if ids.get(kind) is not None and val not in ids[kind]:
            problems.append(f"{where}: unknown {kind[:-1] if kind.endswith('s') else kind} '{val}'")
    if ty == "item":
        check("items", t["item"])
        n = int(t.get("count", 1))
        out.update({"count": Long(n)} if n > 1 else {})
        out["item"] = {"count": min(n, 99) if n > 1 else 1, "id": t["item"]}
        if t.get("consume"):
            out["consume_items"] = True
    elif ty == "kill":
        check("entity_types", t["entity"])
        out["entity"] = t["entity"]
        if t.get("custom_name"):
            out["custom_name"] = t["custom_name"]
        out["value"] = Long(int(t.get("count", 1)))
    elif ty == "advancement":
        check("advancements_visible", t["advancement"])
        out.update({"advancement": t["advancement"], "criterion": t.get("criterion", "")})
    elif ty == "structure":
        if not t["structure"].startswith("#"):
            check("structures", t["structure"])
        out["structure"] = t["structure"]
    elif ty == "dimension":
        check("dimensions", t["dimension"])
        out["dimension"] = t["dimension"]
    elif ty == "biome":
        if not t["biome"].startswith("#"):
            check("biomes", t["biome"])
        out["biome"] = t["biome"]
    elif ty == "stage":
        out["stage"] = t["stage"]
        if t.get("team"):
            out["team_stage"] = True
    elif ty == "checkmark":
        pass
    else:
        problems.append(f"{where}: unknown task type '{ty}'")
    out["type"] = ty
    if t.get("optional"):
        out["optional_task"] = True
    return out


def reward_snbt(r, rid, problems, where, ids):
    ty = r["type"]
    if ty == "item":
        if ids["items"] is not None and r["item"] not in ids["items"]:
            problems.append(f"{where}: unknown reward item '{r['item']}'")
        n = int(r.get("count", 1))
        out = {"id": rid}
        if n > 1:
            out["count"] = n
        out.update({"item": {"count": 1, "id": r["item"]}, "type": "item"})
        return out
    if ty == "xp":
        return {"id": rid, "type": "xp", "xp": int(r["xp"])}
    if ty == "xp_levels":
        return {"id": rid, "type": "xp_levels", "xp_levels": int(r["levels"])}
    if ty == "stage":
        return {"id": rid, "stage": r["stage"], "type": "stage"}
    if ty in ("command", "skill_xp", "loot"):
        if ty == "skill_xp":
            cmd = f"/puffish_skills experience add {{p}} greenlanterns:{r['category']} {int(r['amount'])}"
        elif ty == "loot":
            cmd = f"/loot give {{p}} loot {r['table']}"
        else:
            cmd = r["command"]
        return {"command": cmd, "elevate_perms": True, "id": rid, "silent": bool(r.get("silent", True)), "type": "command"}
    problems.append(f"{where}: unknown reward type '{ty}'")
    return {"id": rid, "type": "xp", "xp": 0}


def main():
    check_only = "--check" in sys.argv
    ids = load_ids()
    specs = sorted(SRC.glob("*.json"))
    chapters, problems, lang = [], [], {}
    keymap = {}
    loaded = []
    for f in specs:
        try:
            spec = json.loads(f.read_text(encoding="utf-8"))
        except ValueError as e:
            problems.append(f"{f.name}: invalid JSON ({e})")
            continue
        loaded.append((f, spec))
        for q in spec.get("quests", []):
            keymap[f"{spec['id']}:{q['key']}"] = hid(spec["id"], q["key"])
    group_ids = {g: hid("group", g) for g, _ in GROUPS}
    for g, title in GROUPS:
        lang[f"chapter_group.{group_ids[g]}.title"] = title
    for f, spec in loaded:
        cid = hid("chapter", spec["id"])
        lang[f"chapter.{cid}.title"] = spec["title"]
        if spec.get("subtitle"):
            lang[f"chapter.{cid}.chapter_subtitle"] = [spec["subtitle"]]
        quests = []
        seen = set()
        for q in spec.get("quests", []):
            where = f"{spec['id']}:{q['key']}"
            if q["key"] in seen:
                problems.append(f"{where}: duplicate key")
            seen.add(q["key"])
            qid = keymap[where]
            deps = []
            for d in q.get("deps", []):
                full = d if ":" in d else f"{spec['id']}:{d}"
                if full not in keymap:
                    problems.append(f"{where}: dependency '{full}' doesn't exist")
                else:
                    deps.append(keymap[full])
            qo = {}
            if deps:
                qo["dependencies"] = deps
            if q.get("dep_mode") == "one":
                qo["dependency_requirement"] = "one_completed"
            if q.get("icon"):
                if ids["items"] is not None and q["icon"] not in ids["items"]:
                    problems.append(f"{where}: unknown icon '{q['icon']}'")
                qo["icon"] = {"id": q["icon"]}
            qo["id"] = qid
            for flag in ("optional", "hide_until_deps_visible", "invisible"):
                if q.get(flag):
                    qo[flag] = True
            rewards = [reward_snbt(r, hid("reward", where, str(i)), problems, where, ids) for i, r in enumerate(q.get("rewards", []))]
            if rewards:
                qo["rewards"] = rewards
            if q.get("shape"):
                if q["shape"] not in SHAPES:
                    problems.append(f"{where}: bad shape '{q['shape']}'")
                qo["shape"] = q["shape"]
            if q.get("size"):
                qo["size"] = Dbl(q["size"])
            tasks = q.get("tasks") or [{"type": "checkmark"}]
            qo["tasks"] = [task_snbt(t, hid("task", where, str(i)), problems, where, ids) for i, t in enumerate(tasks)]
            qo["x"] = Dbl(q.get("x", 0))
            qo["y"] = Dbl(q.get("y", 0))
            quests.append(qo)
            lang[f"quest.{qid}.title"] = q["title"]
            if q.get("subtitle"):
                lang[f"quest.{qid}.quest_subtitle"] = q["subtitle"]
            if q.get("desc"):
                lang[f"quest.{qid}.quest_desc"] = q["desc"] if isinstance(q["desc"], list) else [q["desc"]]
        if spec.get("group") not in group_ids:
            problems.append(f"{spec['id']}: group must be one of {list(group_ids)}")
        icon = spec.get("icon", "minecraft:book")
        if ids["items"] is not None and icon not in ids["items"]:
            problems.append(f"{spec['id']}: unknown chapter icon '{icon}'")
        chapters.append((spec, {
            "default_hide_dependency_lines": False, "default_quest_shape": "", "filename": spec["id"],
            "group": group_ids.get(spec.get("group"), ""), "icon": {"id": icon}, "id": cid,
            "order_index": int(spec.get("order", 0)), "progression_mode": "flexible", "quest_links": [],
            "quests": quests}))

    n_quests = sum(len(c[1]["quests"]) for c in chapters)
    print(f"{len(chapters)} chapters, {n_quests} quests, {len(problems)} problem(s)")
    for p in problems[:80]:
        print("   ", p)
    if check_only or problems:
        sys.exit(1 if problems else 0)

    (OUT / "chapters").mkdir(parents=True, exist_ok=True)
    (OUT / "lang").mkdir(parents=True, exist_ok=True)
    for old in (OUT / "chapters").glob("*.snbt"):
        old.unlink()
    for spec, c in chapters:
        (OUT / "chapters" / f"{spec['id']}.snbt").write_text(snbt(c) + "\n", encoding="utf-8", newline="\n")
    (OUT / "chapter_groups.snbt").write_text(snbt({"chapter_groups": [{"id": group_ids[g]} for g, _ in GROUPS]}) + "\n", encoding="utf-8", newline="\n")
    data = {"default_autoclaim_rewards": "disabled", "default_consume_items": False, "default_quest_disable_jei": False,
            "default_quest_shape": "circle", "default_reward_team": False, "detection_delay": 20, "disable_gui": False,
            "drop_loot_crates": False, "emergency_items_cooldown": 300, "grid_scale": Dbl(0.5),
            "icon": {"id": "createlanterns:power_ring"}, "lock_message": "", "pause_game": False,
            "progression_mode": "flexible", "show_lock_icons": True, "title": "The Book of Oa", "version": 13}
    (OUT / "data.snbt").write_text(snbt(data) + "\n", encoding="utf-8", newline="\n")
    lines = ["{"] + [f"\t{k}: {snbt(v, 1)}" for k, v in sorted(lang.items())] + ["}"]
    (OUT / "lang" / "en_us.snbt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
