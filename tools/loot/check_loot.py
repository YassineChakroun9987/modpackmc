# Validates the greenlanterns loot system without booting the server.
# usage: python -I check_loot.py
import json, os, re, sys, subprocess, zipfile, collections

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "server")
EXP = ROOT + "/kubejs/exported"
DATA = ROOT + "/kubejs/data/greenlanterns/loot_table"
SCRIPT = ROOT + "/kubejs/server_scripts/loot/tiered_chest_loot.js"
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = HERE  # harness output and tier_map.json land next to this script (git-ignored)

errors, warns = [], []
def err(m): errors.append(m)
def warn(m): warns.append(m)

def load(name, key):
    return set(json.load(open(os.path.join(EXP, name), encoding="utf8"))[key])
ITEMS = load("items.json", "items")
TABLES = load("loot_tables.json", "loot_tables")
ENCH = load("enchantments.json", "enchantments")
POTIONS = load("potions.json", "potions")
STRUCTS = load("structures.json", "structures")
DIMS = load("dimensions.json", "dimensions")
NAMES = json.load(open(os.path.join(EXP, "item_names.json"), encoding="utf8"))

# spells / schools from mod lang files
SPELLS, SCHOOLS = set(), set()
for jar in os.listdir(ROOT + "/mods"):
    if not jar.endswith(".jar"):
        continue
    z = zipfile.ZipFile(ROOT + "/mods/" + jar)
    for n in z.namelist():
        if n.endswith("/lang/en_us.json"):
            try:
                lang = json.loads(z.read(n))
            except Exception:
                continue
            for k in lang:
                m = re.match(r"spell\.([a-z_]+)\.([a-z_]+)$", k)
                if m and m.group(2) != "none":
                    SPELLS.add(m.group(1) + ":" + m.group(2))
                m = re.match(r"school\.([a-z_]+)\.([a-z_]+)$", k)
                if m:
                    SCHOOLS.add(m.group(1) + ":" + m.group(2))

# ---------------------------------------------------------------- bans
BANNED_RE = re.compile(r"(debug|creative|_test|test_|example|icon|spawn_egg|placeholder|dummy|missing|admin|cheat|"
                       r"command|technical|_disabled|_inventory$|_hand$|spawn_structure|boss_spawner|miniature_structure|"
                       r"plush|trophy|weezer|whoopee|sword_on_a_stick|gecko_|fake_)")
BANNED_NS = {"createlanterns", "draconicevolution", "dog", "darkdoppelganger", "aces_spell_utils", "ftbquests",
             "ftblibrary", "guideme", "patchouli", "lootr", "irons_lib", "familiarslib", "elysium_api"}
BANNED_ITEMS = {
    # boss uniques / boss summons / progression shortcuts that must never come from random chests
    "cataclysm:the_incinerator", "cataclysm:the_annihilator", "cataclysm:the_immolator", "cataclysm:gauntlet_of_guard",
    "cataclysm:gauntlet_of_bulwark", "cataclysm:gauntlet_of_maelstrom", "cataclysm:astrape", "cataclysm:ceraunus",
    "cataclysm:wrath_of_the_desert", "cataclysm:laser_gatling", "cataclysm:tidal_claws", "cataclysm:meat_shredder",
    "cataclysm:void_assault_shoulder_weapon", "cataclysm:wither_assault_shoulder_weapon", "cataclysm:cursed_bow",
    "cataclysm:soul_render", "cataclysm:bulwark_of_the_flame", "cataclysm:abyss_eye", "cataclysm:flame_eye",
    "cataclysm:void_eye", "cataclysm:monstrous_eye", "cataclysm:desert_eye", "cataclysm:mech_eye", "cataclysm:storm_eye",
    "cataclysm:cursed_eye", "minecraft:nether_star", "minecraft:elytra", "minecraft:dragon_egg", "minecraft:command_block",
    "minecraft:barrier", "minecraft:structure_block", "minecraft:debug_stick", "minecraft:knowledge_book",
    "minecraft:bedrock", "minecraft:spawner", "minecraft:trial_spawner", "minecraft:vault", "minecraft:light",
    "irons_spellbooks:legendary_spell_book", "irons_spellbooks:gold_crown", "irons_spellbooks:eldritch_manuscript",
    "iceandfire:dragon_debug_stick", "iceandfire:creative_dragon_meal", "iceandfire:tide_trident_inventory",
    "farmersdelight:debug_pumpkin_pie", "kingsandmonsters:creative_destroyer", "mowziesmobs:mob_remover",
    "mowziesmobs:grant_suns_blessing", "mowziesmobs:logo", "bookofdragons:debug_tame_stick",
    "alexsmobs:effect_item", "alexsmobs:fancy_item", "alexsmobs:tab_icon",
    "simplyswords:mjolnir", "apotheosis:boss_summoner", "apotheosis:potion_charm",
}
BIG_TICKET = set("simplyswords:" + x for x in [
    "arcanethyst", "bloodwake", "bramblethorn", "brimstone_claymore", "caelestis", "chompolotl", "dawnquiver",
    "emberblade", "emberlash", "enigma", "flamewind", "frostfall", "hearthflame", "hiveheart", "icewhisper", "livyatan",
    "magiblade", "magiscythe", "magispear", "molten_edge", "ribboncleaver", "riftmane", "shadowsting",
    "slumbering_lichblade", "soulkeeper", "soulpyre", "soulrender", "soulstealer", "stars_edge", "stormbringer",
    "storms_edge", "stormscale", "tempest", "thunderbrand", "toxic_longsword", "twisted_blade", "watcher_claymore",
    "watching_warglaive", "waxweaver", "whisperwind", "wickpiercer", "wraithfang"]) | {
    "minecraftdungeonsv1:" + x for x in [
        "bone_cudgel_scythe", "broad_sword_claymore", "cursed_axe_double_axe", "encrusted_anchor", "fangs_of_frost_dagger",
        "fighters_binding_fist", "firebrand_axe", "great_hammer_of_gravity", "nameless_blade_cutlass",
        "nightmares_bite_sickle", "spooky_sword", "stormlander_great_hammer", "suns_grace_mace", "battlestaff_growing"]} | {
    "minecraft:netherite_ingot", "minecraft:enchanted_golden_apple", "minecraft:totem_of_undying",
    "minecraft:netherite_upgrade_smithing_template", "minecraft:heart_of_the_sea",
    "iceandfire:fire_dragon_heart", "iceandfire:ice_dragon_heart", "iceandfire:lightning_dragon_heart",
    "iceandfire:dragonbone_sword_fire", "iceandfire:dragonbone_sword_ice", "iceandfire:dragonbone_sword_lightning",
    "iceandfire:dragonbone", "iceandfire:fire_dragon_blood", "iceandfire:ice_dragon_blood", "iceandfire:lightning_dragon_blood",
    "irons_spellbooks:legendary_ink", "irons_spellbooks:diamond_spell_book", "irons_spellbooks:mithril_ingot",
    "irons_spellbooks:netherite_mage_helmet", "irons_spellbooks:netherite_mage_chestplate",
    "irons_spellbooks:netherite_mage_leggings", "irons_spellbooks:netherite_mage_boots",
    "apotheosis:sigil_of_supremacy", "legendary_monsters:enderitium_gem",
    "legendary_monsters:enderitium_upgrade_smithing_template", "alshanex_familiars:life_fruit_tier_3",
    "alshanex_familiars:magic_power_tier_3", "alshanex_familiars:magic_resist_tier_3", "mekanism:alloy_atomic",
    "sophisticatedbackpacks:diamond_backpack", "sophisticatedbackpacks:netherite_backpack", "cataclysm:vitality_ankh",
}
# dragonbone in small amounts is allowed at T3 (it is in vanilla-ish Ice and Fire graveyards), so whitelist that one
BIG_TICKET_T3_OK = {"iceandfire:dragonbone"}

ENTRY_TYPES = {"minecraft:item", "minecraft:empty", "minecraft:loot_table", "minecraft:tag",
               "apotheosis:random_gem", "apotheosis:random_affix_item"}
FUNCS = {"minecraft:set_count", "minecraft:set_potion", "minecraft:enchant_randomly", "minecraft:enchant_with_levels",
         "minecraft:set_damage", "irons_spellbooks:randomize_spell"}
PURITIES = {"cracked", "chipped", "flawed", "normal", "flawless", "perfect"}
RARITIES = {"apotheosis:common", "apotheosis:uncommon", "apotheosis:rare", "apotheosis:epic", "apotheosis:mythic"}

def check_number(v, where, lo=None, hi=None):
    if isinstance(v, (int, float)):
        vals = [v]
    elif isinstance(v, dict) and v.get("type", "minecraft:uniform") == "minecraft:uniform" and set(v) <= {"type", "min", "max"}:
        vals = [v["min"], v["max"]]
        if v["min"] > v["max"]:
            err(where + ": min > max")
    else:
        err(where + ": bad number provider " + json.dumps(v)); return
    for x in vals:
        if not isinstance(x, (int, float)):
            err(where + ": non-numeric " + repr(x))
        if lo is not None and x < lo or hi is not None and x > hi:
            err("%s: %r out of range [%s, %s]" % (where, x, lo, hi))

def check_func(f, where):
    fn = f.get("function")
    if fn not in FUNCS:
        err(where + ": unexpected function " + str(fn)); return
    if fn == "minecraft:set_count":
        check_number(f["count"], where + " count", 1, 64)
    elif fn == "minecraft:set_potion":
        if f.get("id") not in POTIONS:
            err(where + ": unknown potion " + str(f.get("id")))
    elif fn in ("minecraft:enchant_randomly", "minecraft:enchant_with_levels"):
        opts = f.get("options")
        if not isinstance(opts, list) or not opts:
            err(where + ": enchant options must be a non-empty list")
        else:
            for e in opts:
                if e not in ENCH:
                    err(where + ": unknown enchantment " + e)
                if re.search(r"curse|boss|shulker|draconicevolution|redomesticate|infusion", e):
                    err(where + ": unwanted enchantment " + e)
        if fn == "minecraft:enchant_with_levels":
            check_number(f["levels"], where + " levels", 1, 60)
    elif fn == "minecraft:set_damage":
        check_number(f["damage"], where + " damage", 0.05, 1.0)
    elif fn == "irons_spellbooks:randomize_spell":
        q = f.get("quality")
        if not (isinstance(q, dict) and set(q) == {"min", "max"}):
            err(where + ": randomize_spell quality must be {min,max}")
        else:
            check_number(q, where + " spell quality", 0.0, 1.0)
        sf = f.get("spell_filter")
        if sf is not None:
            if "school" in sf and sf["school"] not in SCHOOLS:
                err(where + ": unknown school " + sf["school"])
            for s in sf.get("spells", []):
                if s not in SPELLS:
                    err(where + ": unknown spell " + s)
    extra = set(f) - {"function", "count", "id", "options", "levels", "damage", "quality", "spell_filter"}
    if extra:
        err(where + ": unexpected keys " + str(extra))

GL_TABLES = {}
for dp, dn, fn in os.walk(DATA):
    for f in fn:
        p = os.path.join(dp, f).replace("\\", "/")
        rel = p[len(DATA) + 1:]
        if rel != rel.lower():
            err("uppercase path: " + rel)
        if not rel.endswith(".json"):
            err("non-json file in data: " + rel); continue
        try:
            GL_TABLES["greenlanterns:" + rel[:-5]] = json.load(open(p, encoding="utf8"))
        except Exception as e:
            err("bad json %s: %s" % (rel, e))

ALL_TABLES = TABLES | set(GL_TABLES)
EXT_JSON = SCRATCH + "/jsons"   # extracted mod tables, for following external references

def ext_table(tid):
    ns, path = tid.split(":", 1)
    fp = os.path.join(EXT_JSON, ns, path + ".json")
    return json.load(open(fp, encoding="utf8")) if os.path.exists(fp) else None

def walk_entries(entries, where, sink):
    for i, e in enumerate(entries):
        w = "%s[%d]" % (where, i)
        t = e.get("type")
        if t not in ENTRY_TYPES:
            err(w + ": bad entry type " + str(t)); continue
        if "weight" in e and (not isinstance(e["weight"], int) or e["weight"] < 1):
            err(w + ": weight must be int >= 1")
        if "quality" in e and not isinstance(e["quality"], int):
            err(w + ": quality must be int")
        for j, f in enumerate(e.get("functions", [])):
            check_func(f, w + ".fn%d" % j)
        if t == "minecraft:item":
            n = e.get("name")
            if n not in ITEMS:
                err(w + ": unknown item " + str(n))
            sink.append(("item", n, e))
        elif t == "minecraft:loot_table":
            v = e.get("value")
            if "name" in e:
                err(w + ": loot_table entry uses 'name' (1.21 wants 'value')")
            if v not in ALL_TABLES:
                err(w + ": unknown table " + str(v))
            sink.append(("ref", v, e))
        elif t == "apotheosis:random_gem":
            for p in e.get("purities", []):
                if p not in PURITIES:
                    err(w + ": bad purity " + p)
            sink.append(("gem", None, e))
        elif t == "apotheosis:random_affix_item":
            rs = e.get("rarities", [])
            if not rs:
                err(w + ": affix item needs rarities")
            for r in rs:
                if r not in RARITIES:
                    err(w + ": bad rarity " + r)
            sink.append(("affix", tuple(rs), e))
        elif t == "minecraft:tag":
            sink.append(("tag", e.get("name"), e))

def check_table(tid, data):
    if data.get("type") != "minecraft:chest":
        warn(tid + ": type is not minecraft:chest")
    if set(data) - {"type", "pools", "random_sequence", "functions"}:
        err(tid + ": unexpected top-level keys")
    sink = []
    for pi, p in enumerate(data.get("pools", [])):
        w = "%s pool%d" % (tid, pi)
        if "rolls" not in p:
            err(w + ": no rolls")
        else:
            check_number(p["rolls"], w + " rolls", 1, 10)
        if "bonus_rolls" in p:
            check_number(p["bonus_rolls"], w + " bonus_rolls", 0, 2)
        if not p.get("entries"):
            err(w + ": no entries")
        if set(p) - {"rolls", "bonus_rolls", "entries", "conditions", "functions"}:
            err(w + ": unexpected pool keys " + str(set(p)))
        walk_entries(p.get("entries", []), w, sink)
    return sink

SINKS = {tid: check_table(tid, d) for tid, d in GL_TABLES.items()}

def reachable(tid, seen=None):
    """items reachable from a table (follows greenlanterns + extracted external tables)."""
    seen = seen if seen is not None else set()
    if tid in seen:
        return set()
    seen.add(tid)
    out = set()
    if tid in SINKS:
        sink = SINKS[tid]
    else:
        d = ext_table(tid)
        if d is None:
            return out
        sink = []
        def w(o):
            if isinstance(o, dict):
                if o.get("type") in ("minecraft:item", "item") and "name" in o:
                    sink.append(("item", o["name"] if ":" in o["name"] else "minecraft:" + o["name"], o))
                if o.get("type") in ("minecraft:loot_table",) and isinstance(o.get("value"), str):
                    sink.append(("ref", o["value"], o))
                for v in o.values(): w(v)
            elif isinstance(o, list):
                for v in o: w(v)
        w(d)
    for kind, v, e in sink:
        if kind == "item":
            out.add(v)
        elif kind == "ref":
            out |= reachable(v, seen)
        elif kind == "affix":
            out.add("<affix:" + ",".join(v) + ">")
        elif kind == "gem":
            out.add("<gem>")
    return out

# ---------------------------------------------------------------- contract
REQ = ["greenlanterns:rewards/tier_%d" % i for i in range(1, 6)] + \
      ["greenlanterns:rewards/scrolls_%d" % i for i in range(1, 4)] + \
      ["greenlanterns:rewards/class_" + c for c in ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]] + \
      ["greenlanterns:chests/injected_tier_%d" % i for i in range(1, 6)]
for r in REQ:
    if r not in GL_TABLES:
        err("missing required table " + r)

# ---------------------------------------------------------------- per-tier item rules
report = {}
for tid in sorted(GL_TABLES):
    if "/parts/" in tid:
        continue
    items = reachable(tid)
    m = re.search(r"tier_(\d)$", tid)
    tier = int(m.group(1)) if m else 3   # class bundles = mid-game, treat as tier 3
    if "scrolls_" in tid:
        tier = 3
    for it in items:
        if it.startswith("<"):
            if "mythic" in it and tier < 5:
                err(tid + ": mythic affix below tier 5")
            continue
        ns = it.split(":")[0]
        if ns in BANNED_NS:
            err(tid + ": banned namespace item " + it)
        if it in BANNED_ITEMS or BANNED_RE.search(it.split(":")[1]):
            err(tid + ": banned item " + it)
        if it not in ITEMS:
            err(tid + ": reachable unknown item " + it)
        nm = NAMES.get(it, "")
        if nm.startswith("item.") or nm.startswith("block."):
            warn(tid + ": item without a display name " + it + " (" + nm + ")")
        if tier <= 3 and it in BIG_TICKET and not (tier == 3 and it in BIG_TICKET_T3_OK):
            err("%s: big-ticket item %s at tier %d" % (tid, it, tier))
    report[tid] = items

# ---------------------------------------------------------------- JS static checks
src = open(SCRIPT, encoding="utf8").read()

def js_tokens(s):
    """tiny JS lexer: yields (kind, text) for code/strings/regex/comments."""
    i, n = 0, len(s)
    prev = ""
    out = []
    while i < n:
        c = s[i]
        if s.startswith("//", i):
            j = s.find("\n", i); j = n if j < 0 else j
            out.append(("comment", s[i:j])); i = j; continue
        if s.startswith("/*", i):
            j = s.find("*/", i + 2); j = n if j < 0 else j + 2
            out.append(("comment", s[i:j])); i = j; continue
        if c in "'\"`":
            j = i + 1
            while j < n and s[j] != c:
                j += 2 if s[j] == "\\" else 1
            out.append(("string" if c != "`" else "template", s[i:j + 1])); i = j + 1; prev = "x"; continue
        if c == "/" and (prev in "" or prev in "(,=:[!&|?{};+-*%<>~^" or prev.endswith("return")):
            j = i + 1; cls = False
            while j < n:
                if s[j] == "\\": j += 2; continue
                if s[j] == "[": cls = True
                elif s[j] == "]": cls = False
                elif s[j] == "/" and not cls: break
                elif s[j] == "\n": raise SyntaxError("unterminated regex at %d" % i)
                j += 1
            j += 1
            while j < n and s[j].isalpha(): j += 1
            out.append(("regex", s[i:j])); i = j; prev = "x"; continue
        if c.isspace():
            i += 1; continue
        m = re.match(r"[A-Za-z_$][\w$]*|\d+(\.\d+)?|=>|\.\.\.|===|!==|==|!=|&&|\|\||[^\s]", s[i:])
        tok = m.group(0)
        out.append(("code", tok)); i += len(tok)
        prev = tok if tok != "return" else "return"
    return out

toks = js_tokens(src)
code = [t for k, t in toks if k == "code"]
for a, b in ["()", "[]", "{}"]:
    if code.count(a) != code.count(b):
        err("JS: unbalanced %s%s: %d vs %d" % (a, b, code.count(a), code.count(b)))
depth = 0
for t in code:
    depth += t in "([{"
    depth -= t in ")]}"
    if depth < 0:
        err("JS: closing bracket before opening"); break
for bad in ["let", "const", "=>", "...", "class", "of", "import", "export", "async", "await", "yield"]:
    if bad in code:
        err("JS: ES6 token not wanted in Rhino scripts: " + bad)
if any(k == "template" for k, t in toks):
    err("JS: template literal")
for i in range(len(code) - 1):
    if code[i] in ("{", ",") and code[i + 1] == "[":
        # could be an array element; computed keys look like  { [x]: ...  -> find matching ] then ':'
        d, j = 0, i + 1
        while j < len(code):
            d += code[j] == "["; d -= code[j] == "]"
            if d == 0: break
            j += 1
        if j + 1 < len(code) and code[j + 1] == ":" and code[i] == "{":
            err("JS: computed object key near token %d" % i)
for k, t in toks:
    if k == "regex":
        if re.search(r"\(\?<[=!]|\(\?<[a-z]|\\p\{", t):
            err("JS: regex feature Rhino may not support: " + t)
r = subprocess.run(["node", "--check", SCRIPT], capture_output=True, text=True)
if r.returncode != 0:
    err("JS: node --check failed: " + r.stderr)

# ---------------------------------------------------------------- harness (run the script against real table ids)
out = SCRATCH + "/harness_out.json"
r = subprocess.run(["node", HERE + "/harness.js", SCRIPT, EXP + "/loot_tables.json", out], capture_output=True, text=True)
if r.returncode != 0:
    err("harness failed: " + r.stderr[-2000:])
    H = None
else:
    print(r.stdout.strip())
    H = json.load(open(out, encoding="utf8"))

if H:
    for lvl, msg in H["logs"]:
        if lvl == "error":
            err("script logged error: " + msg)
    tierOf = H["tierOf"]
    for d, t in H["data"]["dims"]:
        if d not in DIMS:
            err("unknown dimension " + d)
    for ss, t in H["data"]["structs"]:
        for s in ss:
            if s not in STRUCTS:
                err("unknown structure " + s)
    for mid, src_t in H["data"]["missing"]:
        if mid in TABLES:
            warn("missing-table entry already exists (will be skipped): " + mid)
        if src_t not in TABLES:
            err("missing-table source does not exist: " + src_t)
    # every modifier references an existing injected table
    def refs(e, acc):
        if e["kind"] == "ref":
            acc.append(e["data"])
        else:
            for c in e["data"]:
                refs(c, acc)
        return acc
    for m in H["modifiers"]:
        for p in m["pools"]:
            for e in p["entries"]:
                for x in refs(e, []):
                    if x not in GL_TABLES:
                        err("modifier references unknown table " + x)
    # coverage: tables structures actually use
    used = json.load(open(HERE + "/structure_tables.json", encoding="utf8"))
    not_tiered = sorted(t for t in used if t in TABLES and t not in tierOf)
    per_tier = collections.Counter(tierOf.values())
    print("\n== tables per tier (classified):", dict(sorted(per_tier.items())), "total", len(tierOf))
    print("== created missing tables:", len(H["created"]))
    print("== structure-used tables with no tier (%d):" % len(not_tiered))
    for t in not_tiered:
        print("   ", t)
    chestish = sorted(t for t in TABLES if re.search(r"chest", t) and t not in tierOf)
    print("== other chest-named tables not injected (%d): %s" % (len(chestish), ", ".join(chestish)))
    # tier listing by namespace
    by_ns = collections.defaultdict(collections.Counter)
    for t, v in tierOf.items():
        by_ns[t.split(":")[0]][v] += 1
    print("== namespace -> tier counts")
    for ns in sorted(by_ns):
        print("   %-28s %s" % (ns, dict(sorted(by_ns[ns].items()))))
    json.dump({t: tierOf[t] for t in sorted(tierOf)}, open(SCRATCH + "/tier_map.json", "w"), indent=0)

# ---------------------------------------------------------------- summary
print("\n== reachable items per top table")
for tid in sorted(report):
    items = report[tid]
    nss = sorted(set(i.split(":")[0] for i in items if not i.startswith("<")))
    print("   %-42s %4d items, %2d mods" % (tid, len(items), len(nss)))
print("\n%d warnings" % len(warns))
for w in warns[:40]:
    print("  WARN", w)
print("%d errors" % len(errors))
for e in errors[:200]:
    print("  ERR ", e)

# ---------------------------------------------------------------- run the script in KubeJS's own Rhino build
RH = SCRATCH + "/rhino"
JAVA = r"C:/Program Files/Java/jdk-25.0.2/bin/java.exe"
RJAR = ROOT + "/mods/" + [j for j in os.listdir(ROOT + "/mods") if j.startswith("rhino-")][0]
if os.path.exists(JAVA) and os.path.exists(RH + "/RhinoCheck.java"):
    r = subprocess.run([JAVA, "-cp", RJAR, RH + "/RhinoCheck.java", RH + "/prelude.js", SCRIPT, RH + "/driver.js", RH + "/ids.txt"],
                       capture_output=True, text=True, cwd=RH)
    first = (r.stdout or "").splitlines()[:1]
    print("\n== Rhino run:", first[0] if first else r.stderr[-1500:])
    if r.returncode != 0 or not first or not first[0].startswith("rhino ok") or "dupes=0" not in first[0] or "ERROR" in r.stdout:
        print("RHINO FAILED"); sys.exit(1)

sys.exit(1 if errors else 0)
