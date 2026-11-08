"""Generator for the Green Lanterns Pufferfish's Skills datapack (puffish_skills 0.19.2, config version 3).

Writes into  server/kubejs/data/greenlanterns/puffish_skills/
Run:  python -I gen_skills.py
"""
import json
import os
import shutil

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'server', 'kubejs', 'data', 'greenlanterns', 'puffish_skills')

CATEGORIES = ['adventurer', 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']

# ---------------------------------------------------------------------------------------------
# Attribute table: key -> (attribute id, operation, label, display format)
#   formats: pct (value*100 %), flat, hearts (value/2), blocks
# ---------------------------------------------------------------------------------------------
MB, ADD = 'multiply_base', 'addition'
ATTR = {
    # Iron's Spells schools / casting
    'fire': ('irons_spellbooks:fire_spell_power', MB, 'Fire Spell Power', 'pct'),
    'blood': ('irons_spellbooks:blood_spell_power', MB, 'Blood Spell Power', 'pct'),
    'nature': ('irons_spellbooks:nature_spell_power', MB, 'Nature (Earth) Spell Power', 'pct'),
    'lightning': ('irons_spellbooks:lightning_spell_power', MB, 'Lightning Spell Power', 'pct'),
    'evocation': ('irons_spellbooks:evocation_spell_power', MB, 'Evocation Spell Power', 'pct'),
    'holy': ('irons_spellbooks:holy_spell_power', MB, 'Holy Spell Power', 'pct'),
    'ice': ('irons_spellbooks:ice_spell_power', MB, 'Ice Spell Power', 'pct'),
    'ender': ('irons_spellbooks:ender_spell_power', MB, 'Ender Spell Power', 'pct'),
    'eldritch': ('irons_spellbooks:eldritch_spell_power', MB, 'Eldritch Spell Power', 'pct'),
    'techno': ('cataclysm_spellbooks:technomancy_spell_power', MB, 'Technomancy Spell Power', 'pct'),
    'spell_power': ('irons_spellbooks:spell_power', MB, 'Spell Power (all schools)', 'pct'),
    'mana': ('irons_spellbooks:max_mana', ADD, 'Max Mana', 'flat'),
    'mana_regen': ('irons_spellbooks:mana_regen', MB, 'Mana Regeneration', 'pct'),
    'cdr': ('irons_spellbooks:cooldown_reduction', MB, 'Spell Cooldown Reduction', 'pct'),
    'cast': ('irons_spellbooks:cast_time_reduction', MB, 'Cast Time Reduction', 'pct'),
    'spell_resist': ('irons_spellbooks:spell_resist', MB, 'Spell Resistance', 'pct'),
    'cast_move': ('irons_spellbooks:casting_movespeed', MB, 'Movement Speed while Casting', 'pct'),
    'summon': ('irons_spellbooks:summon_damage', MB, 'Summon Damage', 'pct'),
    'familiar': ('familiarslib:familiar_damage', MB, 'Familiar Damage', 'pct'),
    'ice_res': ('irons_spellbooks:ice_magic_resist', MB, 'Ice Magic Resistance', 'pct'),
    'lightning_res': ('irons_spellbooks:lightning_magic_resist', MB, 'Lightning Magic Resistance', 'pct'),
    'ender_res': ('irons_spellbooks:ender_magic_resist', MB, 'Ender Magic Resistance', 'pct'),
    'eldritch_res': ('irons_spellbooks:eldritch_magic_resist', MB, 'Eldritch Magic Resistance', 'pct'),
    # Pufferfish's Attributes (dynamic attributes -> multiply_base fractions)
    'melee': ('puffish_attributes:melee_damage', MB, 'Melee Damage', 'pct'),
    'ranged': ('puffish_attributes:ranged_damage', MB, 'Ranged Damage', 'pct'),
    'magic_dmg': ('puffish_attributes:magic_damage', MB, 'Magic Damage', 'pct'),
    'axe': ('puffish_attributes:axe_damage', MB, 'Axe Damage', 'pct'),
    'sword': ('puffish_attributes:sword_damage', MB, 'Sword Damage', 'pct'),
    'mace': ('puffish_attributes:mace_damage', MB, 'Mace Damage', 'pct'),
    'xp': ('puffish_attributes:experience', MB, 'Experience from Orbs', 'pct'),
    'regen': ('puffish_attributes:natural_regeneration', MB, 'Natural Regeneration', 'pct'),
    'healing': ('puffish_attributes:healing', MB, 'Healing Received', 'pct'),
    'resist': ('puffish_attributes:resistance', MB, 'Damage Reduction', 'pct'),
    'melee_res': ('puffish_attributes:melee_resistance', MB, 'Melee Damage Reduction', 'pct'),
    'ranged_res': ('puffish_attributes:ranged_resistance', MB, 'Ranged Damage Reduction', 'pct'),
    'reflect': ('puffish_attributes:damage_reflection', MB, 'Damage Reflection', 'pct'),
    'mining': ('puffish_attributes:mining_speed', MB, 'Mining Speed', 'pct'),
    'pick': ('puffish_attributes:pickaxe_speed', MB, 'Pickaxe Speed', 'pct'),
    'fortune': ('puffish_attributes:fortune', ADD, 'Fortune', 'flat'),
    'mount': ('puffish_attributes:mount_speed', MB, 'Mount Speed', 'pct'),
    'sprint': ('puffish_attributes:sprinting_speed', MB, 'Sprinting Speed', 'pct'),
    'jump': ('puffish_attributes:jump', MB, 'Jump Height', 'pct'),
    'fall_red': ('puffish_attributes:fall_reduction', ADD, 'Fall Damage Reduction', 'blocks'),
    'tamed_dmg': ('puffish_attributes:tamed_damage', MB, 'Pet Damage', 'pct'),
    'tamed_res': ('puffish_attributes:tamed_resistance', MB, 'Pet Damage Reduction', 'pct'),
    'stealth': ('puffish_attributes:stealth', MB, 'Detection Range Reduction', 'pct'),
    'stamina': ('puffish_attributes:stamina', MB, 'Stamina (slower hunger)', 'pct'),
    'xbow_speed': ('puffish_attributes:crossbow_projectile_speed', MB, 'Crossbow Bolt Speed', 'pct'),
    # Vanilla
    'atk_speed': ('minecraft:generic.attack_speed', MB, 'Attack Speed', 'pct'),
    'move': ('minecraft:generic.movement_speed', MB, 'Movement Speed', 'pct'),
    'hp': ('minecraft:generic.max_health', ADD, 'Max Health', 'hearts'),
    'armor': ('minecraft:generic.armor', ADD, 'Armor', 'flat'),
    'tough': ('minecraft:generic.armor_toughness', ADD, 'Armor Toughness', 'flat'),
    'kb_res': ('minecraft:generic.knockback_resistance', ADD, 'Knockback Resistance', 'pct'),
    'luck': ('minecraft:generic.luck', ADD, 'Luck', 'flat'),
    'absorb': ('minecraft:generic.max_absorption', ADD, 'Max Absorption', 'hearts'),
    'burn': ('minecraft:generic.burning_time', MB, 'Burn Duration', 'pct'),
    'safe_fall': ('minecraft:generic.safe_fall_distance', ADD, 'Safe Fall Distance', 'blocks'),
    'step': ('minecraft:generic.step_height', ADD, 'Step Height', 'blocks'),
    'oxygen': ('minecraft:generic.oxygen_bonus', ADD, 'Oxygen Bonus', 'flat'),
    'water_move': ('minecraft:generic.water_movement_efficiency', ADD, 'Water Movement Efficiency', 'pct'),
    'sweep': ('minecraft:player.sweeping_damage_ratio', ADD, 'Sweeping Damage Ratio', 'pct'),
    'reach': ('minecraft:player.block_interaction_range', ADD, 'Block Reach', 'blocks'),
    'ereach': ('minecraft:player.entity_interaction_range', ADD, 'Attack Reach', 'blocks'),
    'break': ('minecraft:player.block_break_speed', MB, 'Block Breaking Speed', 'pct'),
    'sneak': ('minecraft:player.sneaking_speed', ADD, 'Sneaking Speed', 'pct'),
    # Apothic Attributes
    'crit': ('apothic_attributes:crit_chance', ADD, 'Critical Strike Chance', 'pct'),
    'crit_dmg': ('apothic_attributes:crit_damage', ADD, 'Critical Strike Damage', 'pct'),
    'dodge': ('apothic_attributes:dodge_chance', ADD, 'Dodge Chance', 'pct'),
    'lifesteal': ('apothic_attributes:life_steal', ADD, 'Life Steal', 'pct'),
    'overheal': ('apothic_attributes:overheal', ADD, 'Overheal', 'pct'),
    'armor_shred': ('apothic_attributes:armor_shred', ADD, 'Armor Shred', 'pct'),
    'armor_pierce': ('apothic_attributes:armor_pierce', ADD, 'Armor Pierce', 'flat'),
    'fire_dmg': ('apothic_attributes:fire_damage', ADD, 'Bonus Fire Damage per Hit', 'flat'),
    'cold_dmg': ('apothic_attributes:cold_damage', ADD, 'Bonus Cold Damage per Hit', 'flat'),
    'draw': ('apothic_attributes:draw_speed', ADD, 'Bow Draw Speed', 'pct'),
    'arrow_dmg': ('apothic_attributes:arrow_damage', ADD, 'Arrow Damage', 'pct'),
    'arrow_vel': ('apothic_attributes:arrow_velocity', ADD, 'Arrow Velocity', 'pct'),
    # Other mods
    'roll': ('combat_roll:count', ADD, 'Combat Roll Charge', 'flat'),
    'roll_dist': ('combat_roll:distance', ADD, 'Combat Roll Distance', 'blocks'),
    'ultimine': ('ftbultimine:max_blocks_modifier', ADD, 'Ultimine Max Blocks', 'flat'),
}

# Default icon per attribute key (items unless prefixed with "effect:")
ICON = {
    'fire': 'irons_spellbooks:fire_rune', 'blood': 'irons_spellbooks:blood_rune',
    'nature': 'irons_spellbooks:nature_rune', 'lightning': 'irons_spellbooks:lightning_rune',
    'evocation': 'irons_spellbooks:evocation_rune', 'holy': 'irons_spellbooks:holy_rune',
    'ice': 'irons_spellbooks:ice_rune', 'ender': 'irons_spellbooks:ender_rune',
    'eldritch': 'irons_spellbooks:eldritch_manuscript', 'techno': 'cataclysm_spellbooks:technomancy_upgrade_orb',
    'spell_power': 'irons_spellbooks:arcane_essence', 'mana': 'irons_spellbooks:mana_upgrade_orb',
    'mana_regen': 'irons_spellbooks:mana_ring', 'cdr': 'irons_spellbooks:cooldown_upgrade_orb',
    'cast': 'irons_spellbooks:cast_time_ring', 'spell_resist': 'irons_spellbooks:protection_rune',
    'cast_move': 'irons_spellbooks:speed_boots', 'summon': 'irons_spellbooks:conjurers_talisman',
    'familiar': 'alshanex_familiars:summoner_trinket', 'ice_res': 'irons_spellbooks:frostward_ring',
    'lightning_res': 'irons_spellbooks:protection_upgrade_orb', 'ender_res': 'irons_spellbooks:protection_upgrade_orb',
    'eldritch_res': 'irons_spellbooks:protection_upgrade_orb',
    'melee': 'minecraft:iron_sword', 'ranged': 'minecraft:bow', 'magic_dmg': 'minecraft:amethyst_shard',
    'axe': 'minecraft:iron_axe', 'sword': 'minecraft:diamond_sword', 'mace': 'minecraft:mace',
    'xp': 'minecraft:experience_bottle', 'regen': 'effect:minecraft:regeneration',
    'healing': 'minecraft:glistering_melon_slice', 'resist': 'effect:minecraft:resistance',
    'melee_res': 'minecraft:shield', 'ranged_res': 'minecraft:turtle_helmet', 'reflect': 'minecraft:cactus',
    'mining': 'minecraft:iron_pickaxe', 'pick': 'minecraft:diamond_pickaxe', 'fortune': 'minecraft:diamond',
    'mount': 'minecraft:saddle', 'sprint': 'minecraft:rabbit_foot', 'jump': 'minecraft:slime_ball',
    'fall_red': 'minecraft:hay_block', 'tamed_dmg': 'minecraft:bone', 'tamed_res': 'minecraft:wolf_armor',
    'stealth': 'effect:minecraft:invisibility', 'stamina': 'minecraft:bread', 'xbow_speed': 'minecraft:crossbow',
    'atk_speed': 'minecraft:golden_sword', 'move': 'minecraft:sugar', 'hp': 'effect:minecraft:health_boost',
    'armor': 'minecraft:iron_chestplate', 'tough': 'minecraft:netherite_chestplate', 'kb_res': 'minecraft:anvil',
    'luck': 'effect:minecraft:luck', 'absorb': 'effect:minecraft:absorption', 'burn': 'minecraft:magma_cream',
    'safe_fall': 'minecraft:feather', 'step': 'minecraft:oak_stairs', 'oxygen': 'minecraft:heart_of_the_sea',
    'water_move': 'minecraft:prismarine_shard', 'sweep': 'minecraft:diamond_axe', 'reach': 'create:extendo_grip',
    'ereach': 'minecraft:lead', 'break': 'minecraft:golden_pickaxe', 'sneak': 'minecraft:leather_boots',
    'crit': 'minecraft:target', 'crit_dmg': 'minecraft:netherite_sword', 'dodge': 'minecraft:phantom_membrane',
    'lifesteal': 'irons_spellbooks:blood_vial', 'overheal': 'minecraft:golden_apple', 'armor_shred': 'minecraft:flint',
    'armor_pierce': 'minecraft:arrow', 'fire_dmg': 'minecraft:blaze_powder', 'cold_dmg': 'minecraft:packed_ice',
    'draw': 'minecraft:string', 'arrow_dmg': 'minecraft:arrow', 'arrow_vel': 'minecraft:spectral_arrow',
    'roll': 'minecraft:rabbit_hide', 'roll_dist': 'minecraft:rabbit_hide', 'ultimine': 'minecraft:netherite_pickaxe',
    'powder_snow': 'minecraft:powder_snow_bucket',
}

# Special non-attribute rewards
SPECIAL = {
    'powder_snow': ({'type': 'puffish_skills:tag', 'data': {'tag': 'walk_on_powder_snow'}},
                    'Walk on Powder Snow'),
}


def fmt_num(v):
    s = ('%.2f' % v).rstrip('0').rstrip('.')
    return s


def describe(key, value):
    if key in SPECIAL:
        return SPECIAL[key][1]
    _, _, label, kind = ATTR[key]
    sign = '+' if value >= 0 else '-'
    a = abs(value)
    if kind == 'pct':
        return '%s%s%% %s' % (sign, fmt_num(a * 100), label)
    if kind == 'hearts':
        h = a / 2
        return '%s%s %s (%s %s)' % (sign, fmt_num(h), 'Heart' if h == 1 else 'Hearts', label, fmt_num(a) + ' HP')
    if kind == 'blocks':
        return '%s%s %s' % (sign, fmt_num(a), label + (' (blocks)' if 'Reach' not in label else ''))
    return '%s%s %s' % (sign, fmt_num(a), label)


def reward(key, value):
    if key in SPECIAL:
        return SPECIAL[key][0]
    attr, op, _, _ = ATTR[key]
    return {'type': 'puffish_skills:attribute', 'data': {'attribute': attr, 'value': value, 'operation': op}}


def icon_obj(icon):
    if icon.startswith('effect:'):
        return {'type': 'effect', 'data': {'effect': icon[len('effect:'):]}}
    return {'type': 'item', 'data': {'item': icon}}


FRAME = {'task': {'type': 'advancement', 'data': {'frame': 'task'}},
         'goal': {'type': 'advancement', 'data': {'frame': 'goal'}},
         'challenge': {'type': 'advancement', 'data': {'frame': 'challenge'}}}

# ---------------------------------------------------------------------------------------------
# Tree layout templates
# ---------------------------------------------------------------------------------------------
# Class branch: 11 nodes. (slot, dx, row, frame, cost)
CLASS_BRANCH = [
    ('a1', 0, 0, 'task', 1),
    ('a2', 0, 1, 'task', 1),
    ('b1', -1, 2, 'task', 1), ('b2', 1, 2, 'task', 1),
    ('b3', -1, 3, 'task', 1), ('b4', 1, 3, 'task', 1),
    ('a3', 0, 4, 'goal', 2),
    ('c1', -1, 5, 'task', 1), ('c2', 1, 5, 'task', 1),
    ('a4', 0, 6, 'goal', 2),
    ('cap', 0, 7, 'challenge', 5),
]
CLASS_LINKS = [('a1', 'a2'), ('a2', 'b1'), ('a2', 'b2'), ('b1', 'b3'), ('b2', 'b4'), ('b3', 'a3'), ('b4', 'a3'),
               ('a3', 'c1'), ('a3', 'c2'), ('c1', 'a4'), ('c2', 'a4'), ('a4', 'cap')]
# Adventurer branch: 7 nodes
ADV_BRANCH = [
    ('a1', 0, 0, 'task', 1),
    ('b1', -1, 1, 'task', 1), ('b2', 1, 1, 'task', 1),
    ('a2', 0, 2, 'goal', 2),
    ('c1', -1, 3, 'task', 1), ('c2', 1, 3, 'task', 1),
    ('cap', 0, 4, 'challenge', 4),
]
ADV_LINKS = [('a1', 'b1'), ('a1', 'b2'), ('b1', 'a2'), ('b2', 'a2'), ('a2', 'c1'), ('a2', 'c2'), ('c1', 'cap'),
             ('c2', 'cap')]

BRANCH_X = [-170, 0, 170]   # element, style, aspect
FORK_DX = 34
ROW_DY = 42
ROOT_Y = 56
CAP_REQUIRED_SPENT = 25

# ---------------------------------------------------------------------------------------------
# Tree content. Each node: slot -> (title, [(attr_key, value), ...], icon override or None)
# ---------------------------------------------------------------------------------------------
TREES = {}

TREES['red'] = {
    'root': ('Ember of Rage', [('melee', 0.02), ('fire', 0.02)], 'createlanterns:red_power_ring'),
    'branches': [
        ('Fire & Blood', {
            'a1': ('Kindling I', [('fire', 0.03)], None),
            'a2': ('Ember Well', [('mana', 15)], None),
            'b1': ('Kindling II', [('fire', 0.03)], None),
            'b2': ('Bloodletting I', [('blood', 0.04)], None),
            'b3': ('Quickfire', [('cast', 0.03)], None),
            'b4': ('Bloodletting II', [('blood', 0.04)], None),
            'a3': ('Kindled Soul', [('fire', 0.05), ('mana', 15)], 'irons_spellbooks:fire_upgrade_orb'),
            'c1': ('Searing Focus', [('cdr', 0.03)], None),
            'c2': ('Smoulder', [('mana_regen', 0.05)], None),
            'a4': ('Pyre Heart', [('fire', 0.05), ('blood', 0.05)], 'irons_spellbooks:blood_upgrade_orb'),
            'cap': ('Hellfire Conduit', [('fire', 0.10), ('fire_dmg', 1.0), ('cdr', 0.05)], 'irons_spellbooks:pyrium_staff'),
        }),
        ('Two-Handed Fury', {
            'a1': ('Heavy Hands', [('melee', 0.03)], None),
            'a2': ('Thick Blood', [('hp', 2)], None),
            'b1': ('Cleaver', [('axe', 0.05)], None),
            'b2': ('Whirlwind', [('atk_speed', 0.02)], None),
            'b3': ('Brutal Strikes', [('crit_dmg', 0.06)], None),
            'b4': ('Momentum', [('melee', 0.03)], 'minecraft:netherite_axe'),
            'a3': ('Wide Arc', [('sweep', 0.10), ('melee', 0.03)], 'simplyswords:iron_claymore'),
            'c1': ('Scarred Hide', [('hp', 2)], None),
            'c2': ('Sunder', [('armor_shred', 0.03)], None),
            'a4': ('Blood Frenzy', [('lifesteal', 0.02), ('atk_speed', 0.02)], None),
            'cap': ('Unstoppable Rage', [('melee', 0.08), ('crit_dmg', 0.12), ('kb_res', 0.15)], 'simplyswords:netherite_greataxe'),
        }),
        ('Ash & Inferno', {
            'a1': ('Ashen Skin', [('burn', -0.10)], None),
            'a2': ('Second Wind', [('regen', 0.05)], None),
            'b1': ('Hoarded Fury', [('absorb', 2)], None),
            'b2': ('Flame Brand', [('fire_dmg', 0.5)], None),
            'b3': ('Overflowing Rage', [('overheal', 0.05)], None),
            'b4': ('Rooted Stance', [('kb_res', 0.05)], None),
            'a3': ('Ashwalker', [('burn', -0.15), ('resist', 0.02)], 'minecraft:netherrack'),
            'c1': ('Dragon Rider', [('mount', 0.05)], None),
            'c2': ('Hot Blood', [('regen', 0.05)], None),
            'a4': ('Dragonkin', [('mount', 0.05), ('hp', 2)], 'minecraft:dragon_head'),
            'cap': ('Phoenix Blood', [('lifesteal', 0.03), ('overheal', 0.10), ('burn', -0.25)], 'minecraft:totem_of_undying'),
        }),
    ],
}

TREES['orange'] = {
    'root': ('Heart of the Mountain', [('armor', 1)], 'createlanterns:orange_power_ring'),
    'branches': [
        ('Earthshaper', {
            'a1': ('Stone Whisper I', [('nature', 0.03)], None),
            'a2': ('Deep Reserves', [('mana', 15)], None),
            'b1': ('Stone Whisper II', [('nature', 0.03)], None),
            'b2': ('Granite Will', [('spell_resist', 0.03)], None),
            'b3': ('Tremor Cadence', [('cast', 0.03)], None),
            'b4': ('Bedrock Mind', [('spell_resist', 0.03)], None),
            'a3': ('Stoneblood', [('nature', 0.05), ('mana', 15)], 'irons_spellbooks:nature_upgrade_orb'),
            'c1': ('Patient Earth', [('cdr', 0.03)], None),
            'c2': ('Mossgrowth', [('mana_regen', 0.05)], None),
            'a4': ('Living Mountain', [('nature', 0.05), ('spell_resist', 0.04)], 'minecraft:mossy_cobblestone'),
            'cap': ('Tectonic Will', [('nature', 0.10), ('cdr', 0.05), ('mana', 25)], 'minecraft:heavy_core'),
        }),
        ('Bulwark', {
            'a1': ('Plated', [('armor', 1)], None),
            'a2': ('Broad Shoulders', [('hp', 2)], None),
            'b1': ('Tempered Steel', [('tough', 1)], None),
            'b2': ('Immovable', [('kb_res', 0.05)], None),
            'b3': ('Shield Wall', [('melee_res', 0.03)], None),
            'b4': ('Crushing Blows', [('mace', 0.05)], None),
            'a3': ('Bulwark', [('armor', 2), ('hp', 2)], 'minecraft:iron_block'),
            'c1': ('Thorned Plate', [('reflect', 0.05)], None),
            'c2': ('Arrow Ward', [('ranged_res', 0.03)], None),
            'a4': ('Iron Hide', [('tough', 1), ('resist', 0.02)], 'minecraft:netherite_chestplate'),
            'cap': ('Unbreakable', [('armor', 3), ('hp', 4), ('kb_res', 0.15), ('resist', 0.03)], 'minecraft:obsidian'),
        }),
        ('Hoard & Delve', {
            'a1': ("Prospector's Grip", [('mining', 0.05)], None),
            'a2': ('Glint Sense', [('luck', 0.5)], None),
            'b1': ('Deep Delver', [('pick', 0.06)], None),
            'b2': ('Lucky Strike', [('fortune', 0.15)], None),
            'b3': ('Vein Seeker', [('ultimine', 8)], None),
            'b4': ('Treasure Nose', [('luck', 0.5)], 'minecraft:gold_nugget'),
            'a3': ('Motherlode', [('fortune', 0.20), ('mining', 0.05)], 'minecraft:raw_gold'),
            'c1': ('Long Reach', [('reach', 0.5)], None),
            'c2': ("Hoarder's Greed", [('xp', 0.05)], None),
            'a4': ("Dragon's Hoard", [('luck', 0.5), ('ultimine', 8)], 'minecraft:gold_block'),
            'cap': ('Mine, All Mine', [('fortune', 0.40), ('luck', 0.5), ('mining', 0.10)], 'minecraft:diamond_block'),
        }),
    ],
}

TREES['yellow'] = {
    'root': ('Spark of the Storm', [('move', 0.02)], 'createlanterns:yellow_power_ring'),
    'branches': [
        ('Stormcalling', {
            'a1': ('Static I', [('lightning', 0.03)], None),
            'a2': ('Capacitor', [('mana', 15)], None),
            'b1': ('Static II', [('lightning', 0.03)], None),
            'b2': ('Circuitry I', [('techno', 0.04)], None),
            'b3': ('Quick Charge', [('cast', 0.03)], None),
            'b4': ('Circuitry II', [('techno', 0.04)], 'create:precision_mechanism'),
            'a3': ('Static Charge', [('lightning', 0.05), ('cast_move', 0.05)], 'irons_spellbooks:lightning_upgrade_orb'),
            'c1': ('Discharge', [('cdr', 0.03)], None),
            'c2': ('Dynamo', [('mana_regen', 0.05)], None),
            'a4': ('Overclock', [('lightning', 0.05), ('techno', 0.05)], 'irons_spellbooks:energized_core'),
            'cap': ('Living Storm', [('lightning', 0.10), ('cast', 0.05), ('cdr', 0.05)], 'minecraft:lightning_rod'),
        }),
        ('Duelist', {
            'a1': ('Quick Hands', [('atk_speed', 0.03)], None),
            'a2': ('Fleet Foot', [('move', 0.02)], None),
            'b1': ('Precision', [('crit', 0.02)], None),
            'b2': ('Sidestep', [('dodge', 0.01)], None),
            'b3': ('Fencer', [('sword', 0.04)], 'simplyswords:iron_rapier'),
            'b4': ('Blur', [('dodge', 0.01)], None),
            'a3': ('Lightning Reflexes', [('crit', 0.02), ('atk_speed', 0.02)], 'simplyswords:diamond_katana'),
            'c1': ('Tumble', [('roll_dist', 0.5)], None),
            'c2': ('Sprinter', [('sprint', 0.04)], None),
            'a4': ('Thunderstep', [('move', 0.03), ('dodge', 0.01)], 'irons_spellbooks:speed_boots'),
            'cap': ('Faster Than Thunder', [('roll', 1), ('crit', 0.03), ('atk_speed', 0.04)], 'simplyswords:netherite_rapier'),
        }),
        ('Artificer', {
            'a1': ('Tinkerer', [('break', 0.05)], 'create:wrench'),
            'a2': ('Long Arm', [('reach', 0.5)], None),
            'b1': ('Soft Landing', [('safe_fall', 1)], None),
            'b2': ('Lineman', [('ereach', 0.25)], None),
            'b3': ('Stair Climber', [('step', 0.5)], None),
            'b4': ('Grounded', [('lightning_res', 0.05)], 'minecraft:copper_block'),
            'a3': ("Engineer's Eye", [('reach', 0.5), ('break', 0.05)], 'create:goggles'),
            'c1': ('Sturdy Frame', [('hp', 2)], None),
            'c2': ('Insulated', [('lightning_res', 0.05)], None),
            'a4': ('Aviator', [('safe_fall', 2), ('kb_res', 0.05)], 'aeronautics:aviators_goggles'),
            'cap': ('Storm Engine', [('reach', 1.0), ('ereach', 0.5), ('move', 0.03)], 'create:mechanical_arm'),
        }),
    ],
}

TREES['green'] = {
    'root': ('Oath of Light', [('hp', 2)], 'createlanterns:power_ring'),
    'branches': [
        ('Evocation & Grace', {
            'a1': ('Warding Words I', [('evocation', 0.03)], None),
            'a2': ('Deep Faith', [('mana', 15)], None),
            'b1': ('Warding Words II', [('evocation', 0.03)], None),
            'b2': ('Blessing I', [('holy', 0.04)], None),
            'b3': ('Swift Litany', [('cast', 0.03)], None),
            'b4': ('Blessing II', [('holy', 0.04)], None),
            'a3': ('Oathbound Magic', [('evocation', 0.05), ('mana', 15)], 'irons_spellbooks:evocation_upgrade_orb'),
            'c1': ('Steadfast Prayer', [('cdr', 0.03)], None),
            'c2': ('Wellspring', [('mana_regen', 0.05)], None),
            'a4': ('Radiance', [('evocation', 0.05), ('holy', 0.05)], 'irons_spellbooks:holy_upgrade_orb'),
            'cap': ('In Brightest Day', [('evocation', 0.10), ('holy', 0.05), ('cdr', 0.05)], 'minecraft:beacon'),
        }),
        ('Paladin', {
            'a1': ("Squire's Mail", [('armor', 1)], 'minecraft:chainmail_chestplate'),
            'a2': ('Oathblade', [('sword', 0.04)], None),
            'b1': ('Stout Heart', [('hp', 2)], None),
            'b2': ('Tempered Plate', [('tough', 0.5)], None),
            'b3': ('Righteous Blows', [('melee', 0.03)], None),
            'b4': ('Hold the Line', [('kb_res', 0.05)], None),
            'a3': ('Shieldwall', [('armor', 1), ('melee_res', 0.03)], 'minecraft:shield'),
            'c1': ('Smite', [('crit_dmg', 0.05)], None),
            'c2': ('Vigil', [('hp', 2)], None),
            'a4': ('Holy Avenger', [('sword', 0.04), ('armor', 1)], 'irons_spellbooks:paladin_chestplate'),
            'cap': ("Lightwarden's Vow", [('hp', 4), ('armor', 2), ('resist', 0.03)], 'minecraft:enchanted_golden_apple'),
        }),
        ('Warden of the Village', {
            'a1': ('Mending Touch', [('healing', 0.05)], None),
            'a2': ('Hearth Rest', [('regen', 0.05)], 'minecraft:campfire'),
            'b1': ('Field Medic', [('healing', 0.05)], 'irons_spellbooks:greater_healing_potion'),
            'b2': ('Sanctuary', [('absorb', 2)], None),
            'b3': ('Overflowing Grace', [('overheal', 0.05)], None),
            'b4': ('Spellward', [('spell_resist', 0.03)], None),
            'a3': ('Hearthguard', [('healing', 0.05), ('regen', 0.05)], 'minecraft:bell'),
            'c1': ('Warhorse', [('mount', 0.05)], 'minecraft:diamond_horse_armor'),
            'c2': ('Town Guard', [('hp', 2)], None),
            'a4': ('Hero of the Village', [('luck', 0.5), ('healing', 0.05), ('mount', 0.05)], 'minecraft:emerald'),
            'cap': ('Beacon of Hope', [('healing', 0.10), ('overheal', 0.10), ('absorb', 4)], 'minecraft:totem_of_undying'),
        }),
    ],
}

TREES['blue'] = {
    'root': ('First Frost', [('ice', 0.02)], 'createlanterns:blue_power_ring'),
    'branches': [
        ('Frostbinding', {
            'a1': ('Rime I', [('ice', 0.03)], None),
            'a2': ('Glacier Well', [('mana', 15)], None),
            'b1': ('Rime II', [('ice', 0.03)], None),
            'b2': ('Meltwater', [('mana_regen', 0.05)], None),
            'b3': ('Cold Snap', [('cast', 0.03)], None),
            'b4': ('Frozen Reserve', [('mana', 15)], None),
            'a3': ('Rime Heart', [('ice', 0.05), ('mana', 15)], 'irons_spellbooks:ice_upgrade_orb'),
            'c1': ('Frozen Patience', [('cdr', 0.03)], None),
            'c2': ('Arcane Lattice', [('spell_power', 0.02)], None),
            'a4': ('Glacial Focus', [('ice', 0.05), ('mana_regen', 0.05)], 'irons_spellbooks:permafrost_shard'),
            'cap': ("Winter's Embrace", [('ice', 0.10), ('cdr', 0.05), ('mana', 25)], 'irons_spellbooks:ice_staff'),
        }),
        ('Battlemage', {
            'a1': ("Spellsword's Edge", [('melee', 0.03)], None),
            'a2': ('Frost Mail', [('armor', 1)], None),
            'b1': ('Chilling Strikes', [('cold_dmg', 0.5)], None),
            'b2': ('Hardy', [('hp', 2)], None),
            'b3': ('Arcane Edge', [('magic_dmg', 0.03)], None),
            'b4': ('Ice Plate', [('tough', 0.5)], None),
            'a3': ('Frostblade', [('cold_dmg', 0.5), ('melee', 0.03)], 'irons_spellbooks:boreal_blade'),
            'c1': ('Glint of Ice', [('crit', 0.02)], None),
            'c2': ('Battle Casting', [('cast_move', 0.05)], None),
            'a4': ('Spellsword', [('spell_power', 0.03), ('atk_speed', 0.02)], 'irons_spellbooks:frosted_helve'),
            'cap': ('Frozen Edge', [('cold_dmg', 1.0), ('melee', 0.05), ('armor', 2)], 'minecraft:blue_ice'),
        }),
        ('Skyward Wanderer', {
            'a1': ('Winter Blood', [('ice_res', 0.05)], None),
            'a2': ("Wanderer's Pace", [('move', 0.02)], None),
            'b1': ('Featherfall', [('safe_fall', 1)], None),
            'b2': ('Dragon Bond', [('mount', 0.05)], None),
            'b3': ('Updraft', [('jump', 0.05)], None),
            'b4': ('Wind Rider', [('mount', 0.05)], 'minecraft:elytra'),
            'a3': ('Snowstrider', [('powder_snow', 0), ('move', 0.02)], 'minecraft:powder_snow_bucket'),
            'c1': ("Sky Pilgrim's Luck", [('luck', 0.5)], None),
            'c2': ('Hearthless Warmth', [('regen', 0.05)], None),
            'a4': ('Sky Wanderer', [('safe_fall', 2), ('mount', 0.05)], 'minecraft:phantom_membrane'),
            'cap': ('Heart of Winter', [('ice_res', 0.10), ('move', 0.03), ('luck', 0.5), ('mount', 0.05)], 'minecraft:heart_of_the_sea'),
        }),
    ],
}

TREES['indigo'] = {
    'root': ('Call of the Wild', [('tamed_dmg', 0.03)], 'createlanterns:indigo_power_ring'),
    'branches': [
        ('Summoner', {
            'a1': ('Conjurer I', [('summon', 0.04)], None),
            'a2': ('Spirit Reserve', [('mana', 15)], None),
            'b1': ('Conjurer II', [('summon', 0.04)], None),
            'b2': ('Familiar Bond I', [('familiar', 0.05)], None),
            'b3': ('Quick Call', [('cdr', 0.03)], None),
            'b4': ('Familiar Bond II', [('familiar', 0.05)], 'alshanex_familiars:familiar_tome'),
            'a3': ('Pack Call', [('summon', 0.06), ('mana', 15)], 'irons_spellbooks:greater_conjurers_talisman'),
            'c1': ('Swift Summons', [('cast', 0.03)], None),
            'c2': ('Wild Spring', [('mana_regen', 0.05)], None),
            'a4': ('Kindred Spirits', [('summon', 0.06), ('familiar', 0.05)], 'alshanex_familiars:summoner_shard'),
            'cap': ('Lord of the Wild', [('summon', 0.12), ('cdr', 0.05), ('mana', 25)], 'irons_spellbooks:necronomicon_spell_book'),
        }),
        ('Ranger', {
            'a1': ('Keen Eye', [('ranged', 0.03)], None),
            'a2': ('Quick Draw', [('draw', 0.05)], None),
            'b1': ('Broadheads', [('arrow_dmg', 0.05)], None),
            'b2': ('Bolt Thrower', [('xbow_speed', 0.05)], None),
            'b3': ('Flight Feathers', [('arrow_vel', 0.05)], None),
            'b4': ('Steady Aim', [('ranged', 0.03)], None),
            'a3': ("Hunter's Mark", [('crit', 0.02), ('ranged', 0.03)], 'minecraft:target'),
            'c1': ('Light Step', [('move', 0.02)], None),
            'c2': ('Evasive Hunter', [('dodge', 0.01)], None),
            'a4': ('Deadeye', [('arrow_dmg', 0.05), ('draw', 0.05)], 'irons_spellbooks:autoloader_crossbow'),
            'cap': ('Alpha Predator', [('ranged', 0.06), ('crit_dmg', 0.10), ('move', 0.03)], 'minecraft:spyglass'),
        }),
        ('Beastheart', {
            'a1': ('Pack Leader', [('tamed_dmg', 0.04)], None),
            'a2': ('Guardian Bond', [('tamed_res', 0.04)], None),
            'b1': ('Trail Rider', [('mount', 0.05)], None),
            'b2': ('Fangs', [('tamed_dmg', 0.04)], None),
            'b3': ('Long Ride', [('mount', 0.05)], 'minecraft:golden_carrot'),
            'b4': ('Thick Fur', [('tamed_res', 0.04)], None),
            'a3': ('Bond of Trust', [('tamed_dmg', 0.05), ('tamed_res', 0.05)], 'minecraft:lead'),
            'c1': ('Farmhand', [('regen', 0.05)], 'minecraft:wheat'),
            'c2': ('Green Thumb', [('luck', 0.5)], None),
            'a4': ('Harvest Moon', [('stamina', 0.10), ('tamed_dmg', 0.05)], 'minecraft:hay_block'),
            'cap': ('Heart of the Pack', [('tamed_dmg', 0.10), ('tamed_res', 0.10), ('mount', 0.05)], 'minecraft:sniffer_egg'),
        }),
    ],
}

TREES['violet'] = {
    'root': ('Touch of the Void', [('crit', 0.01)], 'createlanterns:violet_power_ring'),
    'branches': [
        ('Voidweaving', {
            'a1': ('Umbral I', [('ender', 0.03)], None),
            'a2': ('Hollow Reserve', [('mana', 15)], None),
            'b1': ('Umbral II', [('ender', 0.03)], None),
            'b2': ('Whispers I', [('eldritch', 0.04)], None),
            'b3': ('Blink Cadence', [('cast', 0.03)], None),
            'b4': ('Whispers II', [('eldritch', 0.04)], 'minecraft:echo_shard'),
            'a3': ('Void Touched', [('ender', 0.05), ('mana', 15)], 'irons_spellbooks:ender_upgrade_orb'),
            'c1': ('Patient Shadow', [('cdr', 0.03)], None),
            'c2': ('Night Tide', [('mana_regen', 0.05)], None),
            'a4': ('Abyssal Gaze', [('ender', 0.05), ('eldritch', 0.05)], 'minecraft:ender_eye'),
            'cap': ('Event Horizon', [('ender', 0.10), ('eldritch', 0.05), ('cdr', 0.05)], 'minecraft:dragon_egg'),
        }),
        ('Assassin', {
            'a1': ('Find the Gap', [('crit', 0.02)], None),
            'a2': ('Quick Knives', [('atk_speed', 0.02)], 'minecraftdungeonsv1:dagger'),
            'b1': ('Cruel Edge', [('crit_dmg', 0.06)], None),
            'b2': ('Slip Away', [('dodge', 0.01)], None),
            'b3': ('Through the Seams', [('armor_pierce', 1)], None),
            'b4': ('Light Feet', [('move', 0.02)], None),
            'a3': ('Backstab', [('crit_dmg', 0.08), ('crit', 0.02)], 'graveyard:bone_dagger'),
            'c1': ('Blood Price', [('lifesteal', 0.01)], None),
            'c2': ('Phantom Step', [('dodge', 0.01)], None),
            'a4': ('Shadowstep', [('roll_dist', 0.5), ('move', 0.02)], 'irons_spellbooks:shadowwalker_boots'),
            'cap': ('Death from Nowhere', [('crit', 0.03), ('crit_dmg', 0.15), ('roll', 1)], 'minecraft:wither_skeleton_skull'),
        }),
        ('Nightstalker', {
            'a1': ('Hush', [('stealth', 0.05)], None),
            'a2': ('Soft Steps', [('sneak', 0.05)], None),
            'b1': ('Void Ward', [('ender_res', 0.05)], None),
            'b2': ('Shadow Blend', [('stealth', 0.05)], None),
            'b3': ('Eldritch Ward', [('eldritch_res', 0.05)], None),
            'b4': ("Cat's Landing", [('fall_red', 1)], None),
            'a3': ('Nightwalker', [('stealth', 0.05), ('sneak', 0.05)], 'minecraft:black_candle'),
            'c1': ('Grave Grit', [('hp', 2)], None),
            'c2': ('Grave Robber', [('luck', 0.5)], 'minecraft:skeleton_skull'),
            'a4': ('Undying Shade', [('stealth', 0.05), ('hp', 2)], 'minecraft:crying_obsidian'),
            'cap': ('One with the Void', [('stealth', 0.10), ('sneak', 0.10), ('dodge', 0.02)], 'minecraft:ender_pearl'),
        }),
    ],
}

TREES['adventurer'] = {
    'root': ("Wanderer's Resolve", [('hp', 2)], 'minecraft:compass'),
    'branches': [
        ('Vitality', {
            'a1': ('Tough Skin', [('hp', 2)], None),
            'b1': ('Padded Gear', [('armor', 1)], 'minecraft:leather_chestplate'),
            'b2': ('Quick Recovery', [('regen', 0.05)], None),
            'a2': ('Hardened', [('hp', 2), ('tough', 0.5)], 'minecraft:iron_chestplate'),
            'c1': ('Sure Footing', [('kb_res', 0.05)], None),
            'c2': ('Second Breath', [('regen', 0.05)], None),
            'cap': ('Seasoned Survivor', [('hp', 2), ('armor', 1), ('tough', 0.5)], 'minecraft:golden_apple'),
        }),
        ('Wayfarer', {
            'a1': ('Brisk Pace', [('move', 0.02)], None),
            'b1': ('Spring Step', [('jump', 0.05)], None),
            'b2': ('Light Landing', [('safe_fall', 1)], None),
            'a2': ('Roadwise', [('move', 0.02), ('sprint', 0.03)], 'minecraft:leather_boots'),
            'c1': ('Strong Swimmer', [('water_move', 0.15)], None),
            'c2': ('Rider', [('mount', 0.05)], None),
            'cap': ('Pathfinder', [('move', 0.03), ('safe_fall', 2), ('oxygen', 1)], 'minecraft:filled_map'),
        }),
        ('Fortune', {
            'a1': ('Lucky Find', [('luck', 0.25)], None),
            'b1': ('Quick Study', [('xp', 0.05)], None),
            'b2': ('Four-Leaf', [('luck', 0.25)], 'minecraft:rabbit_foot'),
            'a2': ('Fortune Smiles', [('luck', 0.5), ('break', 0.05)], 'minecraft:emerald'),
            'c1': ('Practiced Hands', [('mining', 0.05)], None),
            'c2': ('Charmed', [('luck', 0.25)], 'minecraft:gold_nugget'),
            'cap': ("Fortune's Favourite", [('luck', 0.75), ('xp', 0.10)], 'minecraft:emerald_block'),
        }),
    ],
}

# ---------------------------------------------------------------------------------------------
# Category meta
# ---------------------------------------------------------------------------------------------
META = {
    'adventurer': dict(title='Adventurer', color='#d8c27a', icon='minecraft:compass',
                       desc='Every hero walks this road. Grows from every fight, every boss and every mile travelled.',
                       bg='minecraft:textures/gui/advancements/backgrounds/adventure.png', unlocked=True),
    'red': dict(title='Red Lantern · Bloodfire Berserker', color='#e8452c', icon='createlanterns:red_power_ring',
                desc='Rage. Fire and Blood magic, two-handed fury, the Nether.',
                bg='minecraft:textures/gui/advancements/backgrounds/nether.png', unlocked=False),
    'orange': dict(title='Orange Lantern · Hoardwarden', color='#f39c34', icon='createlanterns:orange_power_ring',
                   desc='Avarice. Earth magic, the heavy knight, mines and treasure.',
                   bg='minecraft:textures/gui/advancements/backgrounds/stone.png', unlocked=False),
    'yellow': dict(title='Yellow Lantern · Stormwright', color='#f4d03f', icon='createlanterns:yellow_power_ring',
                   desc='Fear. Lightning and Technomancy, the speed duelist, machines and airships.',
                   bg='minecraft:textures/block/cut_copper.png', unlocked=False),
    'green': dict(title='Green Lantern · Lightwarden', color='#3ec24a', icon='createlanterns:power_ring',
                  desc='Will. Evocation and Holy magic, the paladin, villages and raids.',
                  bg='minecraft:textures/block/mossy_stone_bricks.png', unlocked=False),
    'blue': dict(title='Blue Lantern · Frostbinder', color='#4aa3ff', icon='createlanterns:blue_power_ring',
                 desc='Hope. Ice magic, the battlemage, frozen lands and the sky.',
                 bg='minecraft:textures/block/packed_ice.png', unlocked=False),
    'indigo': dict(title='Indigo Lantern · Wildheart', color='#5b5bd6', icon='createlanterns:indigo_power_ring',
                   desc='Compassion. Summoning, the ranger, beasts, breeding and farms.',
                   bg='minecraft:textures/gui/advancements/backgrounds/husbandry.png', unlocked=False),
    'violet': dict(title='Violet Lantern · Voidblade', color='#a64ad8', icon='createlanterns:violet_power_ring',
                   desc='Love, turned to the void. Ender and Eldritch magic, the assassin, night and undead.',
                   bg='minecraft:textures/gui/advancements/backgrounds/end.png', unlocked=False),
}

CLASS_LEVEL_LIMIT = 50
CLASS_SPENT_LIMIT = 45
CLASS_CURVE = '60 + 22 * level + 1.0 * level ^ 2'
ADV_LEVEL_LIMIT = 40
ADV_CURVE = '50 + 20 * level + 0.9 * level ^ 2'


def shade(hex_color, f):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if f >= 0:
        r, g, b = [int(c + (255 - c) * f) for c in (r, g, b)]
    else:
        r, g, b = [int(c * (1 + f)) for c in (r, g, b)]
    return '#%02x%02x%02x' % (r, g, b)


def category_json(cat):
    m = META[cat]
    c = m['color']
    d = {
        'title': {'text': m['title'], 'color': c},
        'description': m['desc'],
        'icon': icon_obj(m['icon']),
        'background': m['bg'],
        'unlocked_by_default': m['unlocked'],
        'starting_points': 1,
        'colors': {
            'connections': {
                'locked': {'fill': '#4b4b4b', 'stroke': '#1c1c1c'},
                'available': {'fill': shade(c, 0.45), 'stroke': '#1c1c1c'},
                'affordable': {'fill': shade(c, 0.2), 'stroke': '#1c1c1c'},
                'unlocked': {'fill': c, 'stroke': '#1c1c1c'},
                'excluded': {'fill': '#7a1f1f', 'stroke': '#2a0b0b'},
            },
            'points': {'fill': c, 'stroke': '#1c1c1c'},
        },
    }
    if not m['unlocked']:
        d['spent_points_limit'] = CLASS_SPENT_LIMIT
        d['extra_description'] = ('Unlocked by your class quest. Capstones need %d points spent in this tree. '
                                  'You can spend at most %d points here, so choose.' % (CAP_REQUIRED_SPENT, CLASS_SPENT_LIMIT))
    else:
        d['extra_description'] = 'Capstones need %d points spent in this tree.' % 12
    return d


def build_tree(cat):
    spec = TREES[cat]
    is_adv = cat == 'adventurer'
    template = ADV_BRANCH if is_adv else CLASS_BRANCH
    links = ADV_LINKS if is_adv else CLASS_LINKS
    defs, skills, conns = {}, {}, []
    color = META[cat]['color']

    def make_def(def_id, title, rewards, icon, frame, cost, req_spent=0):
        lines = [describe(k, v) for k, v in rewards]
        title_obj = title if frame == 'task' else {'text': title, 'color': color if frame == 'goal' else 'gold'}
        d = {
            'title': title_obj,
            'description': '\n'.join(lines),
            'icon': icon_obj(icon),
            'frame': FRAME[frame],
            'rewards': [reward(k, v) for k, v in rewards],
            'cost': cost,
        }
        if req_spent:
            d['required_spent_points'] = req_spent
            d['extra_description'] = 'Requires %d points spent in this tree.' % req_spent
        defs[def_id] = d

    # root
    rt, rrew, ricon = spec['root']
    root_id = '%s_root' % cat
    make_def(root_id, rt, rrew, ricon, 'goal', 1)
    skills[root_id] = {'x': 0, 'y': ROOT_Y, 'definition': root_id, 'root': True}

    for bi, (bname, nodes) in enumerate(spec['branches']):
        bx = BRANCH_X[bi]
        for slot, dx, row, frame, cost in template:
            title, rew, icon = nodes[slot]
            sid = '%s_b%d_%s' % (cat, bi + 1, slot)
            if icon is None:
                icon = ICON[rew[0][0]]
            req = 0
            if slot == 'cap':
                req = 12 if is_adv else CAP_REQUIRED_SPENT
            make_def(sid, title, rew, icon, frame, cost, req)
            skills[sid] = {'x': bx + dx * FORK_DX, 'y': -row * ROW_DY - (8 if slot == 'cap' else 0),
                           'definition': sid}
        conns.append([root_id, '%s_b%d_a1' % (cat, bi + 1)])
        for a, b in links:
            conns.append(['%s_b%d_%s' % (cat, bi + 1, a), '%s_b%d_%s' % (cat, bi + 1, b)])
    return defs, skills, {'normal': {'bidirectional': conns}}


# ---------------------------------------------------------------------------------------------
# Experience sources
# ---------------------------------------------------------------------------------------------
def op(t, data=None):
    d = {'type': t}
    if data is not None:
        d['data'] = data
    return d


def var(ops, fallback=0):
    return {'operations': ops, 'fallback': fallback}


def sr(v):
    """Stochastic rounding (XP is Math.round()-ed per event). Uses world time as the dice."""
    return 'floor(%s) + (fract(%s) > mod(t, 100) / 100)' % (v, v)


class Vars:
    def __init__(self, prefix_get_player='get_player'):
        self.v = {}
        self.gp = prefix_get_player

    def add(self, name, ops, fallback=0):
        assert name not in self.v, name
        self.v[name] = var(ops, fallback)
        return name

    def any_of(self, prefix, base_ops, key, values):
        names = []
        for i, val in enumerate(values):
            n = '%s_%d' % (prefix, i)
            self.add(n, list(base_ops) + [op('puffish_skills:test', {key: val})])
            names.append(n)
        return '(' + ' | '.join(names) + ')'

    def time(self):
        return self.add('t', [op(self.gp), op('get_world'), op('get_time_of_day')])


KILLED_TYPE = [op('get_killed_living_entity'), op('get_type')]
WEAPON = [op('get_weapon_item_stack')]
DMG_TYPE = [op('get_damage_source'), op('get_type')]

EXCLUDED_KILLS = ['minecraft:villager', 'minecraft:iron_golem', 'minecraft:snow_golem', 'minecraft:wandering_trader',
                  'minecraft:player', 'minecraft:armor_stand', 'guardvillagers:guard']

BOSS_EXTRA = ['minecraft:warden', 'minecraft:elder_guardian', 'kingsandmonsters:ogre_lord', 'graveyard:lich',
              'dog:devourer_head', 'darkdoppelganger:dark_doppelganger', 'draconicevolution:draconic_guardian',
              'iceandfire:hydra', 'iceandfire:sea_serpent', 'iceandfire:cyclops', 'iceandfire:gorgon',
              'iceandfire:dread_lich', 'iceandfire:fire_dragon', 'iceandfire:ice_dragon', 'iceandfire:lightning_dragon',
              'born_in_chaos_v1:lord_pumpkinhead', 'born_in_chaos_v1:supreme_bonescaller', 'born_in_chaos_v1:krampus',
              'born_in_chaos_v1:nightmare_stalker', 'legendary_monsters:ancient_guardian',
              'legendary_monsters:overgrown_colossus', 'legendary_monsters:withered_abomination',
              'legendary_monsters:frostbitten_golem', 'legendary_monsters:endersent', 'legendary_monsters:lava_eater',
              'legendary_monsters:skeletosaurus', 'legendary_monsters:warped_fungussus',
              'legendary_monsters:dune_sentinel']

NEMESIS = {
    'red': ['cataclysm:ignis', 'cataclysm:netherite_monstrosity', 'bosses_of_mass_destruction:gauntlet',
            'born_in_chaos_v1:lord_pumpkinhead', 'irons_spellbooks:fire_boss'],
    'orange': ['mowziesmobs:ferrous_wroughtnaut', 'mowziesmobs:sculptor', 'kingsandmonsters:ogre_lord',
               'bosses_of_mass_destruction:void_blossom', 'cataclysm:ancient_remnant'],
    'yellow': ['cataclysm:the_harbinger', 'cataclysm:scylla', 'iceandfire:lightning_dragon'],
    'green': ['irons_spellbooks:dead_king'],
    'blue': ['mowziesmobs:frostmaw', 'bosses_of_mass_destruction:lich', 'cataclysm:maledictus',
             'twilightforest:snow_queen', 'twilightforest:alpha_yeti'],
    'indigo': ['mowziesmobs:umvuthi', 'iceandfire:hydra', 'iceandfire:sea_serpent', 'cataclysm:the_leviathan'],
    'violet': ['born_in_chaos_v1:nightmare_stalker', 'graveyard:lich', 'cataclysm:ender_guardian',
               'bosses_of_mass_destruction:obsidilith', 'minecraft:warden'],
}

KILL_AF = {'limit_per_chunk': 24, 'reset_after_seconds': 300}
BOSS_AF = {'limit_per_chunk': 40, 'reset_after_seconds': 600}
TEAM_KILL = {'distance_limit': 32.0}
TEAM_BOSS = {'distance_limit': 64.0}

HEAVY_ITEMS = ['#simplyswords:heavy_weapons', '#minecraft:axes', 'minecraft:mace',
               'minecraftdungeonsv1:claymore', 'minecraftdungeonsv1:broad_sword_claymore',
               'minecraftdungeonsv1:great_hammer', 'minecraftdungeonsv1:great_hammer_of_gravity',
               'minecraftdungeonsv1:stormlander_great_hammer', 'irons_spellbooks:claymore',
               'irons_spellbooks:decrepit_scythe', 'legendary_monsters:shattered_greatsword',
               'legendary_monsters:soul_great_sword', 'legendary_monsters:withered_scythe',
               'legendary_monsters:sharp_battle_axe', 'discerning_the_eldritch:deep_greatsword',
               'discerning_the_eldritch:soul_fire_scythe', 'discerning_the_eldritch:starmetal_scythe',
               'companions:crystallized_blood_scythe', 'born_in_chaos_v1:nightmare_scythe']
EK_MATERIALS = ['wood', 'stone', 'copper', 'tin', 'bronze', 'iron', 'steel', 'silver', 'gold', 'diamond', 'netherite']
HEAVY_ITEMS += ['magistuarmory:%s_%s' % (m, t) for m in EK_MATERIALS
                for t in ('claymore', 'zweihander', 'heavywarhammer', 'concavehalberd')]

HAMMER_ITEMS = ['minecraft:mace', 'minecraftdungeonsv1:great_hammer', 'minecraftdungeonsv1:great_hammer_of_gravity',
                'minecraftdungeonsv1:stormlander_great_hammer', 'minecraftdungeonsv1:mace',
                'minecraftdungeonsv1:suns_grace_mace', 'born_in_chaos_v1:shell_mace']
HAMMER_ITEMS += ['simplyswords:%s_greathammer' % m for m in ('iron', 'gold', 'diamond', 'netherite', 'runic')]
HAMMER_ITEMS += ['magistuarmory:%s_%s' % (m, t) for m in EK_MATERIALS for t in ('heavymace', 'heavywarhammer')]

SS_MATS = ('iron', 'gold', 'diamond', 'netherite', 'runic')
LIGHT_ITEMS = ['simplyswords:%s_%s' % (m, t) for m in SS_MATS for t in ('rapier', 'katana', 'twinblade')]
LIGHT_ITEMS += ['irons_spellbooks:amethyst_rapier', 'discerning_the_eldritch:forlorn_rapier']

DAGGER_ITEMS = ['simplyswords:%s_sai' % m for m in SS_MATS]
DAGGER_ITEMS += ['minecraftdungeonsv1:dagger', 'minecraftdungeonsv1:fangs_of_frost_dagger',
                 'born_in_chaos_v1:dark_ritual_dagger', 'born_in_chaos_v1:intoxicating_dagger',
                 'companions:netherite_dagger', 'discerning_the_eldritch:ritual_dagger', 'graveyard:bone_dagger',
                 'iceandfire:stymphalian_bird_dagger', 'mowziesmobs:naga_fang_dagger',
                 'farmersdelight:flint_knife', 'farmersdelight:iron_knife', 'farmersdelight:golden_knife',
                 'farmersdelight:diamond_knife', 'farmersdelight:netherite_knife']

COLD_MOBS = ['minecraft:stray', 'minecraft:polar_bear', 'irons_spellbooks:ice_spider', 'irons_spellbooks:cryomancer',
             'mowziesmobs:frostmaw', 'twilightforest:yeti', 'twilightforest:alpha_yeti', 'twilightforest:winter_wolf',
             'twilightforest:snow_guardian', 'twilightforest:snow_queen', 'twilightforest:stable_ice_core',
             'twilightforest:unstable_ice_core', 'legendary_monsters:frostbitten_golem', 'iceandfire:ice_dragon',
             'bosses_of_mass_destruction:lich', 'cataclysm:maledictus', 'born_in_chaos_v1:krampus',
             'alexsmobs:froststalker', 'alexsmobs:snow_leopard']

RAIDER_EXTRA = ['graveyard:corrupted_pillager', 'graveyard:corrupted_vindicator', 'graveyard:corrupted_evoker',
                'irons_spellbooks:archevoker', 'irons_spellbooks:magehunter_vindicator']

SUMMON_SPELLS = ['irons_spellbooks:raise_dead', 'irons_spellbooks:summon_vex', 'irons_spellbooks:summon_polar_bear',
                 'irons_spellbooks:summon_swords', 'cataclysm_spellbooks:conjure_amethyst_crab',
                 'cataclysm_spellbooks:conjure_ignited_reinforcement', 'cataclysm_spellbooks:conjure_koboldiator',
                 'cataclysm_spellbooks:conjure_thralls', 'cataclysm_spellbooks:summon_koboleton',
                 'discerning_the_eldritch:conjure_forsaken_aid', 'discerning_the_eldritch:conjure_gaoler',
                 'discerning_the_eldritch:call_ascended_one']

# Yellow: technology items crafted at a crafting table (XP per item; Pufferfish multiplies by the crafted amount)
TECH_CRAFTS = {
    # Create
    'create:mechanical_press': 5, 'create:mechanical_mixer': 5, 'create:encased_fan': 4, 'create:mechanical_drill': 4,
    'create:mechanical_saw': 4, 'create:deployer': 6, 'create:mechanical_harvester': 3, 'create:mechanical_plough': 3,
    'create:mechanical_bearing': 4, 'create:windmill_bearing': 4, 'create:water_wheel': 3, 'create:large_water_wheel': 6,
    'create:steam_engine': 8, 'create:mechanical_crafter': 4, 'create:mechanical_arm': 8, 'create:millstone': 3,
    'create:spout': 4, 'create:item_drain': 3, 'create:mechanical_pump': 3, 'create:rotation_speed_controller': 6,
    'create:sequenced_gearshift': 4, 'create:gantry_carriage': 3, 'create:elevator_pulley': 5, 'create:rope_pulley': 3,
    'create:cart_assembler': 4, 'create:track_station': 6, 'create:controls': 6, 'create:portable_storage_interface': 4,
    'create:contraption_controls': 3, 'create:display_link': 3, 'create:schematicannon': 10,
    'create:empty_blaze_burner': 4, 'create:goggles': 3, 'create:wrench': 2, 'create:extendo_grip': 6,
    'create:potato_cannon': 6, 'create:wand_of_symmetry': 6, 'create:clockwork_bearing': 6, 'create:mechanical_roller': 4,
    'create:package_frogport': 4, 'create:stock_ticker': 6, 'create:packager': 3, 'create:copper_backtank': 6,
    'create:netherite_backtank': 20, 'create:mechanical_piston': 3, 'create:chain_conveyor': 3,
    'create:speedometer': 2, 'create:stressometer': 2, 'create:steam_whistle': 2,
    # Create addons
    'createaddition:electric_motor': 8, 'createaddition:alternator': 8, 'createaddition:rolling_mill': 5,
    'createaddition:tesla_coil': 8, 'createaddition:modular_accumulator': 6, 'createaddition:portable_energy_interface': 4,
    'createaddition:digital_adapter': 4,
    'aeronautics:propeller_bearing': 6, 'aeronautics:gyroscopic_propeller_bearing': 12, 'aeronautics:smart_propeller': 10,
    'aeronautics:wooden_propeller': 3, 'aeronautics:andesite_propeller': 4, 'aeronautics:adjustable_burner': 5,
    'aeronautics:steam_vent': 5, 'aeronautics:aviators_goggles': 4, 'aeronautics:mounted_potato_cannon': 6,
    'simulated:physics_assembler': 10, 'simulated:steering_wheel': 6, 'simulated:throttle_lever': 4,
    'simulated:navigation_table': 8, 'simulated:altitude_sensor': 3, 'simulated:velocity_sensor': 3,
    'simulated:gimbal_sensor': 3, 'simulated:docking_connector': 5, 'simulated:rope_winch': 4,
    'simulated:swivel_bearing': 5, 'simulated:laser_sensor': 3, 'simulated:redstone_magnet': 3,
    'simulated:analog_transmission': 4,
    # Mekanism
    'mekanism:metallurgic_infuser': 6, 'mekanism:enrichment_chamber': 6, 'mekanism:crusher': 6,
    'mekanism:osmium_compressor': 6, 'mekanism:combiner': 6, 'mekanism:purification_chamber': 8,
    'mekanism:chemical_injection_chamber': 10, 'mekanism:energized_smelter': 6, 'mekanism:digital_miner': 30,
    'mekanism:electrolytic_separator': 8, 'mekanism:chemical_infuser': 8, 'mekanism:chemical_oxidizer': 8,
    'mekanism:chemical_washer': 8, 'mekanism:chemical_dissolution_chamber': 10, 'mekanism:chemical_crystallizer': 10,
    'mekanism:precision_sawmill': 6, 'mekanism:pressurized_reaction_chamber': 10, 'mekanism:rotary_condensentrator': 8,
    'mekanism:electric_pump': 6, 'mekanism:teleporter': 20, 'mekanism:quantum_entangloporter': 20,
    'mekanism:solar_neutron_activator': 15, 'mekanism:isotopic_centrifuge': 15, 'mekanism:antiprotonic_nucleosynthesizer': 40,
    'mekanism:mekasuit_helmet': 40, 'mekanism:mekasuit_bodyarmor': 40, 'mekanism:mekasuit_pants': 40,
    'mekanism:mekasuit_boots': 40, 'mekanism:atomic_disassembler': 15, 'mekanism:meka_tool': 40, 'mekanism:jetpack': 15,
    'mekanism:free_runners': 8, 'mekanism:basic_energy_cube': 5, 'mekanism:advanced_energy_cube': 10,
    'mekanism:elite_energy_cube': 15, 'mekanism:ultimate_energy_cube': 20, 'mekanism:steel_casing': 4,
    'mekanism:portable_teleporter': 15, 'mekanism:robit': 15, 'mekanism:seismic_vibrator': 8,
    'mekanism:modification_station': 15, 'mekanism:formulaic_assemblicator': 8, 'mekanism:sps_casing': 10,
    'mekanism:supercharged_coil': 15, 'mekanism:dimensional_stabilizer': 15, 'mekanism:qio_drive_array': 15,
    'mekanism:qio_dashboard': 10, 'mekanism:scuba_tank': 5, 'mekanism:electric_bow': 8, 'mekanism:flamethrower': 8,
    'mekanismgenerators:heat_generator': 4, 'mekanismgenerators:solar_generator': 5,
    'mekanismgenerators:advanced_solar_generator': 12, 'mekanismgenerators:wind_generator': 8,
    'mekanismgenerators:gas_burning_generator': 15, 'mekanismgenerators:bio_generator': 6,
    'mekanismgenerators:fusion_reactor_controller': 40, 'mekanismgenerators:turbine_rotor': 4,
    'mekanismgenerators:electromagnetic_coil': 8, 'mekanismgenerators:rotational_complex': 15,
    'mekanismgenerators:saturating_condenser': 8,
    # Draconic Evolution
    'draconicevolution:draconium_core': 8, 'draconicevolution:wyvern_core': 20, 'draconicevolution:awakened_core': 40,
    'draconicevolution:chaotic_core': 80, 'draconicevolution:crafting_core': 15,
    'draconicevolution:basic_crafting_injector': 6, 'draconicevolution:wyvern_crafting_injector': 12,
    'draconicevolution:awakened_crafting_injector': 20, 'draconicevolution:chaotic_crafting_injector': 40,
    'draconicevolution:energy_core': 20, 'draconicevolution:energy_core_stabilizer': 10,
    'draconicevolution:reactor_core': 60, 'draconicevolution:reactor_injector': 20,
    'draconicevolution:wyvern_capacitor': 15, 'draconicevolution:draconic_capacitor': 30,
    'draconicevolution:wyvern_chestpiece': 30, 'draconicevolution:draconic_chestpiece': 50,
    'draconicevolution:chaotic_chestpiece': 80, 'draconicevolution:wyvern_sword': 15,
    'draconicevolution:draconic_sword': 30, 'draconicevolution:chaotic_sword': 60,
    'draconicevolution:wyvern_pickaxe': 15, 'draconicevolution:draconic_pickaxe': 30,
    'draconicevolution:chaotic_pickaxe': 60, 'draconicevolution:module_core': 5,
    # Applied Energistics 2 (smaller)
    'ae2:controller': 10, 'ae2:drive': 8, 'ae2:inscriber': 8, 'ae2:molecular_assembler': 8,
    'ae2:crafting_unit': 4, 'ae2:energy_acceptor': 3, 'ae2:wireless_access_point': 6,
    'ae2:quantum_ring': 15, 'ae2:spatial_io_port': 8, 'ae2:wireless_terminal': 10, 'ae2:crafting_terminal': 5,
    'ae2:pattern_encoding_terminal': 5, 'ae2:charger': 3, 'ae2:vibration_chamber': 3,
}


def src(t, data, team=None):
    d = {'type': t, 'data': data}
    if team:
        d['team_sharing'] = team
    return d


def boss_any(V, prefix='boss'):
    base = V.any_of(prefix + 't', KILLED_TYPE, 'entity_type', ['#c:bosses'])
    extra = V.any_of(prefix + 'x', KILLED_TYPE, 'entity_type', BOSS_EXTRA)
    return '(%s | %s)' % (base, extra)


def excl_any(V, base_ops=KILLED_TYPE):
    return V.any_of('ex', base_ops, 'entity_type', EXCLUDED_KILLS)


def kill_source(variables, experience, tamed=None, af=KILL_AF, team=TEAM_KILL):
    data = {'variables': variables, 'experience': experience, 'anti_farming_per_chunk': af}
    if tamed:
        data['tamed'] = tamed
    return src('puffish_skills:kill_entity', data, team)


def class_boss_source(cat, extra_cases=None):
    V = Vars()
    boss = boss_any(V)
    nem = V.any_of('nem', KILLED_TYPE, 'entity_type', NEMESIS[cat])
    cases = [{'condition': nem, 'expression': '150'},
             {'condition': '%s & !%s' % (boss, nem), 'expression': '40'}]
    if extra_cases:
        for ids, val in extra_cases:
            e = V.any_of('el%d' % len(cases), KILLED_TYPE, 'entity_type', ids)
            cases.append({'condition': '%s & !%s & !%s' % (e, boss, nem), 'expression': str(val)})
    return kill_source(V.v, cases, af=BOSS_AF, team=TEAM_BOSS)


def spell_source(cond_builder, mult=1.0):
    """cond_builder(V) -> condition string. XP ~ 0.5 + mana/30 per full cast, split across continuous ticks."""
    V = Vars(prefix_get_player='player')
    V.time()
    V.add('mana', [op('mana_cost')])
    V.add('mps', [op('mana_cost_per_second')])
    V.add('dur', [op('cast_duration')])
    V.add('ticks', [op('expected_ticks')], fallback=1)
    cond = cond_builder(V)
    v = '%s * (0.5 + max(mana, mps * dur) / 30) / max(ticks, 1)' % mult
    return src('pufferfish_unofficial_additions:spell_casting',
               {'variables': V.v, 'experience': [{'condition': cond, 'expression': sr(v)}]})


def schools(*ids):
    def b(V):
        return V.any_of('school', [op('school')], 'school', list(ids))
    return b


def spells(ids):
    def b(V):
        return V.any_of('spell', [op('spell')], 'spell', ids)
    return b


def player_hp(V):
    V.add('hp', [op('get_player'), op('as_living_entity'), op('get_health')], fallback=20)
    V.add('maxhp', [op('get_player'), op('as_living_entity'), op('get_max_health')], fallback=20)


def dim(V, name, dimension):
    return V.add(name, [op('get_player'), op('get_world'), op('puffish_skills:test', {'dimension': dimension})])


def melee(V):
    return V.add('melee', [op('get_damage_source'), op('puffish_skills:is_melee')])


def stat_test(V, name, stat):
    return V.add(name, [op('get_stat'), op('puffish_skills:test', {'stat': stat})])


def stat_value(V, name, stat):
    return V.add(name, [op('get_player'), op('puffish_skills:get_stat_value', {'stat': stat})])


def travel_source(stats, blocks, xp):
    V = Vars()
    tests = [stat_test(V, 'is%d' % i, 'minecraft.custom:minecraft.%s' % s) for i, s in enumerate(stats)]
    vals = [stat_value(V, 'tot%d' % i, 'minecraft.custom:minecraft.%s' % s) for i, s in enumerate(stats)]
    V.add('amount', [op('get_increase_amount')])
    tot = '(' + ' + '.join(vals) + ')'
    cm = blocks * 100
    expr = '%d * (floor((%s + amount) / %d) - floor(%s / %d))' % (xp, tot, cm, tot, cm)
    return src('puffish_skills:increase_stat',
               {'variables': V.v, 'experience': [{'condition': '(' + ' | '.join(tests) + ')', 'expression': expr}]})


def stat_rewards(pairs):
    """pairs: [(stat id, xp)]"""
    V = Vars()
    cases = []
    for i, (stat, xp) in enumerate(pairs):
        n = stat_test(V, 's%d' % i, stat)
        cases.append({'condition': n, 'expression': str(xp)})
    return src('puffish_skills:increase_stat', {'variables': V.v, 'experience': cases})


def criterion(crit, xp):
    return src('puffish_skills:criterion', {'criterion': crit, 'experience': str(xp)})


def mh_var(V):
    V.add('mh', [op('get_killed_living_entity'), op('get_max_health')])


def dmg_any(V, prefix, tags):
    return V.any_of(prefix, DMG_TYPE, 'damage_type', tags)


def experience_for(cat):
    sources = []
    if cat == 'adventurer':
        # 1) every kill, scaled by the victim's max health
        V = Vars(); mh_var(V); V.time()
        boss = boss_any(V); ex = excl_any(V)
        sources.append(kill_source(V.v, [{'condition': '!%s & !%s' % (boss, ex),
                                          'expression': sr('min(mh, 200) / 8')}]))
        # 2) bosses (big)
        V = Vars(); mh_var(V)
        boss = boss_any(V)
        sources.append(kill_source(V.v, [{'condition': boss, 'expression': '60 + min(mh, 3000) / 4'}],
                                   af=BOSS_AF, team=TEAM_BOSS))
        # 3) exploration: 3 XP per 300 blocks sprinted / swum / ridden / flown with elytra
        sources.append(travel_source(['sprint_one_cm', 'swim_one_cm', 'horse_one_cm', 'aviate_one_cm'], 300, 3))
        # 4) raids
        sources.append(stat_rewards([('minecraft.custom:minecraft.raid_win', 40)]))
        return sources

    if cat == 'red':
        V = Vars(); mh_var(V); V.time(); melee(V); player_hp(V)
        fire = dmg_any(V, 'fire', ['#irons_spellbooks:fire_magic', '#minecraft:is_fire'])
        blood = dmg_any(V, 'blood', ['#irons_spellbooks:blood_magic'])
        nether = dim(V, 'nether', 'minecraft:the_nether')
        heavy = V.any_of('heavy', WEAPON, 'item', HEAVY_ITEMS)
        ex = excl_any(V)
        v = 'min(mh, 200) / 10 * (1 + 0.8 * %s * melee + 0.5 * %s + 0.5 * (hp / maxhp < 0.4))' % (heavy, nether)
        sources.append(kill_source(V.v, [{'condition': '(melee | %s | %s) & !%s' % (fire, blood, ex),
                                          'expression': sr(v)}]))
        # fighting while below 40% health
        V = Vars(); V.time(); player_hp(V)
        V.add('dmg', [op('get_dealt_damage')])
        V.add('melee', [op('get_damage_source'), op('puffish_skills:is_melee')])
        ex = V.any_of('ex', [op('get_damaged_living_entity'), op('get_type')], 'entity_type', EXCLUDED_KILLS)
        sources.append(src('puffish_skills:deal_damage', {
            'variables': V.v,
            'experience': [{'condition': 'melee & hp / maxhp < 0.4 & !%s' % ex,
                            'expression': sr('min(dmg, 20) * 0.15')}],
            'anti_farming_per_entity': {'limit_per_entity': 6, 'reset_after_seconds': 300}}))
        sources.append(spell_source(schools('irons_spellbooks:fire', 'irons_spellbooks:blood')))
        sources.append(class_boss_source('red'))
        return sources

    if cat == 'orange':
        V = Vars(); V.time()
        V.add('silk', [op('get_tool_item_stack'), op('puffish_skills:test', {
            'predicates': {'minecraft:enchantments': [{'enchantments': 'minecraft:silk_touch', 'levels': {'min': 1}}]}})])
        tiers = [('deb', '#c:ores/netherite_scrap', '15'), ('dia', '#c:ores/diamond', '10'),
                 ('eme', '#c:ores/emerald', '10'), ('gold', '#c:ores/gold', '4'), ('lapis', '#c:ores/lapis', '3'),
                 ('redst', '#c:ores/redstone', '2'), ('iron', '#c:ores/iron', '2'), ('quartz', '#c:ores/quartz', '1'),
                 ('coal', '#c:ores/coal', '1'), ('copper', '#c:ores/copper', sr('0.7'))]
        BLOCK = [op('get_mined_block_state')]
        for n, tag, _ in tiers:
            V.add(n, BLOCK + [op('puffish_skills:test', {'block': tag})])
        V.add('ore', BLOCK + [op('puffish_skills:test', {'block': '#c:ores'})])
        V.add('stone', BLOCK + [op('puffish_skills:test', {'block': 'minecraft:stone'})])
        V.add('deep', BLOCK + [op('puffish_skills:test', {'block': 'minecraft:deepslate'})])
        stat_value(V, 'mined_stone', 'minecraft.mined:minecraft.stone')
        stat_value(V, 'mined_deep', 'minecraft.mined:minecraft.deepslate')
        cases, prev = [], []
        for n, _, xp in tiers:
            cond = '!silk & %s' % n + ''.join(' & !%s' % p for p in prev)
            cases.append({'condition': cond, 'expression': xp})
            prev.append(n)
        cases.append({'condition': '!silk & ore' + ''.join(' & !%s' % p for p in prev), 'expression': '3'})
        # stone: 1 XP every 15 stone/deepslate mined, only for the first 45 000 blocks (no stone-generator farming)
        cases.append({'condition': '!silk & !ore & (stone | deep) & mined_stone + mined_deep < 45000 & '
                                   'mod(mined_stone + mined_deep, 15) = 0', 'expression': '1'})
        sources.append(src('puffish_skills:mine_block', {'variables': V.v, 'experience': cases}))
        # tank kills: heavy armour and hammers/maces earn more
        V = Vars(); mh_var(V); V.time(); melee(V)
        V.add('armor', [op('get_player'), op('as_living_entity'),
                        op('puffish_skills:get_attribute', {'attribute': 'minecraft:generic.armor'}), op('get_value')])
        nature = dmg_any(V, 'nature', ['#irons_spellbooks:nature_magic'])
        hammer = V.any_of('hammer', WEAPON, 'item', HAMMER_ITEMS)
        ex = excl_any(V)
        v = 'min(mh, 200) / 12 * (1 + 0.5 * (armor >= 15) + 0.5 * %s * melee)' % hammer
        sources.append(kill_source(V.v, [{'condition': '(melee | %s) & !%s' % (nature, ex), 'expression': sr(v)}]))
        # selling to villagers for emeralds
        sources.append(criterion({'trigger': 'minecraft:villager_trade',
                                  'conditions': {'item': {'items': 'minecraft:emerald'}}}, 2))
        sources.append(spell_source(schools('irons_spellbooks:nature')))
        sources.append(class_boss_source('orange'))
        return sources

    if cat == 'yellow':
        V = Vars()
        terms = []
        for i, (item, xp) in enumerate(sorted(TECH_CRAFTS.items())):
            n = 'c%d' % i
            V.add(n, [op('get_crafted_item_stack'), op('puffish_skills:test', {'item': item})])
            terms.append('%d * %s' % (xp, n))
        sources.append(src('puffish_skills:craft_item', {'variables': V.v,
                                                         'experience': [{'expression': ' + '.join(terms)}]}))
        sources.append(spell_source(schools('irons_spellbooks:lightning', 'cataclysm_spellbooks:technomancy')))
        V = Vars(); mh_var(V); V.time(); melee(V)
        V.add('sword', WEAPON + [op('puffish_skills:test', {'item': '#minecraft:swords'})])
        light = V.any_of('light', WEAPON, 'item', LIGHT_ITEMS)
        bolt = dmg_any(V, 'bolt', ['#irons_spellbooks:lightning_magic', '#minecraft:is_lightning'])
        V.add('speed', [op('get_player'), op('as_living_entity'),
                        op('puffish_skills:get_effect', {'effect': 'minecraft:speed'}), op('get_level')])
        ex = excl_any(V)
        factor = 'max(0.6 * melee * sword, 1.0 * melee * %s, 1.2 * %s)' % (light, bolt)
        v = 'min(mh, 200) / 10 * %s * (1 + 0.5 * (speed > 0))' % factor
        sources.append(kill_source(V.v, [{'condition': '!%s' % ex, 'expression': sr(v)}]))
        sources.append(class_boss_source('yellow'))
        return sources

    if cat == 'green':
        sources.append(stat_rewards([('minecraft.custom:minecraft.raid_win', 200),
                                     ('minecraft.custom:minecraft.traded_with_villager', 2)]))
        sources.append(criterion({'trigger': 'minecraft:cured_zombie_villager'}, 40))
        sources.append(criterion({'trigger': 'minecraft:summoned_entity', 'conditions': {'entity': [
            {'condition': 'minecraft:entity_properties', 'entity': 'this',
             'predicate': {'type': 'minecraft:iron_golem'}}]}}, 25))
        V = Vars(); mh_var(V); V.time(); melee(V)
        evo = dmg_any(V, 'evo', ['#irons_spellbooks:evocation_magic'])
        holy = dmg_any(V, 'holy', ['#irons_spellbooks:holy_magic'])
        raider = V.any_of('raider', KILLED_TYPE, 'entity_type', ['#minecraft:raiders'] + RAIDER_EXTRA)
        ex = excl_any(V)
        v = 'min(mh, 200) / 6 * max(%s, 0.5 * (melee | %s | %s))' % (raider, evo, holy)
        sources.append(kill_source(V.v, [{'condition': '!%s' % ex, 'expression': sr(v)}]))
        # burst healing (spells, potions) - natural regeneration ticks heal 1 HP and do not count
        V = Vars(); V.time()
        V.add('amount', [op('get_heal_amount')])
        sources.append(src('puffish_skills:heal', {'variables': V.v, 'experience': [
            {'condition': 'amount >= 2', 'expression': sr('min(amount, 20) * 0.25')}]}))
        sources.append(spell_source(schools('irons_spellbooks:evocation', 'irons_spellbooks:holy')))
        sources.append(class_boss_source('green', extra_cases=[(['irons_spellbooks:archevoker'], 60),
                                                                (['minecraft:ravager'], 20),
                                                                (['minecraft:evoker'], 10)]))
        return sources

    if cat == 'blue':
        sources.append(spell_source(schools('irons_spellbooks:ice')))
        V = Vars(); mh_var(V); V.time(); melee(V)
        V.add('magic', [op('get_damage_source'), op('puffish_skills:is_magic')])
        icy = dmg_any(V, 'icy', ['#irons_spellbooks:ice_magic', '#minecraft:is_freezing'])
        cold = V.any_of('cold', KILLED_TYPE, 'entity_type', COLD_MOBS)
        V.add('cold_biome', [op('get_player'), op('as_entity'), op('puffish_skills:has_tag', {'tag': 'gl_cold_biome'})])
        ex = excl_any(V)
        v = 'min(mh, 200) / 10 * max(1.3 * %s, 1.0 * %s, 1.0 * cold_biome, 0.4 * (melee | magic))' % (icy, cold)
        sources.append(kill_source(V.v, [{'condition': '!%s' % ex, 'expression': sr(v)}]))
        # kills shared with other players (split by damage share)
        V = Vars(); mh_var(V); V.time()
        V.add('share', [op('get_share')])
        V.add('participants', [op('get_participants')], fallback=1)
        ex = excl_any(V)
        sources.append(src('puffish_skills:shared_kill_entity', {
            'variables': V.v,
            'experience': [{'condition': 'participants >= 2 & !%s' % ex, 'expression': sr('share * min(mh, 200) / 8')}],
            'anti_farming_per_chunk': KILL_AF}))
        # distance flown with elytra: 3 XP per 400 blocks
        sources.append(travel_source(['aviate_one_cm'], 400, 3))
        sources.append(class_boss_source('blue'))
        return sources

    if cat == 'indigo':
        sources.append(stat_rewards([('minecraft.custom:minecraft.animals_bred', 3)]))
        sources.append(criterion({'trigger': 'minecraft:tame_animal'}, 15))
        V = Vars(prefix_get_player='player'); V.time()
        V.add('crop', [op('block'), op('puffish_skills:test', {'block': '#minecraft:crops'})])
        V.add('crops', [op('dropped_crops')])
        V.add('seeds', [op('dropped_seeds')])
        sources.append(src('pufferfish_unofficial_additions:harvest_crops', {'variables': V.v, 'experience': [
            {'condition': 'crop & (crops >= 2 | (crops >= 1 & seeds >= 1))', 'expression': sr('0.6')}]}))
        sources.append(spell_source(spells(SUMMON_SPELLS), mult=1.5))
        # kills made by your tamed animals
        V = Vars(); mh_var(V); V.time(); ex = excl_any(V)
        sources.append(kill_source(V.v, [{'condition': '!%s' % ex, 'expression': sr('min(mh, 200) / 8')}],
                                   tamed='only'))
        # ranger: bow / crossbow kills
        V = Vars(); mh_var(V); V.time(); ex = excl_any(V)
        V.add('proj', [op('get_damage_source'), op('puffish_skills:is_projectile')])
        sources.append(kill_source(V.v, [{'condition': 'proj & !%s' % ex, 'expression': sr('min(mh, 200) / 12')}]))
        sources.append(class_boss_source('indigo'))
        return sources

    if cat == 'violet':
        V = Vars(); mh_var(V); V.time(); melee(V)
        V.add('proj', [op('get_damage_source'), op('puffish_skills:is_projectile')])
        void = dmg_any(V, 'void', ['#irons_spellbooks:ender_magic', '#irons_spellbooks:eldritch_magic'])
        V.add('undead', KILLED_TYPE + [op('puffish_skills:test', {'entity_type': '#minecraft:undead'})])
        end = dim(V, 'end', 'minecraft:the_end')
        over = dim(V, 'over', 'minecraft:overworld')
        V.add('invis', [op('get_player'), op('as_living_entity'),
                        op('puffish_skills:get_effect', {'effect': 'minecraft:invisibility'}), op('get_level')])
        V.add('sneaking', [op('get_player'), op('as_entity'), op('puffish_skills:has_tag', {'tag': 'gl_sneaking'})])
        dagger = V.any_of('dagger', WEAPON, 'item', DAGGER_ITEMS)
        ex = excl_any(V)
        night = '(mod(t, 24000) >= 13000) * (mod(t, 24000) <= 23000)'
        v = ('min(mh, 200) / 11 * (1 + 0.5 * %s * %s + 1.0 * max(invis > 0, sneaking) + 0.5 * undead + 0.5 * %s + 0.3 * %s * melee)'
             % (over, night, end, dagger))
        sources.append(kill_source(V.v, [{'condition': '(melee | proj | %s) & !%s' % (void, ex), 'expression': sr(v)}]))
        sources.append(spell_source(schools('irons_spellbooks:ender', 'irons_spellbooks:eldritch')))
        sources.append(class_boss_source('violet'))
        return sources
    raise KeyError(cat)


def experience_json(cat):
    adv = cat == 'adventurer'
    return {
        'level_limit': ADV_LEVEL_LIMIT if adv else CLASS_LEVEL_LIMIT,
        'experience_per_level': {'type': 'expression', 'data': {'expression': ADV_CURVE if adv else CLASS_CURVE}},
        'sources': experience_for(cat),
    }


def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, indent='\t', ensure_ascii=False)
        f.write('\n')


def main():
    if os.path.isdir(os.path.join(OUT, 'categories')):
        shutil.rmtree(os.path.join(OUT, 'categories'))
    write(os.path.join(OUT, 'config.json'), {'version': 3, 'categories': CATEGORIES})
    for cat in CATEGORIES:
        base = os.path.join(OUT, 'categories', cat)
        defs, skills, conns = build_tree(cat)
        write(os.path.join(base, 'category.json'), category_json(cat))
        write(os.path.join(base, 'definitions.json'), defs)
        write(os.path.join(base, 'skills.json'), skills)
        write(os.path.join(base, 'connections.json'), conns)
        write(os.path.join(base, 'experience.json'), experience_json(cat))
        cost = sum(d['cost'] for d in defs.values())
        print('%-10s nodes=%2d total_cost=%d sources=%d' % (cat, len(skills), cost, len(experience_json(cat)['sources'])))


if __name__ == '__main__':
    main()
