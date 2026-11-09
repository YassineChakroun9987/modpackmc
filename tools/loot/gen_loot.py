# Generates greenlanterns loot tables (vanilla 1.21.1 format) into kubejs/data.
# Run: python -I gen_loot.py
import json, os, shutil

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "server", "kubejs", "data", "greenlanterns", "loot_table")

# ---------------------------------------------------------------- helpers
def uni(a, b):
    return {"type": "minecraft:uniform", "min": a, "max": b}

def count_fn(c):
    if c is None:
        return []
    if isinstance(c, (list, tuple)):
        if c[0] == c[1]:
            return [{"function": "minecraft:set_count", "count": c[0]}]
        return [{"function": "minecraft:set_count", "count": uni(c[0], c[1])}]
    return [{"function": "minecraft:set_count", "count": c}]

def entry(base, w, q):
    if w != 1:
        base["weight"] = w
    if q:
        base["quality"] = q
    return base

def item(name, w=1, q=0, c=None, fns=None):
    e = {"type": "minecraft:item", "name": name}
    f = count_fn(c) + (fns or [])
    if f:
        e["functions"] = f
    return entry(e, w, q)

def empty(w, q=0):
    return entry({"type": "minecraft:empty"}, w, q)

def ref(table, w=1, q=0):
    return entry({"type": "minecraft:loot_table", "value": table}, w, q)

def potion(pid, w=1, q=0, kind="minecraft:potion"):
    return item(kind, w, q, fns=[{"function": "minecraft:set_potion", "id": pid}])

def scroll(qmin, qmax, w=1, q=0, school=None, spells=None):
    fn = {"function": "irons_spellbooks:randomize_spell", "quality": {"min": qmin, "max": qmax}}
    if school:
        fn["spell_filter"] = {"school": school}
    if spells:
        fn["spell_filter"] = {"spells": spells}
    return item("irons_spellbooks:scroll", w, q, fns=[fn])

def gem(w, q, purities=None):
    e = {"type": "apotheosis:random_gem"}
    if purities:
        e["purities"] = purities
    return entry(e, w, q)

def affix(w, q, rarities):
    return entry({"type": "apotheosis:random_affix_item", "rarities": rarities}, w, q)

def ench_levels(a, b, opts):
    return {"function": "minecraft:enchant_with_levels", "levels": uni(a, b), "options": opts}

def ench_random(opts):
    return {"function": "minecraft:enchant_randomly", "options": opts}

def damaged(a=0.55, b=0.95):
    return {"function": "minecraft:set_damage", "damage": uni(a, b)}

def book_random(w, q, opts):
    return item("minecraft:book", w, q, fns=[ench_random(opts)])

def book_levels(w, q, a, b, opts):
    return item("minecraft:book", w, q, fns=[ench_levels(a, b, opts)])

def pool(name, rolls, entries, bonus=0):
    p = {"rolls": rolls if not isinstance(rolls, tuple) else uni(rolls[0], rolls[1])}
    if bonus:
        p["bonus_rolls"] = bonus
    p["entries"] = entries
    return p

def table(pools):
    return {"type": "minecraft:chest", "pools": pools}

FILES = {}
def put(path, data):
    FILES[path] = data

GL = "greenlanterns:chests/parts/"

# ---------------------------------------------------------------- enchantment option lists
ENCH_T1 = [
    "minecraft:protection", "minecraft:fire_protection", "minecraft:blast_protection",
    "minecraft:projectile_protection", "minecraft:feather_falling", "minecraft:respiration",
    "minecraft:aqua_affinity", "minecraft:depth_strider", "minecraft:thorns",
    "minecraft:sharpness", "minecraft:smite", "minecraft:bane_of_arthropods", "minecraft:knockback",
    "minecraft:fire_aspect", "minecraft:looting", "minecraft:sweeping_edge",
    "minecraft:efficiency", "minecraft:silk_touch", "minecraft:unbreaking", "minecraft:fortune",
    "minecraft:power", "minecraft:punch", "minecraft:flame", "minecraft:infinity",
    "minecraft:luck_of_the_sea", "minecraft:lure", "minecraft:loyalty", "minecraft:impaling",
    "minecraft:riptide", "minecraft:channeling", "minecraft:multishot", "minecraft:quick_charge",
    "minecraft:piercing", "minecraft:density", "minecraft:breach",
    "farmersdelight:backstabbing", "combat_roll:acrobat", "combat_roll:longfooted",
    "combat_roll:multi_roll", "galosphere:sifting", "galosphere:sustain", "create:capacity",
    "create:potato_recovery", "kingsandmonsters:barbed", "kingsandmonsters:heavy_throw",
    "netherexp:recoil", "netherexp:volley",
]
ENCH_T3 = ENCH_T1 + [
    "minecraft:mending", "minecraft:frost_walker", "minecraft:soul_speed", "minecraft:swift_sneak",
    "minecraft:wind_burst", "galosphere:enfeeble", "galosphere:rupture", "kingsandmonsters:tyrant",
    "netherexp:counterforce", "netherexp:longshot",
    "apothic_enchanting:boon_of_the_earth", "apothic_enchanting:chainsaw",
    "apothic_enchanting:chromatic", "apothic_enchanting:crescendo_of_bolts",
    "apothic_enchanting:growth_serum", "apothic_enchanting:icy_thorns",
    "apothic_enchanting:knowledge_of_the_ages", "apothic_enchanting:miners_fervor",
    "apothic_enchanting:natures_blessing", "apothic_enchanting:rebounding",
    "apothic_enchanting:reflective_defenses", "apothic_enchanting:scavenger",
    "apothic_enchanting:shield_bash", "apothic_enchanting:stable_footing",
    "apothic_enchanting:tempting", "apothic_enchanting:worker_exploitation",
    "apothic_enchanting:berserkers_fury",
]
ENCH_T4 = ENCH_T3 + [
    "apothic_enchanting:endless_quiver", "apothic_enchanting:life_mending",
    "twilightforest:chill_aura", "twilightforest:destruction", "twilightforest:fire_react",
    "twilightforest:renewal", "dungeons_arise:discharge", "dungeons_arise:ensnaring",
    "dungeons_arise:purification", "dungeons_arise:voltaic_shot",
    "nova_structures:traveler", "nova_structures:outreach", "nova_structures:photosynthesis",
    "nova_structures:wax_wings", "nova_structures:illagers_bane", "nova_structures:antidote",
    "nova_structures:ghasted", "nova_structures:gravity", "nova_structures:wither_coated",
]

# ---------------------------------------------------------------- shared sub-tables (parts)
def flat(names, c=None, fns=None):
    return [item(n, 1, 0, c, fns) for n in names]

ART_T2 = ["artifacts:snorkel", "artifacts:umbrella", "artifacts:villager_hat", "artifacts:plastic_drinking_hat",
          "artifacts:flippers", "artifacts:cowboy_hat", "artifacts:night_vision_goggles", "artifacts:digging_claws",
          "artifacts:snowshoes", "artifacts:steadfast_spikes", "artifacts:kitty_slippers", "artifacts:charm_of_sinking",
          "artifacts:onion_ring", "artifacts:everlasting_beef", "artifacts:golden_hook", "artifacts:superstitious_hat",
          "artifacts:lucky_scarf", "artifacts:pickaxe_heater", "artifacts:rooted_boots", "artifacts:strider_shoes",
          "artifacts:obsidian_skull", "artifacts:antidote_vessel", "artifacts:charm_of_shrinking", "artifacts:anglers_hat"]
ART_T3 = ART_T2 + ["artifacts:running_shoes", "artifacts:bunny_hoppers", "artifacts:aqua_dashers",
          "artifacts:cloud_in_a_bottle", "artifacts:feral_claws", "artifacts:power_glove", "artifacts:fire_gauntlet",
          "artifacts:pocket_piston", "artifacts:vampiric_glove", "artifacts:thorn_pendant", "artifacts:flame_pendant",
          "artifacts:shock_pendant", "artifacts:panic_necklace", "artifacts:cross_necklace",
          "artifacts:scarf_of_invisibility", "artifacts:universal_attractor", "artifacts:withered_bracelet",
          "artifacts:novelty_drinking_hat", "artifacts:helium_flamingo", "artifacts:warp_drive", "artifacts:eternal_steak"]
ART_T4 = ART_T3 + ["artifacts:crystal_heart", "artifacts:chorus_totem"]
put("chests/parts/artifacts_t2", table([pool("artifacts", 1, flat(ART_T2))]))
put("chests/parts/artifacts_t3", table([pool("artifacts", 1, flat(ART_T3))]))
put("chests/parts/artifacts_t4", table([pool("artifacts", 1, flat(ART_T4))]))

SS_KINDS = ["chakram", "claymore", "cutlass", "glaive", "greataxe", "greathammer", "halberd", "katana",
            "longsword", "rapier", "sai", "scythe", "spear", "twinblade", "warglaive"]
put("chests/parts/ss_iron", table([pool("ss", 1, flat(["simplyswords:iron_" + k for k in SS_KINDS], fns=[damaged()]))]))
put("chests/parts/ss_diamond", table([pool("ss", 1, flat(["simplyswords:diamond_" + k for k in SS_KINDS], fns=[ench_levels(10, 25, ENCH_T3)]))]))
put("chests/parts/ss_netherite", table([pool("ss", 1, flat(["simplyswords:netherite_" + k for k in SS_KINDS], fns=[ench_levels(20, 35, ENCH_T4)]))]))
put("chests/parts/ss_runic", table([pool("ss", 1, flat(["simplyswords:runic_" + k for k in SS_KINDS]))]))
SS_UNIQUES = ["simplyswords:arcanethyst", "simplyswords:bloodwake", "simplyswords:bramblethorn",
              "simplyswords:brimstone_claymore", "simplyswords:caelestis", "simplyswords:chompolotl",
              "simplyswords:dawnquiver", "simplyswords:emberblade", "simplyswords:emberlash", "simplyswords:enigma",
              "simplyswords:flamewind", "simplyswords:frostfall", "simplyswords:hearthflame", "simplyswords:hiveheart",
              "simplyswords:icewhisper", "simplyswords:livyatan", "simplyswords:magiblade", "simplyswords:magiscythe",
              "simplyswords:magispear", "simplyswords:molten_edge", "simplyswords:ribboncleaver", "simplyswords:riftmane",
              "simplyswords:shadowsting", "simplyswords:slumbering_lichblade", "simplyswords:soulkeeper",
              "simplyswords:soulpyre", "simplyswords:soulrender", "simplyswords:soulstealer", "simplyswords:stars_edge",
              "simplyswords:stormbringer", "simplyswords:storms_edge", "simplyswords:stormscale", "simplyswords:tempest",
              "simplyswords:thunderbrand", "simplyswords:toxic_longsword", "simplyswords:twisted_blade",
              "simplyswords:watcher_claymore", "simplyswords:watching_warglaive", "simplyswords:waxweaver",
              "simplyswords:whisperwind", "simplyswords:wickpiercer", "simplyswords:wraithfang"]
put("chests/parts/ss_uniques", table([pool("ss", 1, flat(SS_UNIQUES))]))

EK_KINDS = ["ahlspiess", "bastardsword", "buckler", "chainmorgenstern", "claymore", "concavehalberd",
            "ellipticalshield", "estoc", "flamebladedsword", "guisarme", "heatershield", "heavymace",
            "heavywarhammer", "katzbalger", "kiteshield", "lochaberaxe", "lucernhammer", "morgenstern",
            "pike", "ranseur", "rondache", "roundshield", "shortsword", "stylet", "target", "tartsche", "zweihander"]
put("chests/parts/ek_iron", table([pool("ek", 1, flat(["magistuarmory:iron_" + k for k in EK_KINDS], fns=[damaged()]))]))
put("chests/parts/ek_steel", table([pool("ek", 1, flat(["magistuarmory:steel_" + k for k in EK_KINDS], fns=[ench_levels(5, 15, ENCH_T1)]))]))
put("chests/parts/ek_diamond", table([pool("ek", 1, flat(["magistuarmory:diamond_" + k for k in EK_KINDS], fns=[ench_levels(10, 25, ENCH_T3)]))]))
put("chests/parts/ek_netherite", table([pool("ek", 1, flat(["magistuarmory:netherite_" + k for k in EK_KINDS], fns=[ench_levels(20, 35, ENCH_T4)]))]))
EK_LIGHT = ["magistuarmory:kettlehat", "magistuarmory:coif", "magistuarmory:bascinet", "magistuarmory:barbute",
            "magistuarmory:gambeson_chestplate", "magistuarmory:gambeson_boots", "magistuarmory:brigandine_chestplate",
            "magistuarmory:halfarmor_chestplate", "magistuarmory:lamellar_chestplate", "magistuarmory:lamellar_boots",
            "magistuarmory:chainmail_chestplate", "magistuarmory:chainmail_leggings", "magistuarmory:chainmail_helmet",
            "magistuarmory:chainmail_boots"]
put("chests/parts/ek_light_armor", table([pool("ek", 1, flat(EK_LIGHT, fns=[damaged(0.6, 1.0)]))]))
EK_PLATE = ["magistuarmory:armet", "magistuarmory:knight_chestplate", "magistuarmory:knight_leggings",
            "magistuarmory:knight_boots", "magistuarmory:greathelm", "magistuarmory:grand_bascinet",
            "magistuarmory:gothic_chestplate", "magistuarmory:gothic_leggings", "magistuarmory:gothic_boots",
            "magistuarmory:maximilian_helmet", "magistuarmory:maximilian_chestplate",
            "magistuarmory:maximilian_leggings", "magistuarmory:maximilian_boots",
            "magistuarmory:kastenbrust_chestplate", "magistuarmory:kastenbrust_leggings",
            "magistuarmory:kastenbrust_boots", "magistuarmory:crusader_chestplate", "magistuarmory:crusader_leggings",
            "magistuarmory:crusader_boots", "magistuarmory:cuirassier_helmet", "magistuarmory:cuirassier_chestplate",
            "magistuarmory:cuirassier_leggings", "magistuarmory:cuirassier_boots", "magistuarmory:face_helmet"]
put("chests/parts/ek_plate_armor", table([pool("ek", 1, flat(EK_PLATE, fns=[ench_levels(10, 25, ENCH_T3)]))]))

MCD_BASIC = ["minecraftdungeonsv1:anchor", "minecraftdungeonsv1:battlestaff", "minecraftdungeonsv1:claymore",
             "minecraftdungeonsv1:cutlass", "minecraftdungeonsv1:dagger", "minecraftdungeonsv1:double_axe",
             "minecraftdungeonsv1:fist", "minecraftdungeonsv1:great_hammer", "minecraftdungeonsv1:mace",
             "minecraftdungeonsv1:sickle", "minecraftdungeonsv1:boneclub_scythe",
             "minecraftdungeonsv1:reinforced_iron_sword", "minecraftdungeonsv1:reinforced_iron_axe",
             "minecraftdungeonsv1:reinforced_iron_pickaxe", "minecraftdungeonsv1:hunter_armor_chestplate",
             "minecraftdungeonsv1:scail_mail_chestplate"]
put("chests/parts/mcd_basic", table([pool("mcd", 1, flat(MCD_BASIC, fns=[damaged(0.6, 1.0)]))]))
MCD_UNIQUES = ["minecraftdungeonsv1:bone_cudgel_scythe", "minecraftdungeonsv1:broad_sword_claymore",
               "minecraftdungeonsv1:cursed_axe_double_axe", "minecraftdungeonsv1:encrusted_anchor",
               "minecraftdungeonsv1:fangs_of_frost_dagger", "minecraftdungeonsv1:fighters_binding_fist",
               "minecraftdungeonsv1:firebrand_axe", "minecraftdungeonsv1:great_hammer_of_gravity",
               "minecraftdungeonsv1:nameless_blade_cutlass", "minecraftdungeonsv1:nightmares_bite_sickle",
               "minecraftdungeonsv1:spooky_sword", "minecraftdungeonsv1:stormlander_great_hammer",
               "minecraftdungeonsv1:suns_grace_mace", "minecraftdungeonsv1:battlestaff_growing",
               "minecraftdungeonsv1:reinforced_diamond_sword", "minecraftdungeonsv1:reinforced_diamond_pickaxe"]
put("chests/parts/mcd_uniques", table([pool("mcd", 1, flat(MCD_UNIQUES))]))

MAGE_LIGHT = []
for s in ["wandering_magician"]:
    MAGE_LIGHT += ["irons_spellbooks:%s_%s" % (s, p) for p in ["helmet", "chestplate", "leggings", "boots"]]
MAGE_LIGHT += ["irons_spellbooks:wizard_hat", "irons_spellbooks:wizard_helmet", "irons_spellbooks:wizard_chestplate",
               "irons_spellbooks:wizard_leggings", "irons_spellbooks:wizard_boots"]
put("chests/parts/irons_mage_armor_light", table([pool("mage", 1, flat(MAGE_LIGHT))]))
MAGE_SETS = ["pyromancer", "cryomancer", "electromancer", "priest", "shadowwalker", "plagued", "archevoker", "cultist"]
MAGE = []
for s in MAGE_SETS:
    MAGE += ["irons_spellbooks:%s_%s" % (s, p) for p in ["helmet", "chestplate", "leggings", "boots"]]
put("chests/parts/irons_mage_armor", table([pool("mage", 1, flat(MAGE))]))
put("chests/parts/irons_netherite_mage_armor", table([pool("mage", 1, flat(
    ["irons_spellbooks:netherite_mage_%s" % p for p in ["helmet", "chestplate", "leggings", "boots"]]))]))
for s in MAGE_SETS:
    put("chests/parts/irons_set_" + s, table([pool("mage", 1, flat(
        ["irons_spellbooks:%s_%s" % (s, p) for p in ["helmet", "chestplate", "leggings", "boots"]]))]))

RUNES = ["irons_spellbooks:%s_rune" % s for s in
         ["fire", "ice", "lightning", "holy", "ender", "blood", "evocation", "nature", "arcane", "cooldown", "protection"]]
put("chests/parts/irons_runes", table([pool("runes", 1, flat(RUNES))]))
ORBS = ["irons_spellbooks:%s_upgrade_orb" % s for s in
        ["fire", "ice", "lightning", "holy", "ender", "blood", "evocation", "nature", "mana", "cooldown", "protection"]]
put("chests/parts/irons_upgrade_orbs", table([pool("orbs", 1, flat(ORBS))]))
put("chests/parts/irons_elixirs", table([pool("elixirs", 1, [
    item("irons_spellbooks:evasion_elixir", 3), item("irons_spellbooks:oakskin_elixir", 3),
    item("irons_spellbooks:invisibility_elixir", 3), item("irons_spellbooks:greater_healing_potion", 2),
    item("irons_spellbooks:netherward_tincture", 2), item("irons_spellbooks:fire_ale", 2),
    potion("irons_spellbooks:instant_mana_one", 3), potion("irons_spellbooks:instant_mana_two", 2)])]))
put("chests/parts/irons_greater_elixirs", table([pool("elixirs", 1, [
    item("irons_spellbooks:greater_evasion_elixir", 2), item("irons_spellbooks:greater_oakskin_elixir", 2),
    item("irons_spellbooks:greater_invisibility_elixir", 2), item("irons_spellbooks:greater_healing_potion", 3),
    potion("irons_spellbooks:instant_mana_three", 2), potion("irons_spellbooks:instant_mana_four", 1)])]))
put("chests/parts/irons_magic_weapons", table([pool("weapons", 1, [
    item("irons_spellbooks:keeper_flamberge", 2), item("irons_spellbooks:autoloader_crossbow", 1),
    item("irons_spellbooks:graybeard_staff", 2), item("irons_spellbooks:ice_staff", 2),
    item("irons_spellbooks:artificer_cane", 2), item("irons_spellbooks:hither_thither_wand", 2),
    item("irons_spellbooks:amethyst_rapier", 2)])]))

DRAGON = [
    item("iceandfire:dragonbone", 10, 0, (2, 5)),
    item("iceandfire:dragonscales_red", 2, 0, (2, 5)), item("iceandfire:dragonscales_green", 2, 0, (2, 5)),
    item("iceandfire:dragonscales_bronze", 2, 0, (2, 5)), item("iceandfire:dragonscales_gray", 2, 0, (2, 5)),
    item("iceandfire:dragonscales_blue", 2, 0, (2, 5)), item("iceandfire:dragonscales_white", 2, 0, (2, 5)),
    item("iceandfire:dragonscales_sapphire", 2, 0, (2, 5)), item("iceandfire:dragonscales_silver", 2, 0, (2, 5)),
    item("iceandfire:dragonscales_electric", 2, 0, (2, 5)), item("iceandfire:dragonscales_amethyst", 2, 0, (2, 5)),
    item("iceandfire:dragonscales_copper", 2, 0, (2, 5)), item("iceandfire:dragonscales_black", 2, 0, (2, 5)),
    item("iceandfire:sea_serpent_scales_blue", 1, 0, (2, 5)), item("iceandfire:sea_serpent_scales_bronze", 1, 0, (2, 5)),
    item("iceandfire:sea_serpent_scales_deepblue", 1, 0, (2, 5)), item("iceandfire:sea_serpent_scales_green", 1, 0, (2, 5)),
    item("iceandfire:sea_serpent_scales_purple", 1, 0, (2, 5)), item("iceandfire:sea_serpent_scales_red", 1, 0, (2, 5)),
    item("iceandfire:sea_serpent_scales_teal", 1, 0, (2, 5)),
    item("iceandfire:fire_dragon_blood", 3, 1), item("iceandfire:ice_dragon_blood", 3, 1),
    item("iceandfire:lightning_dragon_blood", 3, 1),
    item("iceandfire:fire_dragon_flesh", 3, 0, (1, 3)), item("iceandfire:ice_dragon_flesh", 3, 0, (1, 3)),
    item("iceandfire:lightning_dragon_flesh", 3, 0, (1, 3)),
    item("iceandfire:dragon_meal", 4, 0, (2, 4)), item("iceandfire:dragon_horn", 2),
    item("iceandfire:dragonarmor_iron_head", 1), item("iceandfire:dragonarmor_iron_neck", 1),
    item("iceandfire:dragonarmor_iron_body", 1), item("iceandfire:dragonarmor_iron_tail", 1),
    item("iceandfire:troll_leather_forest", 2, 0, (1, 3)), item("iceandfire:troll_leather_frost", 2, 0, (1, 3)),
    item("iceandfire:troll_leather_mountain", 2, 0, (1, 3)),
    item("iceandfire:amphithere_feather", 2, 0, (2, 5)), item("iceandfire:hippogryph_talon", 2, 0, (1, 2)),
    item("iceandfire:deathworm_chitin_yellow", 2, 0, (2, 4)), item("iceandfire:deathworm_chitin_red", 1, 0, (2, 4)),
    item("iceandfire:deathworm_chitin_white", 1, 0, (2, 4)),
    item("bookofdragons:nightfury_scales", 1, 0, (1, 3)), item("bookofdragons:gronckle_scales", 2, 0, (1, 3)),
    item("bookofdragons:deadlynadder_scales", 2, 0, (1, 3)), item("bookofdragons:monstrousnightmare_scales", 2, 0, (1, 3)),
    item("bookofdragons:hideouszippleback_scales", 2, 0, (1, 3)), item("bookofdragons:gronckle_iron", 2, 0, (1, 3)),
]
put("chests/parts/dragon_materials", table([pool("dragon", 1, DRAGON)]))

ALSH_TRINKETS = ["alshanex_familiars:forest_trinket", "alshanex_familiars:frostling_trinket",
                 "alshanex_familiars:scorcher_trinket", "alshanex_familiars:hunter_trinket",
                 "alshanex_familiars:mage_trinket", "alshanex_familiars:cleric_trinket",
                 "alshanex_familiars:plague_trinket", "alshanex_familiars:illusionist_trinket",
                 "alshanex_familiars:necromancer_trinket", "alshanex_familiars:summoner_trinket",
                 "alshanex_familiars:archmage_trinket", "alshanex_familiars:evasion_curio",
                 "alshanex_familiars:healing_curio"]
put("chests/parts/alshanex_trinkets", table([pool("trinkets", 1, flat(ALSH_TRINKETS))]))

# ---------------------------------------------------------------- tier contents
# Each tier: SUPPLIES (common, junk has negative quality), TREASURE (empty has negative quality, so luck
# removes blanks), JACKPOT (tier 4-5 only, big-ticket items, mostly empty).

SUP = {}
TRE = {}
JACK = {}

SUP[1] = [
    # junk: luck makes these rarer
    item("minecraft:rotten_flesh", 30, -3, (2, 6)), item("minecraft:bone", 24, -2, (2, 5)),
    item("minecraft:string", 18, -2, (2, 5)), item("minecraft:stick", 14, -3, (3, 8)),
    item("born_in_chaos_v1:monster_skin", 6, -1, (1, 2)),
    # food
    item("minecraft:bread", 16, 0, (1, 3)), item("farmersdelight:onion", 10, 0, (2, 4)),
    item("farmersdelight:tomato", 10, 0, (2, 4)), item("farmersdelight:cabbage", 8, 0, (1, 3)),
    item("farmersdelight:rice", 8, 0, (2, 5)), item("farmersdelight:fried_egg", 6, 0, (1, 2)),
    item("farmersdelight:egg_sandwich", 5), item("farmersdelight:vegetable_soup", 4),
    item("farmersdelight:cooked_rice", 4), item("galosphere:salted_jerky", 7, 0, (2, 4)),
    item("alexsmobs:banana", 5, 0, (1, 3)), item("create:bar_of_chocolate", 4, 0, (1, 2)),
    item("create:sweet_roll", 3, 0, (1, 2)), item("born_in_chaos_v1:smoked_fish", 5, 0, (1, 3)),
    item("netherexp:hogham", 3, 0, (1, 2)),
    # materials
    item("minecraft:coal", 14, 0, (2, 6)), item("minecraft:iron_nugget", 14, 0, (3, 9)),
    item("minecraft:gold_nugget", 8, 0, (2, 6)), item("minecraft:copper_ingot", 10, 0, (1, 4)),
    item("create:raw_zinc", 9, 0, (1, 3)), item("create:zinc_nugget", 7, 0, (2, 6)),
    item("create:andesite_alloy", 9, 0, (1, 4)), item("create:cogwheel", 5, 0, (1, 3)),
    item("create:shaft", 5, 0, (2, 5)), item("mekanism:raw_tin", 7, 0, (1, 3)),
    item("mekanism:raw_osmium", 7, 0, (1, 3)), item("mekanism:raw_lead", 5, 0, (1, 2)),
    item("mekanism:salt", 4, 0, (2, 5)), item("galosphere:raw_palladium", 5, 0, (1, 2)),
    item("galosphere:allurite_shard", 4, 0, (1, 3)), item("galosphere:lumiere_shard", 4, 0, (1, 3)),
    item("galosphere:pink_salt_shard", 3, 0, (1, 3)), item("iceandfire:silver_nugget", 6, 0, (2, 5)),
    item("kingsandmonsters:raw_bog_iron", 4, 0, (1, 3)), item("createaddition:copper_wire", 3, 0, (2, 4)),
    item("minecraft:flint", 7, 0, (2, 5)), item("minecraft:leather", 7, 0, (1, 3)),
    item("minecraft:paper", 7, 0, (2, 5)), item("minecraft:torch", 9, 0, (4, 10)),
    item("minecraft:arrow", 9, 0, (4, 10)), item("mowziesmobs:dart", 3, 0, (4, 10)),
    item("minecraft:redstone", 6, 1, (2, 5)), item("minecraft:lapis_lazuli", 5, 1, (1, 4)),
    item("ae2:certus_quartz_crystal", 3, 1, (1, 3)), item("companions:copper_coin", 4, 0, (1, 4)),
    # consumables
    potion("minecraft:healing", 4, 1), potion("minecraft:swiftness", 3, 1), potion("minecraft:night_vision", 2, 1),
    item("waystones:warp_dust", 4, 1, (1, 3)), item("waystones:return_scroll", 3, 1),
    item("irons_spellbooks:common_ink", 5, 1), item("irons_spellbooks:arcane_essence", 4, 1, (1, 2)),
    item("minecraft:experience_bottle", 4, 1, (1, 2)), item("minecraft:emerald", 5, 1, (1, 2)),
]
TRE[1] = [
    empty(150, -6),
    book_random(10, 2, ENCH_T1), scroll(0.0, 0.25, 8, 2),
    item("irons_spellbooks:uncommon_ink", 2, 1), item("irons_spellbooks:copper_spell_book", 1, 2),
    ref(GL + "artifacts_t2", 3, 1),
    item("simplyswords:iron_longsword", 2, 0, None, [damaged()]), item("simplyswords:iron_spear", 1, 0, None, [damaged()]),
    item("magistuarmory:iron_shortsword", 2, 0, None, [damaged()]), item("magistuarmory:iron_buckler", 1, 0, None, [damaged()]),
    item("minecraftdungeonsv1:dagger", 2, 0, None, [damaged()]), item("minecraftdungeonsv1:sickle", 1, 0, None, [damaged()]),
    ref(GL + "ek_light_armor", 2), item("minecraft:name_tag", 3), item("minecraft:saddle", 3),
    item("sophisticatedbackpacks:upgrade_base", 2), item("sophisticatedbackpacks:backpack", 1, 2),
    item("sophisticatedstorage:upgrade_base", 1), item("sophisticatedstorage:basic_tier_upgrade", 1),
    item("apotheosis:gem_dust", 3, 1, (1, 2)), item("iceandfire:pixie_dust", 2, 0, (1, 2)),
    item("minecraft:golden_apple", 1, 2), item("minecraft:diamond", 1, 2),
]

SUP[2] = [
    item("minecraft:rotten_flesh", 20, -3, (2, 5)), item("minecraft:bone", 14, -2, (2, 5)),
    item("minecraft:string", 10, -2, (2, 5)), item("minecraft:spider_eye", 7, -2, (1, 3)),
    item("minecraft:gunpowder", 8, 0, (1, 4)),
    item("farmersdelight:beef_stew", 6), item("farmersdelight:chicken_soup", 6), item("farmersdelight:fish_stew", 5),
    item("farmersdelight:hamburger", 5), item("farmersdelight:mutton_wrap", 5),
    item("farmersdelight:pasta_with_meatballs", 4), item("farmersdelight:steak_and_potatoes", 4),
    item("farmersdelight:honey_cookie", 5, 0, (2, 4)), item("farmersdelight:sweet_berry_cookie", 4, 0, (2, 4)),
    item("farmersdelight:apple_pie_slice", 4), item("farmersdelight:cooked_bacon", 6, 0, (2, 4)),
    item("farmersdelight:smoked_ham", 3), item("twilightforest:maze_wafer", 3, 0, (2, 4)),
    item("netherexp:glowcheese", 3), item("kingsandmonsters:ironbelly_stew", 3),
    item("alexsmobs:cooked_kangaroo_meat", 3, 0, (1, 3)), item("cataclysm:amethyst_crab_meat", 3, 0, (1, 2)),
    item("minecraft:cooked_beef", 6, 0, (2, 4)), item("minecraft:golden_carrot", 5, 1, (1, 3)),
    item("minecraft:iron_ingot", 14, 0, (1, 4)), item("minecraft:gold_ingot", 10, 0, (1, 3)),
    item("minecraft:copper_ingot", 8, 0, (2, 5)), item("create:zinc_ingot", 10, 0, (1, 3)),
    item("create:brass_ingot", 5, 1, (1, 2)), item("create:andesite_alloy", 8, 0, (2, 6)),
    item("create:iron_sheet", 5, 0, (1, 3)), item("create:copper_sheet", 4, 0, (1, 3)),
    item("create:cogwheel", 4, 0, (2, 4)), item("create:large_cogwheel", 3, 0, (1, 2)),
    item("create:belt_connector", 3, 0, (1, 2)), item("create:electron_tube", 3, 1, (1, 2)),
    item("create:rose_quartz", 3, 0, (1, 3)),
    item("mekanism:ingot_osmium", 8, 0, (1, 3)), item("mekanism:ingot_tin", 7, 0, (1, 3)),
    item("mekanism:ingot_lead", 6, 0, (1, 3)), item("mekanism:ingot_bronze", 4, 0, (1, 2)),
    item("mekanism:ingot_steel", 3, 1, (1, 2)), item("mekanism:fluorite_gem", 4, 0, (1, 3)),
    item("iceandfire:silver_ingot", 6, 0, (1, 3)), item("galosphere:palladium_ingot", 5, 0, (1, 2)),
    item("galosphere:allurite_shard", 3, 0, (2, 4)), item("galosphere:lumiere_shard", 3, 0, (2, 4)),
    item("kingsandmonsters:bog_iron", 4, 0, (1, 2)), item("born_in_chaos_v1:dark_metal_nugget", 4, 0, (1, 3)),
    item("createaddition:electrum_nugget", 3, 0, (2, 4)), item("ae2:certus_quartz_crystal", 4, 0, (1, 4)),
    item("minecraft:redstone", 8, 0, (3, 8)), item("minecraft:lapis_lazuli", 6, 0, (2, 6)),
    item("minecraft:obsidian", 4, 0, (1, 3)), item("minecraft:emerald", 6, 1, (1, 3)),
    item("minecraft:diamond", 3, 2),
    potion("minecraft:healing", 3, 1), potion("minecraft:swiftness", 3, 1), potion("minecraft:strength", 3, 1),
    potion("minecraft:fire_resistance", 3, 1), potion("minecraft:regeneration", 3, 1),
    potion("minecraft:leaping", 2, 1), potion("minecraft:water_breathing", 2, 1),
    potion("minecraft:healing", 2, 1, "minecraft:splash_potion"), potion("galosphere:astral", 2, 1),
    item("irons_spellbooks:common_ink", 5, 1), item("irons_spellbooks:uncommon_ink", 3, 1),
    item("irons_spellbooks:arcane_essence", 6, 1, (1, 3)), item("irons_spellbooks:fire_ale", 2),
    item("waystones:warp_dust", 5, 0, (2, 4)), item("waystones:return_scroll", 3, 1),
    item("waystones:warp_scroll", 2, 1), item("minecraft:experience_bottle", 6, 1, (1, 3)),
    item("minecraft:ender_pearl", 3, 1, (1, 2)), item("netherexp:antidote", 2),
    item("galosphere:glow_flare", 2, 0, (2, 4)), item("companions:copper_coin", 3, 0, (2, 6)),
]
TRE[2] = [
    empty(110, -5),
    book_random(10, 2, ENCH_T1), book_levels(6, 2, 5, 15, ENCH_T1), scroll(0.05, 0.45, 10, 2),
    item("irons_spellbooks:blank_rune", 4, 1), item("irons_spellbooks:magic_cloth", 2, 2),
    item("irons_spellbooks:copper_spell_book", 2, 2), ref("irons_spellbooks:magic_items/basic_curios", 1, 2),
    ref(GL + "irons_mage_armor_light", 3, 1), ref(GL + "irons_elixirs", 3, 1),
    gem(5, 2, ["cracked", "chipped", "flawed"]),
    affix(4, 2, ["apotheosis:common", "apotheosis:uncommon", "apotheosis:rare"]),
    item("apotheosis:gem_dust", 4, 0, (1, 3)),
    ref(GL + "artifacts_t2", 8, 1),
    ref(GL + "ss_iron", 6), ref(GL + "ek_iron", 6), ref(GL + "mcd_basic", 5), ref(GL + "ek_light_armor", 4),
    item("sophisticatedbackpacks:backpack", 2, 2), item("sophisticatedbackpacks:stack_upgrade_starter_tier", 2),
    item("sophisticatedbackpacks:pickup_upgrade", 1), item("sophisticatedbackpacks:upgrade_base", 2),
    item("sophisticatedstorage:basic_to_copper_tier_upgrade", 1, 1), item("sophisticatedstorage:stack_upgrade_tier_1", 1, 1),
    item("minecraft:golden_apple", 3, 2), item("minecraft:name_tag", 2), item("minecraft:saddle", 2),
    item("minecraft:diamond", 2, 2, (1, 2)), item("iceandfire:pixie_dust", 2, 0, (1, 3)),
    item("graveyard:bone_dagger", 1, 0, None, [damaged()]), item("mowziesmobs:blowgun", 1),
]

SUP[3] = [
    item("minecraft:rotten_flesh", 8, -3, (2, 5)), item("minecraft:bone", 6, -2, (2, 5)),
    item("farmersdelight:roast_chicken", 2), item("farmersdelight:honey_glazed_ham", 2),
    item("farmersdelight:shepherds_pie", 2), item("farmersdelight:steak_and_potatoes", 4),
    item("farmersdelight:pasta_with_mutton_chop", 3), item("farmersdelight:ratatouille", 3),
    item("farmersdelight:squid_ink_pasta", 3), item("farmersdelight:glow_berry_custard", 3),
    item("minecraft:golden_carrot", 5, 0, (2, 4)), item("netherexp:cooked_hogham", 3, 0, (1, 2)),
    item("twilightforest:venison_jerky", 3, 0, (2, 4)), item("alexsmobs:kangaroo_burger", 2),
    item("create:builders_tea", 3), item("create:honeyed_apple", 3, 0, (1, 3)),
    item("minecraft:iron_ingot", 10, 0, (2, 6)), item("minecraft:gold_ingot", 8, 0, (2, 5)),
    item("minecraft:diamond", 5, 1, (1, 2)), item("minecraft:emerald", 6, 0, (2, 5)),
    item("create:brass_ingot", 6, 0, (2, 4)), item("create:zinc_ingot", 5, 0, (2, 5)),
    item("create:precision_mechanism", 3, 1), item("create:electron_tube", 4, 0, (1, 3)),
    item("create:sturdy_sheet", 2, 1, (1, 2)), item("create:polished_rose_quartz", 3, 0, (1, 3)),
    item("mekanism:ingot_osmium", 6, 0, (2, 5)), item("mekanism:ingot_steel", 4, 0, (1, 3)),
    item("mekanism:alloy_infused", 4, 1, (1, 3)), item("mekanism:basic_control_circuit", 3, 1, (1, 2)),
    item("mekanism:ingot_bronze", 3, 0, (2, 4)),
    item("iceandfire:silver_ingot", 4, 0, (2, 4)), item("iceandfire:sapphire_gem", 3, 1, (1, 2)),
    item("galosphere:palladium_ingot", 4, 0, (2, 4)), item("cataclysm:black_steel_ingot", 3, 1, (1, 2)),
    item("cataclysm:ancient_metal_nugget", 3, 0, (2, 5)), item("graveyard:dark_iron_ingot", 3, 0, (1, 2)),
    item("born_in_chaos_v1:dark_metal_ingot", 2, 0, (1, 1)), item("kingsandmonsters:golden_ogre_tooth", 2),
    item("twilightforest:steeleaf_ingot", 2, 0, (1, 3)), item("twilightforest:ironwood_ingot", 2, 0, (1, 3)),
    item("ae2:fluix_crystal", 3, 0, (1, 3)), item("ae2:charged_certus_quartz_crystal", 2, 0, (1, 2)),
    item("createaddition:electrum_ingot", 3, 0, (1, 3)), item("discerning_the_eldritch:starmetal_nugget", 2, 0, (1, 3)),
    item("netherexp:phasmo_shard", 2, 0, (1, 2)), item("bookofdragons:gronckle_iron", 2, 0, (1, 2)),
    item("iceandfire:amphithere_feather", 2, 0, (2, 4)), item("iceandfire:troll_tusk", 1),
    item("minecraft:obsidian", 3, 0, (2, 4)), item("minecraft:blaze_rod", 4, 1, (1, 3)),
    item("minecraft:ender_pearl", 4, 0, (1, 3)), item("minecraft:ghast_tear", 2, 1),
    potion("minecraft:long_strength", 3, 1), potion("minecraft:long_swiftness", 3, 1),
    potion("minecraft:strong_healing", 3, 1), potion("minecraft:long_fire_resistance", 3, 1),
    potion("minecraft:long_regeneration", 2, 1), potion("minecraft:long_night_vision", 2, 1),
    potion("minecraft:long_invisibility", 2, 1), potion("minecraft:long_water_breathing", 2, 1),
    potion("minecraft:strong_leaping", 2, 1), potion("minecraft:long_slow_falling", 2, 1),
    potion("apothic_attributes:knowledge", 2, 1), potion("apothic_attributes:resistance", 2, 1),
    potion("apothic_attributes:vitality", 2, 1), potion("apothic_attributes:haste", 2, 1),
    potion("apothic_attributes:absorption", 2, 1), potion("galosphere:long_astral", 2, 1),
    ref(GL + "irons_elixirs", 6, 1),
    item("irons_spellbooks:arcane_essence", 6, 0, (2, 4)), item("irons_spellbooks:uncommon_ink", 4, 1),
    item("irons_spellbooks:rare_ink", 2, 2), item("irons_spellbooks:cinder_essence", 2, 1),
    item("waystones:warp_scroll", 3, 0, (1, 2)), item("waystones:bound_scroll", 2, 1),
    item("waystones:warp_dust", 3, 0, (3, 6)), item("minecraft:experience_bottle", 6, 1, (2, 5)),
    item("companions:nether_coin", 2, 0, (1, 3)),
]
TRE[3] = [
    empty(75, -4),
    book_levels(10, 2, 15, 30, ENCH_T3), book_random(6, 2, ENCH_T3), scroll(0.2, 0.65, 12, 2),
    ref(GL + "irons_runes", 8, 1), item("irons_spellbooks:blank_rune", 3), item("irons_spellbooks:upgrade_orb", 2, 2),
    item("irons_spellbooks:arcane_ingot", 2, 2), item("irons_spellbooks:mithril_scrap", 1, 2),
    item("irons_spellbooks:magic_cloth", 3), ref("irons_spellbooks:magic_items/basic_curios", 3, 2),
    ref("irons_spellbooks:magic_items/all_focuses", 2, 1), item("irons_spellbooks:iron_spell_book", 1, 2),
    ref(GL + "irons_mage_armor_light", 3, 1), ref(GL + "irons_magic_weapons", 2, 2),
    gem(6, 2, ["chipped", "flawed", "normal"]),
    affix(5, 3, ["apotheosis:uncommon", "apotheosis:rare", "apotheosis:epic"]),
    item("apotheosis:sigil_of_socketing", 2, 2), item("apotheosis:gem_dust", 3, 0, (2, 4)),
    ref(GL + "artifacts_t3", 10, 2), ref(GL + "alshanex_trinkets", 2, 1),
    item("alshanex_familiars:magic_power_tier_1", 1, 2), item("alshanex_familiars:magic_resist_tier_1", 1, 2),
    item("alshanex_familiars:life_fruit_tier_1", 1, 2),
    ref(GL + "ss_diamond", 5), ref(GL + "ss_runic", 2, 2), ref(GL + "ek_steel", 4), ref(GL + "ek_diamond", 3),
    ref(GL + "ek_plate_armor", 3), ref(GL + "mcd_basic", 3),
    item("cataclysm:black_steel_sword", 1, 0, None, [ench_levels(10, 20, ENCH_T3)]),
    item("iceandfire:silver_sword", 1, 0, None, [ench_levels(10, 20, ENCH_T3)]),
    item("twilightforest:steeleaf_sword", 1, 1, None, [ench_levels(10, 20, ENCH_T3)]),
    item("galosphere:sterling_helmet", 1), item("galosphere:sterling_chestplate", 1),
    item("galosphere:sterling_leggings", 1), item("galosphere:sterling_boots", 1),
    item("iceandfire:dragonbone", 2, 2, (1, 3)), item("iceandfire:shiny_scales", 1, 0, (1, 3)),
    item("iceandfire:siren_tear", 1), item("iceandfire:iron_hippogryph_armor", 1),
    item("bookofdragons:gronckle_scales", 1, 0, (1, 3)), item("bookofdragons:deadlynadder_scales", 1, 0, (1, 3)),
    item("sophisticatedbackpacks:copper_backpack", 1, 2), item("sophisticatedbackpacks:stack_upgrade_tier_1", 2, 1),
    item("sophisticatedbackpacks:magnet_upgrade", 1), item("sophisticatedbackpacks:feeding_upgrade", 1),
    item("sophisticatedbackpacks:crafting_upgrade", 1), item("sophisticatedbackpacks:refill_upgrade", 1),
    item("sophisticatedstorage:basic_to_iron_tier_upgrade", 1, 1), item("sophisticatedstorage:compacting_upgrade", 1, 1),
    item("waystones:warp_stone", 1, 2), item("waystones:attuned_shard", 1),
    item("minecraft:golden_apple", 4, 2), item("minecraft:diamond", 3, 2, (2, 3)),
    item("minecraft:experience_bottle", 3, 0, (4, 8)), item("minecraft:diamond_horse_armor", 1),
    item("twilightforest:charm_of_keeping_1", 1, 2), item("twilightforest:ore_magnet", 1),
    item("twilightforest:transformation_powder", 1, 0, (2, 4)),
]

SUP[4] = [
    item("minecraft:golden_carrot", 6, 0, (3, 6)), item("minecraft:golden_apple", 4, 1, (1, 2)),
    item("farmersdelight:roast_chicken", 3), item("farmersdelight:honey_glazed_ham", 3),
    item("farmersdelight:shepherds_pie", 3), item("netherexp:cooked_hogham", 2, 0, (2, 3)),
    item("iceandfire:ambrosia", 2), item("create:honeyed_apple", 3, 0, (2, 4)),
    item("minecraft:diamond", 8, 1, (1, 3)), item("minecraft:emerald", 6, 0, (3, 8)),
    item("minecraft:gold_ingot", 6, 0, (3, 8)), item("minecraft:iron_ingot", 6, 0, (4, 10)),
    item("minecraft:netherite_scrap", 2, 2), item("minecraft:ancient_debris", 1, 2),
    item("create:precision_mechanism", 4, 0, (1, 2)), item("create:brass_ingot", 4, 0, (3, 6)),
    item("create:sturdy_sheet", 3, 0, (1, 3)),
    item("mekanism:alloy_infused", 4, 0, (2, 4)), item("mekanism:alloy_reinforced", 3, 1, (1, 2)),
    item("mekanism:advanced_control_circuit", 2, 1), item("mekanism:ingot_refined_obsidian", 2, 1, (1, 2)),
    item("mekanism:ingot_refined_glowstone", 3, 0, (1, 3)),
    item("iceandfire:silver_ingot", 3, 0, (3, 6)), item("iceandfire:sapphire_gem", 3, 0, (1, 3)),
    item("cataclysm:black_steel_ingot", 3, 0, (2, 4)), item("cataclysm:ancient_metal_ingot", 2, 1),
    item("cataclysm:ancient_metal_nugget", 3, 0, (3, 6)), item("graveyard:dark_iron_ingot", 2, 0, (2, 3)),
    item("iceandfire:ghost_ingot", 1, 1), item("galosphere:palladium_ingot", 3, 0, (3, 6)),
    item("discerning_the_eldritch:starmetal_nugget", 2, 0, (2, 5)), item("ae2:fluix_crystal", 2, 0, (2, 5)),
    item("twilightforest:ironwood_ingot", 1, 0, (2, 4)), item("twilightforest:steeleaf_ingot", 1, 0, (2, 4)),
    item("bookofdragons:gronckle_iron", 2, 0, (2, 3)), item("minecraft:blaze_rod", 3, 0, (2, 5)),
    item("minecraft:ender_pearl", 3, 0, (2, 4)), item("eternalnether:warped_ender_pearl", 2, 0, (1, 2)),
    potion("minecraft:strong_healing", 3, 1), potion("minecraft:strong_strength", 3, 1),
    potion("minecraft:strong_regeneration", 3, 1), potion("minecraft:long_turtle_master", 2, 1),
    potion("minecraft:long_invisibility", 2, 1), potion("minecraft:strong_swiftness", 3, 1),
    potion("apothic_attributes:long_resistance", 2, 1), potion("apothic_attributes:strong_vitality", 2, 1),
    potion("apothic_attributes:long_knowledge", 2, 1), potion("apothic_attributes:long_haste", 2, 1),
    potion("apothic_attributes:strong_absorption", 2, 1),
    ref(GL + "irons_greater_elixirs", 6, 1),
    item("irons_spellbooks:rare_ink", 4, 1), item("irons_spellbooks:epic_ink", 1, 2),
    item("irons_spellbooks:arcane_essence", 4, 0, (3, 6)), item("minecraft:experience_bottle", 6, 0, (4, 10)),
    item("waystones:warp_scroll", 2, 0, (2, 3)), item("waystones:bound_scroll", 2),
    item("companions:nether_coin", 2, 0, (2, 4)), item("companions:end_coin", 1, 1, (1, 2)),
]
TRE[4] = [
    empty(40, -3),
    book_levels(12, 2, 25, 35, ENCH_T4), scroll(0.4, 0.85, 14, 2),
    ref(GL + "irons_runes", 10, 1), ref(GL + "irons_upgrade_orbs", 5, 2),
    item("irons_spellbooks:arcane_ingot", 3, 0, (1, 2)), item("irons_spellbooks:mithril_scrap", 2, 1, (1, 2)),
    item("irons_spellbooks:mithril_ingot", 1, 3), item("irons_spellbooks:energized_core", 1, 2),
    item("irons_spellbooks:divine_pearl", 1, 2), ref("irons_spellbooks:magic_items/basic_curios", 4, 2),
    ref("irons_spellbooks:magic_items/all_focuses", 2, 1), item("irons_spellbooks:iron_spell_book", 2, 2),
    item("irons_spellbooks:gold_spell_book", 1, 3), ref(GL + "irons_mage_armor", 5, 1),
    ref(GL + "irons_magic_weapons", 4, 2),
    gem(8, 2), affix(6, 3, ["apotheosis:rare", "apotheosis:epic"]),
    item("apotheosis:sigil_of_socketing", 2), item("apotheosis:sigil_of_enhancement", 1, 2),
    item("apotheosis:sigil_of_withdrawal", 1), item("apotheosis:gem_dust", 2, 0, (3, 6)),
    ref(GL + "artifacts_t4", 8, 2), ref(GL + "alshanex_trinkets", 3, 1),
    item("alshanex_familiars:magic_power_tier_2", 1, 2), item("alshanex_familiars:magic_resist_tier_2", 1, 2),
    item("alshanex_familiars:life_fruit_tier_2", 1, 2),
    ref(GL + "ss_netherite", 3), ref(GL + "ss_runic", 3, 1), ref(GL + "ss_uniques", 2, 2),
    ref(GL + "ek_netherite", 2), ref(GL + "ek_plate_armor", 3), ref(GL + "mcd_uniques", 2, 2),
    ref(GL + "dragon_materials", 8, 1),
    item("cataclysm:sturdy_boots", 1, 2), item("cataclysm:berserker_soul_amulet", 1, 2),
    item("sophisticatedbackpacks:iron_backpack", 1, 2), item("sophisticatedbackpacks:stack_upgrade_tier_2", 1, 2),
    item("sophisticatedbackpacks:advanced_magnet_upgrade", 1), item("sophisticatedbackpacks:advanced_pickup_upgrade", 1),
    item("sophisticatedstorage:iron_to_gold_tier_upgrade", 1, 1), item("sophisticatedstorage:stack_upgrade_tier_2", 1, 1),
    item("minecraft:totem_of_undying", 2, 2), item("minecraft:golden_apple", 4, 0, (1, 2)),
    item("minecraft:diamond", 3, 1, (2, 4)), item("minecraft:netherite_scrap", 2, 2, (1, 2)),
    item("twilightforest:charm_of_life_1", 1, 2), item("twilightforest:charm_of_keeping_2", 1, 2),
    item("waystones:warp_stone", 2, 1),
]
JACK[4] = [
    empty(300, -10),
    item("minecraft:netherite_ingot", 2, 2), item("minecraft:enchanted_golden_apple", 3, 2),
    ref(GL + "ss_uniques", 4, 2), ref(GL + "mcd_uniques", 3, 2),
    item("legendary_monsters:enderitium_gem", 2, 1), affix(3, 2, ["apotheosis:epic"]),
    item("minecraft:netherite_upgrade_smithing_template", 2, 1), item("minecraft:trident", 1, 1),
    item("irons_spellbooks:epic_ink", 2, 2),
]

SUP[5] = [
    item("minecraft:golden_carrot", 5, 0, (4, 8)), item("minecraft:golden_apple", 5, 1, (1, 3)),
    item("farmersdelight:roast_chicken", 2), item("farmersdelight:honey_glazed_ham", 2),
    item("iceandfire:ambrosia", 3, 0, (1, 2)),
    item("minecraft:diamond", 10, 1, (2, 4)), item("minecraft:emerald", 6, 0, (6, 12)),
    item("minecraft:gold_ingot", 4, 0, (6, 12)), item("minecraft:netherite_scrap", 4, 2, (1, 2)),
    item("minecraft:ancient_debris", 2, 2, (1, 2)),
    item("create:precision_mechanism", 3, 0, (2, 3)), item("create:sturdy_sheet", 3, 0, (2, 4)),
    item("mekanism:alloy_reinforced", 3, 0, (1, 3)), item("mekanism:alloy_atomic", 1, 2),
    item("mekanism:elite_control_circuit", 1, 2), item("mekanism:ingot_refined_obsidian", 3, 0, (1, 3)),
    item("cataclysm:ancient_metal_ingot", 3, 1, (1, 2)), item("cataclysm:black_steel_ingot", 2, 0, (3, 5)),
    item("iceandfire:sapphire_gem", 3, 0, (2, 4)), item("iceandfire:ghost_ingot", 2, 1),
    item("discerning_the_eldritch:starmetal_nugget", 2, 0, (3, 6)), item("eternalnether:warped_ender_pearl", 2, 0, (1, 3)),
    item("minecraft:ender_pearl", 3, 0, (3, 6)), item("minecraft:blaze_rod", 3, 0, (3, 6)),
    potion("minecraft:strong_healing", 3, 1), potion("minecraft:strong_strength", 3, 1),
    potion("minecraft:strong_regeneration", 3, 1), potion("minecraft:strong_turtle_master", 2, 1),
    potion("apothic_attributes:strong_resistance", 2, 1), potion("apothic_attributes:strong_vitality", 2, 1),
    potion("apothic_attributes:strong_knowledge", 2, 1), potion("apothic_attributes:long_flying", 1, 2),
    ref(GL + "irons_greater_elixirs", 6, 1),
    item("irons_spellbooks:epic_ink", 3, 1), item("irons_spellbooks:rare_ink", 3, 0),
    item("irons_spellbooks:arcane_essence", 3, 0, (4, 8)), item("minecraft:experience_bottle", 6, 0, (8, 16)),
    item("companions:end_coin", 2, 0, (1, 3)),
]
TRE[5] = [
    empty(30, -3),
    book_levels(12, 2, 30, 45, ENCH_T4), scroll(0.6, 1.0, 14, 3),
    ref(GL + "irons_runes", 6), ref(GL + "irons_upgrade_orbs", 8, 2),
    item("irons_spellbooks:mithril_ingot", 2, 2, (1, 2)), item("irons_spellbooks:arcane_ingot", 3, 0, (2, 3)),
    item("irons_spellbooks:legendary_ink", 1, 3), ref("irons_spellbooks:magic_items/basic_curios", 4, 2),
    item("irons_spellbooks:gold_spell_book", 2, 2), item("irons_spellbooks:diamond_spell_book", 1, 3),
    ref(GL + "irons_mage_armor", 4, 1), ref(GL + "irons_netherite_mage_armor", 1, 3),
    ref(GL + "irons_magic_weapons", 3, 2),
    gem(8, 2), affix(8, 3, ["apotheosis:rare", "apotheosis:epic", "apotheosis:mythic"]),
    item("apotheosis:sigil_of_enhancement", 2, 1), item("apotheosis:sigil_of_supremacy", 1, 2),
    item("apotheosis:sigil_of_socketing", 2),
    ref(GL + "artifacts_t4", 10, 2), ref(GL + "alshanex_trinkets", 3),
    item("alshanex_familiars:magic_power_tier_3", 1, 2), item("alshanex_familiars:magic_resist_tier_3", 1, 2),
    item("alshanex_familiars:life_fruit_tier_3", 1, 3),
    ref(GL + "ss_netherite", 4), ref(GL + "ss_uniques", 4, 2), ref(GL + "mcd_uniques", 3, 2),
    ref(GL + "ek_netherite", 3), ref(GL + "ek_plate_armor", 3),
    item("minecraft:diamond_chestplate", 1, 1, None, [ench_levels(30, 40, ENCH_T4)]),
    item("minecraft:diamond_sword", 1, 1, None, [ench_levels(30, 40, ENCH_T4)]),
    item("minecraft:diamond_pickaxe", 1, 1, None, [ench_levels(30, 40, ENCH_T4)]),
    ref(GL + "dragon_materials", 10, 1),
    item("iceandfire:dragonbone_sword_fire", 1, 2), item("iceandfire:dragonbone_sword_ice", 1, 2),
    item("iceandfire:dragonbone_sword_lightning", 1, 2),
    item("iceandfire:dragonarmor_gold_body", 1), item("iceandfire:dragonarmor_diamond_head", 1),
    item("cataclysm:sturdy_boots", 1, 1), item("cataclysm:vitality_ankh", 1, 2),
    item("legendary_monsters:enderitium_gem", 2, 2), item("legendary_monsters:enderitium_upgrade_smithing_template", 1, 2),
    item("sophisticatedbackpacks:gold_backpack", 1, 2), item("sophisticatedbackpacks:diamond_backpack", 1, 3),
    item("sophisticatedbackpacks:stack_upgrade_tier_3", 1, 2),
    item("sophisticatedstorage:gold_to_diamond_tier_upgrade", 1, 2), item("sophisticatedstorage:stack_upgrade_tier_3", 1, 2),
    item("minecraft:totem_of_undying", 3, 2), item("minecraft:enchanted_golden_apple", 2, 2),
    item("minecraft:netherite_scrap", 3, 2, (1, 3)), item("minecraft:heart_of_the_sea", 1, 2),
    item("twilightforest:charm_of_life_2", 1, 2),
]
JACK[5] = [
    empty(140, -8),
    ref(GL + "ss_uniques", 6, 2), ref(GL + "mcd_uniques", 4, 2),
    item("iceandfire:fire_dragon_heart", 1, 2), item("iceandfire:ice_dragon_heart", 1, 2),
    item("iceandfire:lightning_dragon_heart", 1, 2),
    item("minecraft:netherite_ingot", 3, 2), item("minecraft:enchanted_golden_apple", 3, 2),
    affix(3, 3, ["apotheosis:epic", "apotheosis:mythic"]),
    item("irons_spellbooks:legendary_ink", 2, 2), scroll(0.85, 1.0, 3, 2),
    item("minecraft:netherite_upgrade_smithing_template", 2, 1),
]

ROLLS = {
    # tier: (supply rolls, supply bonus/luck, treasure rolls, treasure bonus/luck)
    1: ((1, 2), 0.25, 1, 0.15),
    2: ((2, 3), 0.3, 1, 0.2),
    3: ((2, 3), 0.35, (1, 2), 0.25),
    4: ((2, 4), 0.4, 2, 0.35),
    5: ((3, 4), 0.4, (2, 3), 0.4),
}
for t in range(1, 6):
    sr, sb, tr, tb = ROLLS[t]
    pools = [pool("supplies", sr, SUP[t], sb), pool("treasure", tr, TRE[t], tb)]
    if t in JACK:
        pools.append(pool("jackpot", 1, JACK[t], 0.1))
    put("chests/injected_tier_%d" % t, table(pools))

# ---------------------------------------------------------------- reward tables (quests, /loot give)
def no_empty(lst):
    return [e for e in lst if e["type"] != "minecraft:empty"]

def no_junk(lst):
    return [e for e in lst if e.get("quality", 0) >= 0]

REWARD = {
    # tier: (goodies rolls, supply rolls, emeralds, xp bottles, extra list)
    1: (2, 2, (2, 5), (1, 3), []),
    2: (3, 2, (3, 8), (2, 5), []),
    3: (3, 3, (5, 12), (3, 8), [item("minecraft:diamond", 1, 0, (1, 2))]),
    4: (4, 3, (8, 16), (6, 12), [item("minecraft:diamond", 1, 0, (2, 4))]),
    5: (5, 3, (16, 32), (10, 20), [item("minecraft:diamond", 1, 0, (3, 6)), item("minecraft:netherite_scrap", 1, 0, (1, 2))]),
}
for t in range(1, 6):
    gr, sr, em, xp, extra = REWARD[t]
    pools = [
        pool("goodies", gr, no_empty(TRE[t])),
        pool("supplies", sr, no_junk(SUP[t])),
        pool("emeralds", 1, [item("minecraft:emerald", 1, 0, em)]),
        pool("experience", 1, [item("minecraft:experience_bottle", 1, 0, xp)]),
    ]
    for x in extra:
        pools.append(pool("extra", 1, [x]))
    if t >= 4:
        jack = [e for e in JACK[t] if e["type"] != "minecraft:empty"]
        pools.append(pool("jackpot", 1, [empty(60 if t == 4 else 25, -3)] + jack))
    put("rewards/tier_%d" % t, table(pools))

put("rewards/scrolls_1", table([pool("scrolls", 2, [scroll(0.0, 0.3)])]))
put("rewards/scrolls_2", table([pool("scrolls", 2, [scroll(0.3, 0.6)])]))
put("rewards/scrolls_3", table([pool("scrolls", 2, [scroll(0.6, 0.85)])]))

IS = "irons_spellbooks:"
def class_bundle(scroll_entries, runes, orb, armor_set, gear, consumables, extra=None):
    pools = [
        pool("class_scrolls", 2, scroll_entries),
        pool("runes", 1, runes),
        pool("upgrade_orb", 1, [item(orb)]),
        pool("ink", 1, [item(IS + "uncommon_ink", 1, 0, (1, 2))]),
        pool("ink_rare", 1, [item(IS + "rare_ink")]),
        pool("armor", 1, [ref(GL + "irons_set_" + armor_set)]),
        pool("gear", 1, gear),
        pool("consumables", 2, consumables),
        pool("gem", 1, [gem(1, 0, ["chipped", "flawed", "normal"])]),
        pool("emeralds", 1, [item("minecraft:emerald", 1, 0, (6, 12))]),
    ]
    if extra:
        pools.append(pool("extra", 1, extra))
    return table(pools)

def sch(s, a=0.3, b=0.7, w=1):
    return scroll(a, b, w, 0, school="irons_spellbooks:" + s)

ss = lambda k: item("simplyswords:iron_" + k, 1, 0, None, [ench_levels(10, 20, ENCH_T3)])
ek = lambda k: item("magistuarmory:steel_" + k, 1, 0, None, [ench_levels(10, 20, ENCH_T3)])

put("rewards/class_red", class_bundle(
    [sch("fire", w=3), sch("blood", w=1)],
    [item(IS + "fire_rune", 3, 0, (2, 4)), item(IS + "blood_rune", 1, 0, (1, 2))],
    IS + "fire_upgrade_orb", "pyromancer",
    [ss("greataxe"), ss("claymore"), ek("zweihander"), ek("heavymace"), item("minecraftdungeonsv1:double_axe")],
    [potion("minecraft:strength", 2), potion("minecraft:long_fire_resistance", 2), item(IS + "fire_ale", 2),
     item("minecraft:blaze_rod", 1, 0, (2, 4)), item("farmersdelight:steak_and_potatoes", 1, 0, (2, 3))]))
put("rewards/class_orange", class_bundle(
    [scroll(0.3, 0.7, 2, 0, spells=["irons_spellbooks:earthquake", "irons_spellbooks:stomp", "irons_spellbooks:oakskin"]),
     sch("nature", w=1)],
    [item(IS + "nature_rune", 3, 0, (2, 4)), item(IS + "protection_rune", 1, 0, (1, 2))],
    IS + "nature_upgrade_orb", "plagued",
    [ek("heatershield"), ek("pavese"), ek("heavywarhammer"), ss("greathammer"), item("minecraftdungeonsv1:great_hammer")],
    [item(IS + "oakskin_elixir", 2), potion("apothic_attributes:resistance", 2), potion("minecraft:long_turtle_master", 1),
     item("farmersdelight:beef_stew", 1, 0, (2, 3)), item("minecraft:golden_carrot", 1, 0, (3, 6))]))
put("rewards/class_yellow", class_bundle(
    [sch("lightning", w=3)],
    [item(IS + "lightning_rune", 3, 0, (2, 4)), item(IS + "cooldown_rune", 1, 0, (1, 2))],
    IS + "lightning_upgrade_orb", "electromancer",
    [ss("rapier"), ss("katana"), ss("spear"), ek("estoc"), item("artifacts:running_shoes")],
    [potion("minecraft:strong_swiftness", 2), item(IS + "lightning_bottle", 2), item(IS + "evasion_elixir", 1),
     item("create:precision_mechanism", 1), item("mekanism:basic_control_circuit", 1, 0, (1, 2))]))
put("rewards/class_green", class_bundle(
    [sch("evocation", w=2), sch("holy", w=2)],
    [item(IS + "evocation_rune", 2, 0, (2, 3)), item(IS + "holy_rune", 2, 0, (2, 3))],
    IS + "holy_upgrade_orb", "priest",
    [ss("longsword"), ek("kiteshield"), ek("bastardsword"), ek("heatershield"), item("minecraftdungeonsv1:mace")],
    [potion("minecraft:strong_healing", 2), item(IS + "greater_healing_potion", 2), item("minecraft:golden_apple", 1),
     potion("minecraft:long_regeneration", 1), item("farmersdelight:honey_glazed_ham", 1)]))
put("rewards/class_blue", class_bundle(
    [sch("ice", w=3)],
    [item(IS + "ice_rune", 3, 0, (2, 4)), item(IS + "arcane_rune", 1, 0, (1, 2))],
    IS + "ice_upgrade_orb", "cryomancer",
    [ss("glaive"), ss("halberd"), item(IS + "ice_staff"), ek("ranseur"), item("minecraftdungeonsv1:battlestaff")],
    [item(IS + "evasion_elixir", 2), item(IS + "permafrost_shard", 1, 0, (2, 4)), item(IS + "frozen_bone", 1, 0, (1, 3)),
     potion("minecraft:long_fire_resistance", 1), item("galosphere:salted_jerky", 1, 0, (3, 6))]))
put("rewards/class_indigo", class_bundle(
    [scroll(0.3, 0.7, 3, 0, spells=["irons_spellbooks:raise_dead", "irons_spellbooks:summon_vex",
                                     "irons_spellbooks:summon_polar_bear", "irons_spellbooks:summon_horse",
                                     "irons_spellbooks:summon_swords", "alshanex_familiars:summon_shadows"]),
     sch("nature", w=1)],
    [item(IS + "evocation_rune", 2, 0, (2, 3)), item(IS + "nature_rune", 1, 0, (1, 2))],
    IS + "mana_upgrade_orb", "archevoker",
    [ref(GL + "alshanex_trinkets", 3), item("alshanex_familiars:summoner_trinket", 1), item("alshanex_familiars:hunter_trinket", 1)],
    [item("minecraft:lead", 1, 0, (2, 3)), item("minecraft:name_tag", 1, 0, (1, 2)), item("minecraft:bone", 1, 0, (6, 12)),
     item("iceandfire:dragon_meal", 1, 0, (2, 4)), item(IS + "oakskin_elixir", 1)],
    extra=[item("alshanex_familiars:summoner_shard", 1), item("alshanex_familiars:hunter_shard", 1),
           item("alshanex_familiars:druid_shard", 1)]))
put("rewards/class_violet", class_bundle(
    [sch("ender", w=3)],
    [item(IS + "ender_rune", 3, 0, (2, 4)), item(IS + "cooldown_rune", 1, 0, (1, 2))],
    IS + "ender_upgrade_orb", "shadowwalker",
    [ss("sai"), ss("twinblade"), ss("cutlass"), ek("stylet"), item("minecraftdungeonsv1:dagger")],
    [item(IS + "invisibility_elixir", 2), potion("minecraft:long_invisibility", 1), item("minecraft:ender_pearl", 2, 0, (4, 8)),
     item("eternalnether:warped_ender_pearl", 1, 0, (1, 2)), item("artifacts:scarf_of_invisibility", 1)]))

# ---------------------------------------------------------------- write
MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_manifest.json")
if os.path.exists(MANIFEST):  # remove only files this generator wrote last time and no longer writes
    for old in json.load(open(MANIFEST)):
        if old not in FILES:
            fp = os.path.join(OUT, old + ".json")
            if os.path.exists(fp):
                os.remove(fp)
json.dump(sorted(FILES), open(MANIFEST, "w"), indent=0)
for path, data in FILES.items():
    assert path == path.lower(), path
    fp = os.path.join(OUT, path + ".json")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
print("wrote", len(FILES), "tables to", OUT)
