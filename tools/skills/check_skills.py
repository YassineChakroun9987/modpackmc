"""Offline validator for the greenlanterns puffish_skills datapack (Pufferfish's Skills 0.19.2, config v3).

Mirrors what the mod does at load time, as read from the 0.19.2 source:
 * config version 3 => any unused / unknown JSON key is a hard error (LegacyUtils.wrapNoUnused)
 * every operation is resolved against its prototype; ids and tags are looked up in registries
 * any failure in one data pack disables ALL skill categories, so everything must pass.

usage: python -I check_skills.py
"""
import json
import os
import re
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK = os.path.join(ROOT, 'server', 'kubejs', 'data', 'greenlanterns', 'puffish_skills')
EXPORTED = os.path.join(ROOT, 'server', 'kubejs', 'exported')
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # tags_index.json lives next to this script
TAGS = os.path.join(SCRATCH, 'tags_index.json')
CLIENT_JAR = r'C:/Users/pc/curseforge/minecraft/Install/versions/1.21.1/1.21.1.jar'

errors, warnings = [], []


def err(where, msg):
    errors.append('%s: %s' % (where, msg))


def warn(where, msg):
    warnings.append('%s: %s' % (where, msg))


def load_list(name, key):
    return set(json.load(open(os.path.join(EXPORTED, name), encoding='utf-8'))[key])


ATTRS = load_list('attributes.json', 'attributes')
ITEMS = load_list('items.json', 'items')
ENTITIES = load_list('entity_types.json', 'entity_types')
EFFECTS = load_list('mob_effects.json', 'mob_effects')
DIMENSIONS = load_list('dimensions.json', 'dimensions')
ENCH = json.load(open(os.path.join(EXPORTED, 'enchantments.json'), encoding='utf-8'))
ENCH = set(ENCH[list(ENCH.keys())[0]]) if isinstance(ENCH, dict) else set(ENCH)
TAGIDX = {k: set(v) for k, v in json.load(open(TAGS, encoding='utf-8')).items()}
CLIENT = set(zipfile.ZipFile(CLIENT_JAR).namelist())

# Attributes that are attached to the PLAYER (AttributeReward rejects others: "Expected a valid player attribute").
VANILLA_PLAYER_ATTRS = {
    'generic.max_health', 'generic.knockback_resistance', 'generic.movement_speed', 'generic.armor',
    'generic.armor_toughness', 'generic.max_absorption', 'generic.step_height', 'generic.scale', 'generic.gravity',
    'generic.safe_fall_distance', 'generic.fall_damage_multiplier', 'generic.jump_strength', 'generic.oxygen_bonus',
    'generic.burning_time', 'generic.explosion_knockback_resistance', 'generic.water_movement_efficiency',
    'generic.movement_efficiency', 'generic.attack_knockback', 'generic.attack_damage', 'generic.attack_speed',
    'generic.luck', 'player.block_interaction_range', 'player.entity_interaction_range', 'player.block_break_speed',
    'player.submerged_mining_speed', 'player.sneaking_speed', 'player.mining_efficiency',
    'player.sweeping_damage_ratio'}
PLAYER_NS = {'irons_spellbooks', 'apothic_attributes', 'puffish_attributes', 'cataclysm_spellbooks', 'familiarslib'}
PLAYER_EXTRA = {'combat_roll:count', 'combat_roll:distance', 'ftbultimine:max_blocks_modifier'}


def player_attr_ok(a):
    if a not in ATTRS:
        return False
    ns, path = a.split(':', 1)
    if ns == 'minecraft':
        return path in VANILLA_PLAYER_ATTRS
    return ns in PLAYER_NS or a in PLAYER_EXTRA


CUSTOM_STATS = {'walk_one_cm', 'crouch_one_cm', 'sprint_one_cm', 'walk_on_water_one_cm', 'fall_one_cm', 'climb_one_cm',
                'fly_one_cm', 'walk_under_water_one_cm', 'minecart_one_cm', 'boat_one_cm', 'pig_one_cm',
                'horse_one_cm', 'aviate_one_cm', 'swim_one_cm', 'strider_one_cm', 'mob_kills', 'animals_bred',
                'player_kills', 'fish_caught', 'traded_with_villager', 'raid_trigger', 'raid_win'}
SCHOOLS = {'irons_spellbooks:' + s for s in ('fire', 'ice', 'lightning', 'holy', 'ender', 'blood', 'evocation',
                                             'nature', 'eldritch')} | {'cataclysm_spellbooks:abyssal',
                                                                       'cataclysm_spellbooks:technomancy',
                                                                       'cataclysm_spellbooks:sand'}
# Spell ids verified against the spell classes + their registry classes in the jars
SPELLS = {'irons_spellbooks:raise_dead', 'irons_spellbooks:summon_vex', 'irons_spellbooks:summon_polar_bear',
          'irons_spellbooks:summon_swords', 'irons_spellbooks:summon_horse',
          'cataclysm_spellbooks:conjure_amethyst_crab', 'cataclysm_spellbooks:conjure_ignited_reinforcement',
          'cataclysm_spellbooks:conjure_koboldiator', 'cataclysm_spellbooks:conjure_thralls',
          'cataclysm_spellbooks:summon_koboleton', 'discerning_the_eldritch:conjure_forsaken_aid',
          'discerning_the_eldritch:conjure_gaoler', 'discerning_the_eldritch:call_ascended_one'}


def check_id_or_tag(where, value, ids, tagkind):
    if not isinstance(value, str):
        err(where, 'expected string id, got %r' % (value,))
        return
    if value.startswith('#'):
        if value[1:] not in TAGIDX.get(tagkind, set()):
            err(where, 'unknown %s tag %s' % (tagkind, value))
    else:
        v = value if ':' in value else 'minecraft:' + value
        if ids is not None and v not in ids:
            err(where, 'unknown %s id %s' % (tagkind, value))


def keys_ok(where, obj, allowed, required=()):
    if not isinstance(obj, dict):
        err(where, 'expected object')
        return False
    for k in obj:
        if k not in allowed:
            err(where, 'unknown/unused key "%s" (fatal with config version 3)' % k)
    for k in required:
        if k not in obj:
            err(where, 'missing required key "%s"' % k)
    return True


# ---------------------------------------------------------------------------------------------
# Expression parser (port of net.puffish.skillsmod.expression.DefaultParser / Parser / Lexer)
# ---------------------------------------------------------------------------------------------
BIN = {'|': (1, 'L'), '&': (2, 'L'), '=': (3, 'L'), '<>': (3, 'L'), '>=': (4, 'L'), '<=': (4, 'L'), '>': (4, 'L'),
       '<': (4, 'L'), '+': (5, 'L'), '-': (5, 'L'), '*': (6, 'L'), '/': (6, 'L'), '^': (8, 'R')}
UNARY_PREC = 7
FUNCS = {'sin': 1, 'cos': 1, 'tan': 1, 'asin': 1, 'acos': 1, 'atan': 1, 'atan2': 2, 'sinh': 1, 'cosh': 1, 'tanh': 1,
         'log': 1, 'exp': 1, 'sqrt': 1, 'cbrt': 1, 'floor': 1, 'ceil': 1, 'round': 1, 'trunc': 1, 'abs': 1,
         'sign': 1, 'fract': 1, 'mod': 2, 'mix': 3, 'clamp': 3, 'min': -1, 'max': -1}
CONSTS = {'pi': 3.141592653589793, 'tau': 6.283185307179586, 'e': 2.718281828459045}
OP_TOKENS = ['<>', '>=', '<=', '|', '&', '=', '>', '<', '+', '-', '*', '/', '^', '!', '(', ')', ',']


def tokenize(s):
    i, out = 0, []
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        for t in OP_TOKENS:
            if s.startswith(t, i):
                out.append(t)
                i += len(t)
                break
        else:
            m = re.match(r'[0-9.a-zA-Z_]+', s[i:])
            if not m:
                raise ValueError('bad character %r at %d' % (s[i], i))
            out.append(m.group(0))
            i += len(m.group(0))
    return out


class Expr:
    def __init__(self, s, variables):
        self.toks = tokenize(s)
        self.p = 0
        self.vars = variables
        self.used = set()
        self.tree = self.parse_bin(0)
        if self.p != len(self.toks):
            raise ValueError('unexpected token %r' % self.toks[self.p])

    def peek(self):
        return self.toks[self.p] if self.p < len(self.toks) else None

    def take(self, t=None):
        tok = self.peek()
        if tok is None or (t is not None and tok != t):
            raise ValueError('expected %r, got %r' % (t, tok))
        self.p += 1
        return tok

    def parse_unary(self):
        tok = self.peek()
        if tok in ('!', '+', '-'):
            self.take()
            return ('u', tok, self.parse_bin(UNARY_PREC))
        if tok == '(':
            self.take('(')
            e = self.parse_bin(0)
            self.take(')')
            return e
        tok = self.take()
        if tok in OP_TOKENS:
            raise ValueError('unexpected operator %r' % tok)
        if tok in FUNCS and self.peek() == '(':
            self.take('(')
            args = [self.parse_bin(0)]
            while self.peek() == ',':
                self.take(',')
                args.append(self.parse_bin(0))
            self.take(')')
            n = FUNCS[tok]
            if n >= 0 and len(args) != n:
                raise ValueError('function %s expects %d args' % (tok, n))
            return ('f', tok, args)
        try:
            return ('n', float(tok))
        except ValueError:
            pass
        if tok in self.vars or tok in CONSTS:
            self.used.add(tok)
            return ('v', tok)
        raise ValueError('Unknown variable `%s`' % tok)

    def parse_bin(self, min_prec):
        left = self.parse_unary()
        while True:
            tok = self.peek()
            if tok not in BIN:
                break
            prec, assoc = BIN[tok]
            if prec < min_prec:
                break
            self.take()
            nxt = prec + 1 if assoc == 'L' else prec
            right = self.parse_bin(nxt)
            left = ('b', tok, left, right)
        return left

    def eval(self, env, node=None):
        node = self.tree if node is None else node
        k = node[0]
        if k == 'n':
            return node[1]
        if k == 'v':
            return env[node[1]] if node[1] in env else CONSTS[node[1]]
        if k == 'u':
            x = self.eval(env, node[2])
            return {'!': 1.0 if x == 0 else 0.0, '+': x, '-': -x}[node[1]]
        if k == 'f':
            a = [self.eval(env, x) for x in node[2]]
            import math
            f = node[1]
            if f == 'floor':
                return float(math.floor(a[0]))
            if f == 'fract':
                return a[0] - math.floor(a[0])
            if f == 'mod':
                return a[0] - a[1] * math.floor(a[0] / a[1])
            if f == 'min':
                return min(a)
            if f == 'max':
                return max(a)
            if f == 'clamp':
                return max(a[1], min(a[2], a[0]))
            return float(getattr(math, f)(*a))
        l, r = self.eval(env, node[2]), self.eval(env, node[3])
        o = node[1]
        if o == '|':
            return 0.0 if l == 0 and r == 0 else 1.0
        if o == '&':
            return 0.0 if l == 0 or r == 0 else 1.0
        if o == '=':
            return float(l == r)
        if o == '<>':
            return float(l != r)
        if o == '>=':
            return float(l >= r)
        if o == '<=':
            return float(l <= r)
        if o == '>':
            return float(l > r)
        if o == '<':
            return float(l < r)
        if o == '+':
            return l + r
        if o == '-':
            return l - r
        if o == '*':
            return l * r
        if o == '/':
            return l / r
        if o == '^':
            return l ** r
        raise ValueError(o)


# ---------------------------------------------------------------------------------------------
# Prototype type system for operation chains
# ---------------------------------------------------------------------------------------------
SRC_PROTO = {
    'puffish_skills:kill_entity': {'get_player': 'player', 'get_weapon_item_stack': 'item_stack',
                                   'get_killed_living_entity': 'living_entity', 'get_damage_source': 'damage_source',
                                   'get_dropped_experience': 'number'},
    'puffish_skills:shared_kill_entity': {'get_player': 'player', 'get_weapon_item_stack': 'item_stack',
                                          'get_killed_living_entity': 'living_entity',
                                          'get_damage_source': 'damage_source', 'get_dropped_experience': 'number',
                                          'get_total_dealt_damage': 'number', 'get_participants': 'number',
                                          'get_share': 'number'},
    'puffish_skills:deal_damage': {'get_player': 'player', 'get_weapon_item_stack': 'item_stack',
                                   'get_damaged_living_entity': 'living_entity', 'get_damage_source': 'damage_source',
                                   'get_dealt_damage': 'number'},
    'puffish_skills:mine_block': {'get_player': 'player', 'get_mined_block_state': 'block_state',
                                  'get_tool_item_stack': 'item_stack'},
    'puffish_skills:craft_item': {'get_player': 'player', 'get_crafted_item_stack': 'item_stack'},
    'puffish_skills:increase_stat': {'get_player': 'player', 'get_stat': 'stat', 'get_increase_amount': 'number'},
    'puffish_skills:heal': {'get_player': 'player', 'get_heal_amount': 'number'},
    'puffish_skills:criterion': {'get_player': 'player'},
    'pufferfish_unofficial_additions:spell_casting': {
        'player': 'player', 'main_hand': 'item_stack', 'spellbook': 'item_stack', 'school': 'ua_school',
        'spell': 'ua_spell', 'level': 'number', 'min_level_rarity': 'number', 'rarity_name': 'ua_string',
        'rarity': 'number', 'mana_cost': 'number', 'mana_cost_per_second': 'number', 'cast_duration': 'number',
        'cast_charge_time': 'number', 'cooldown': 'number', 'expected_ticks': 'number'},
    'pufferfish_unofficial_additions:harvest_crops': {'player': 'player', 'block': 'block_state', 'tool': 'item_stack',
                                                      'dropped_seeds': 'number', 'dropped_crops': 'number'},
}
SRC_DATA_KEYS = {
    'puffish_skills:kill_entity': {'variables', 'experience', 'anti_farming_per_chunk', 'tamed'},
    'puffish_skills:shared_kill_entity': {'variables', 'experience', 'anti_farming_per_chunk', 'tamed'},
    'puffish_skills:deal_damage': {'variables', 'experience', 'anti_farming_per_entity', 'anti_farming_per_chunk',
                                   'tamed'},
    'puffish_skills:mine_block': {'variables', 'experience'},
    'puffish_skills:craft_item': {'variables', 'experience'},
    'puffish_skills:increase_stat': {'variables', 'experience'},
    'puffish_skills:heal': {'variables', 'experience'},
    'puffish_skills:criterion': {'criterion', 'variables', 'experience'},
    'pufferfish_unofficial_additions:spell_casting': {'variables', 'experience'},
    'pufferfish_unofficial_additions:harvest_crops': {'variables', 'experience'},
}
# prototype -> {op name: (result prototype, allowed data keys or None for "no data")}
PROTO = {
    'player': {'as_living_entity': ('living_entity', None), 'as_entity': ('entity', None),
               'get_world': ('world', None), 'puffish_skills:get_stat_value': ('number', {'stat'})},
    'living_entity': {'as_entity': ('entity', None), 'get_type': ('entity_type', None), 'get_world': ('world', None),
                      'get_max_health': ('number', None), 'get_health': ('number', None),
                      'puffish_skills:get_effect': ('effect_instance', {'effect'}),
                      'puffish_skills:get_attribute': ('attribute_instance', {'attribute'})},
    'entity': {'get_type': ('entity_type', None), 'get_world': ('world', None),
               'puffish_skills:test': ('boolean', {'entity_type', 'nbt'}),
               'puffish_skills:has_tag': ('boolean', {'tag'})},
    'world': {'get_server': ('server', None), 'get_time_of_day': ('number', None),
              'puffish_skills:test': ('boolean', {'dimension'})},
    'item_stack': {'get_item': ('item', None), 'get_count': ('number', None),
                   'puffish_skills:test': ('boolean', {'item', 'nbt', 'components', 'predicates'})},
    'item': {'puffish_skills:test': ('boolean', {'item'})},
    'block_state': {'get_block': ('block', None), 'puffish_skills:test': ('boolean', {'block', 'state'})},
    'block': {'puffish_skills:test': ('boolean', {'block'})},
    'damage_source': {'get_type': ('damage_type', None), 'get_attacker': ('entity', None),
                      'get_source': ('entity', None), 'puffish_skills:is_melee': ('boolean', None),
                      'puffish_skills:is_projectile': ('boolean', None), 'puffish_skills:is_magic': ('boolean', None)},
    'damage_type': {'puffish_skills:test': ('boolean', {'damage_type'})},
    'entity_type': {'puffish_skills:test': ('boolean', {'entity_type'})},
    'stat': {'get_type': ('stat_type', None), 'puffish_skills:test': ('boolean', {'stat'})},
    'effect_instance': {'get_level': ('number', None), 'get_duration': ('number', None)},
    'attribute_instance': {'get_value': ('number', None), 'get_base_value': ('number', None)},
    'ua_school': {'puffish_skills:test': ('boolean', {'school'})},
    'ua_spell': {'puffish_skills:test': ('boolean', {'spell'}), 'min_level': ('number', None),
                 'max_level': ('number', None)},
    'boolean': {'switch': ('number', {'true', 'false'})},
}


def check_stat(where, s):
    m = re.match(r'^([a-z0-9_]+)\.([a-z0-9_]+):([a-z0-9_]+)\.([a-z0-9_./]+)$', s or '')
    if not m:
        err(where, 'bad stat id %r' % s)
        return
    stype = m.group(1) + ':' + m.group(2)
    sid = m.group(3) + ':' + m.group(4)
    if stype == 'minecraft:custom':
        if m.group(3) != 'minecraft' or m.group(4) not in CUSTOM_STATS:
            err(where, 'unknown custom stat %s' % sid)
    elif stype == 'minecraft:mined':
        if sid not in ITEMS:   # block ids; every block used here also has an item
            err(where, 'unknown block for mined stat %s' % sid)
    else:
        err(where, 'unhandled stat type %s' % stype)


def check_test_data(where, proto, data):
    for k, v in data.items():
        w = '%s.%s' % (where, k)
        if k == 'entity_type':
            check_id_or_tag(w, v, ENTITIES, 'entity_type')
        elif k == 'item':
            check_id_or_tag(w, v, ITEMS, 'item')
        elif k == 'block':
            check_id_or_tag(w, v, ITEMS, 'block')
        elif k == 'damage_type':
            check_id_or_tag(w, v, None, 'damage_type')
            if not v.startswith('#'):
                warn(w, 'damage type id not verified: %s' % v)
        elif k == 'dimension':
            if v not in DIMENSIONS:
                err(w, 'unknown dimension %s' % v)
        elif k == 'stat':
            check_stat(w, v)
        elif k == 'school':
            if v not in SCHOOLS:
                err(w, 'unknown school %s' % v)
        elif k == 'spell':
            if v not in SPELLS:
                err(w, 'unverified spell %s' % v)
        elif k == 'predicates':
            ok = (isinstance(v, dict) and list(v) == ['minecraft:enchantments']
                  and isinstance(v['minecraft:enchantments'], list))
            if not ok:
                err(w, 'unexpected predicates shape')
            else:
                for p in v['minecraft:enchantments']:
                    keys_ok(w, p, {'enchantments', 'levels'})
                    if p.get('enchantments') not in ENCH:
                        err(w, 'unknown enchantment %s' % p.get('enchantments'))
        else:
            err(w, 'data key not handled by checker: %s' % k)


def check_variables(where, src_type, variables):
    names = set()
    if not isinstance(variables, dict):
        err(where, 'variables must be an object')
        return names
    for name, v in variables.items():
        w = '%s.variables.%s' % (where, name)
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
            err(w, 'bad variable name')
        keys_ok(w, v, {'operations', 'fallback', 'required'}, ('operations',))
        names.add(name)
        cur = 'source'
        for i, o in enumerate(v.get('operations', [])):
            wo = '%s.operations[%d]' % (w, i)
            keys_ok(wo, o, {'type', 'data'}, ('type',))
            t = o.get('type')
            table = SRC_PROTO[src_type] if cur == 'source' else PROTO.get(cur, {})
            if t not in table:
                err(wo, 'operation "%s" not valid on prototype %s' % (t, cur))
                cur = None
                break
            if cur == 'source':
                nxt, allowed = table[t], None
            else:
                nxt, allowed = table[t]
            if 'data' in o:
                if allowed is None:
                    err(wo, 'operation %s takes no data' % t)
                else:
                    keys_ok(wo + '.data', o['data'], allowed)
                    if t == 'puffish_skills:test':
                        check_test_data(wo + '.data', cur, o['data'])
                    elif t == 'puffish_skills:get_effect':
                        if o['data'].get('effect') not in EFFECTS:
                            err(wo, 'unknown effect %s' % o['data'].get('effect'))
                    elif t == 'puffish_skills:get_attribute':
                        if o['data'].get('attribute') not in ATTRS:
                            err(wo, 'unknown attribute %s' % o['data'].get('attribute'))
                    elif t == 'puffish_skills:get_stat_value':
                        check_stat(wo, o['data'].get('stat'))
            elif allowed:
                err(wo, 'operation %s requires data' % t)
            cur = nxt
        if cur not in ('number', 'boolean'):
            err(w, 'operations end in %s, expected number/boolean' % cur)
        if 'fallback' not in v:
            warn(w, 'no fallback')
    return names


def check_calc(where, exp, names):
    exprs = []
    if isinstance(exp, str):
        exprs.append(('expression', exp))
    elif isinstance(exp, list):
        for i, c in enumerate(exp):
            keys_ok('%s[%d]' % (where, i), c, {'condition', 'expression'}, ('expression',))
            for k in ('condition', 'expression'):
                if k in c:
                    exprs.append(('%s[%d].%s' % (where, i, k), c[k]))
    else:
        err(where, 'experience must be string or array')
    parsed = []
    for w, s in exprs:
        try:
            parsed.append((w, Expr(s, names)))
        except Exception as e:
            err('%s.%s' % (where, w), 'expression error: %s  in: %s' % (e, s[:200]))
    return parsed


def check_source(where, s):
    keys_ok(where, s, {'type', 'data', 'team_sharing'}, ('type', 'data'))
    t = s.get('type')
    if t not in SRC_PROTO:
        err(where, 'unknown source type %s' % t)
        return None
    if 'team_sharing' in s:
        keys_ok(where + '.team_sharing', s['team_sharing'], {'distance_limit'}, ('distance_limit',))
    data = s['data']
    keys_ok(where + '.data', data, SRC_DATA_KEYS[t], ('experience',))
    if 'anti_farming_per_chunk' in data:
        keys_ok(where + '.anti_farming_per_chunk', data['anti_farming_per_chunk'],
                {'limit_per_chunk', 'reset_after_seconds'}, ('limit_per_chunk', 'reset_after_seconds'))
    if 'anti_farming_per_entity' in data:
        keys_ok(where + '.anti_farming_per_entity', data['anti_farming_per_entity'],
                {'limit_per_entity', 'reset_after_seconds'}, ('limit_per_entity', 'reset_after_seconds'))
    if 'tamed' in data and data['tamed'] not in ('exclude', 'include', 'only'):
        err(where, 'bad tamed option')
    if t == 'puffish_skills:criterion':
        c = data.get('criterion', {})
        keys_ok(where + '.criterion', c, {'trigger', 'conditions'}, ('trigger',))
        if not c.get('trigger', '').startswith('minecraft:'):
            err(where, 'unexpected trigger')
        it = c.get('conditions', {}).get('item', {}).get('items')
        if it and it not in ITEMS:
            err(where, 'unknown criterion item %s' % it)
    names = check_variables(where, t, data.get('variables', {}))
    return check_calc(where + '.experience', data['experience'], names)


def check_text(where, t):
    if isinstance(t, str):
        return
    if isinstance(t, dict):
        for k in t:
            if k not in ('text', 'color', 'bold', 'italic', 'translate'):
                warn(where, 'text key %s' % k)
        if 'color' in t and not (re.match(r'^#[0-9a-fA-F]{6}$', t['color']) or t['color'] in (
                'gold', 'red', 'green', 'aqua', 'yellow', 'white', 'gray', 'dark_purple', 'light_purple', 'blue')):
            err(where, 'bad text color %s' % t['color'])
        return
    err(where, 'bad text object')


def check_icon(where, ic):
    keys_ok(where, ic, {'type', 'data'}, ('type', 'data'))
    if ic.get('type') == 'item':
        keys_ok(where + '.data', ic['data'], {'item'}, ('item',))
        if ic['data'].get('item') not in ITEMS:
            err(where, 'unknown icon item %s' % ic['data'].get('item'))
    elif ic.get('type') == 'effect':
        keys_ok(where + '.data', ic['data'], {'effect'}, ('effect',))
        if ic['data'].get('effect') not in EFFECTS:
            err(where, 'unknown icon effect %s' % ic['data'].get('effect'))
    else:
        err(where, 'icon type %s' % ic.get('type'))


def check_color_fs(where, c):
    if isinstance(c, str):
        c = {'fill': c}
    keys_ok(where, c, {'fill', 'stroke'})
    for k, v in c.items():
        if not re.match(r'^#([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$', v):
            err(where, 'bad colour %s' % v)


def main():
    # ---- files: valid JSON, lowercase paths
    all_json = {}
    for root, dirs, files in os.walk(PACK):
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, PACK).replace('\\', '/')
            if rel != rel.lower():
                err(rel, 'path must be lowercase')
            try:
                all_json[rel] = json.load(open(p, encoding='utf-8'))
            except Exception as e:
                err(rel, 'invalid JSON: %s' % e)

    cfg = all_json.get('config.json')
    keys_ok('config.json', cfg, {'version', 'categories'}, ('version', 'categories'))
    if cfg.get('version') != 3:
        err('config.json', 'version must be 3 for 0.19.x')
    cats = cfg.get('categories', [])
    for c in cats:
        if not re.match(r'^[a-z_]+$', c):
            err('config.json', 'category id %s must be [a-z_]' % c)
    folders = sorted({k.split('/')[1] for k in all_json if k.startswith('categories/')})
    if sorted(cats) != folders:
        err('config.json', 'categories %s != folders %s' % (cats, folders))

    report = []
    for cat in cats:
        P = 'categories/%s/' % cat
        need = ['category.json', 'definitions.json', 'skills.json', 'connections.json', 'experience.json']
        for n in need:
            if P + n not in all_json:
                err(P + n, 'missing')
        catj, defs, skills, conns, exp = [all_json.get(P + n, {}) for n in need]

        # category.json
        w = P + 'category.json'
        keys_ok(w, catj, {'title', 'description', 'extra_description', 'icon', 'background', 'colors',
                          'unlocked_by_default', 'starting_points', 'spent_points_limit', 'exclusive_root',
                          'erase_on_death'}, ('title', 'icon', 'background'))
        check_text(w + '.title', catj.get('title'))
        check_icon(w + '.icon', catj.get('icon', {}))
        bg = catj.get('background', '')
        tex = 'assets/%s/%s' % tuple(bg.split(':', 1)) if ':' in bg else 'assets/minecraft/' + bg
        if tex not in CLIENT:
            err(w, 'background texture not in vanilla client jar: %s' % bg)
        if tex + '.mcmeta' in CLIENT:
            warn(w, 'background is animated: %s' % bg)
        expected_unlocked = cat == 'adventurer'
        if catj.get('unlocked_by_default') is not expected_unlocked:
            err(w, 'unlocked_by_default should be %s' % expected_unlocked)
        cols = catj.get('colors', {})
        keys_ok(w + '.colors', cols, {'connections', 'exchange', 'points'})
        keys_ok(w + '.colors.connections', cols.get('connections', {}),
                {'locked', 'available', 'affordable', 'unlocked', 'excluded'})
        for k, v in cols.get('connections', {}).items():
            check_color_fs(w + '.colors.connections.' + k, v)
        if 'points' in cols:
            check_color_fs(w + '.colors.points', cols['points'])

        # definitions.json
        w = P + 'definitions.json'
        reward_attrs = {}
        for did, d in defs.items():
            wd = '%s[%s]' % (w, did)
            keys_ok(wd, d, {'title', 'description', 'extra_description', 'icon', 'frame', 'size', 'rewards', 'cost',
                            'required_skills', 'required_points', 'required_spent_points', 'required_exclusions',
                            'required_mods', 'metadata'}, ('title', 'icon', 'frame'))
            check_text(wd + '.title', d.get('title'))
            check_icon(wd + '.icon', d.get('icon', {}))
            fr = d.get('frame', {})
            keys_ok(wd + '.frame', fr, {'type', 'data'}, ('type', 'data'))
            if fr.get('type') != 'advancement' or fr.get('data', {}).get('frame') not in ('task', 'goal', 'challenge'):
                err(wd, 'bad frame')
            for k in ('cost', 'required_spent_points'):
                if k in d and (not isinstance(d[k], int) or d[k] < 0):
                    err(wd, '%s must be a non-negative integer' % k)
            for i, r in enumerate(d.get('rewards', [])):
                wr = '%s.rewards[%d]' % (wd, i)
                keys_ok(wr, r, {'type', 'data', 'required'}, ('type', 'data'))
                if r['type'] == 'puffish_skills:attribute':
                    keys_ok(wr + '.data', r['data'], {'attribute', 'value', 'operation'},
                            ('attribute', 'value', 'operation'))
                    a = r['data'].get('attribute')
                    if a not in ATTRS:
                        err(wr, 'attribute not in attributes.json: %s' % a)
                    elif not player_attr_ok(a):
                        err(wr, 'attribute probably not a PLAYER attribute: %s' % a)
                    if r['data'].get('operation') not in ('addition', 'multiply_base', 'multiply_total'):
                        err(wr, 'bad operation')
                    if not isinstance(r['data'].get('value'), (int, float)):
                        err(wr, 'value must be a number')
                    reward_attrs.setdefault(a, 0)
                    reward_attrs[a] += r['data']['value']
                elif r['type'] == 'puffish_skills:tag':
                    keys_ok(wr + '.data', r['data'], {'tag'}, ('tag',))
                else:
                    err(wr, 'unexpected reward type %s' % r['type'])

        # skills.json
        w = P + 'skills.json'
        roots = 0
        pos = {}
        for sid, s in skills.items():
            ws = '%s[%s]' % (w, sid)
            keys_ok(ws, s, {'x', 'y', 'definition', 'root'}, ('x', 'y', 'definition'))
            if s.get('definition') not in defs:
                err(ws, 'definition %s missing in definitions.json' % s.get('definition'))
            if not isinstance(s.get('x'), int) or not isinstance(s.get('y'), int):
                err(ws, 'x/y must be integers')
            if s.get('root'):
                roots += 1
            for other, (ox, oy) in pos.items():
                if abs(ox - s['x']) < 26 and abs(oy - s['y']) < 26:
                    err(ws, 'overlaps skill %s' % other)
            pos[sid] = (s['x'], s['y'])
        if roots != 1:
            err(w, 'expected exactly 1 root, found %d' % roots)
        unused_defs = set(defs) - {s['definition'] for s in skills.values()}
        if unused_defs:
            warn(w, 'unused definitions: %s' % sorted(unused_defs))

        # connections.json
        w = P + 'connections.json'
        keys_ok(w, conns, {'normal', 'exclusive'})
        adj = {s: set() for s in skills}
        seen = set()
        for kind, group in conns.items():
            keys_ok('%s.%s' % (w, kind), group, {'bidirectional', 'unidirectional'})
            for direction, pairs in group.items():
                for i, pr in enumerate(pairs):
                    wp = '%s.%s.%s[%d]' % (w, kind, direction, i)
                    if not (isinstance(pr, list) and len(pr) == 2):
                        err(wp, 'expected [a, b]')
                        continue
                    a, b = pr
                    for x in (a, b):
                        if x not in skills:
                            err(wp, 'unknown skill id %s' % x)
                    if a == b:
                        err(wp, 'self connection')
                    key = tuple(sorted((a, b)))
                    if key in seen:
                        err(wp, 'duplicate connection')
                    seen.add(key)
                    if a in adj and b in adj:
                        adj[a].add(b)
                        adj[b].add(a)
        root_id = [s for s, v in skills.items() if v.get('root')]
        if root_id:
            stack, reach = [root_id[0]], {root_id[0]}
            while stack:
                x = stack.pop()
                for y in adj[x]:
                    if y not in reach:
                        reach.add(y)
                        stack.append(y)
            if reach != set(skills):
                err(w, 'unreachable skills: %s' % sorted(set(skills) - reach))

        # experience.json
        w = P + 'experience.json'
        keys_ok(w, exp, {'level_limit', 'experience_per_level', 'sources', 'reset_on_death'},
                ('experience_per_level', 'sources'))
        epl = exp.get('experience_per_level', {})
        keys_ok(w + '.experience_per_level', epl, {'type', 'data'}, ('type', 'data'))
        curve = None
        if epl.get('type') == 'expression':
            keys_ok(w + '.experience_per_level.data', epl['data'], {'expression'}, ('expression',))
            try:
                curve = Expr(epl['data']['expression'], {'level'})
            except Exception as e:
                err(w, 'curve expression: %s' % e)
        else:
            err(w, 'expected expression curve')
        parsed_sources = []
        for i, s in enumerate(exp.get('sources', [])):
            parsed_sources.append((s.get('type'), check_source('%s.sources[%d]' % (w, i), s), s))

        total_cost = sum(d.get('cost', 1) for d in defs.values())
        lim = exp.get('level_limit', 10 ** 9)
        cum, table = 0, {}
        if curve:
            for L in range(lim):
                cum += round(curve.eval({'level': L}))
                if L + 1 in (1, 5, 10, 15, 25, 35, 40, 50):
                    table[L + 1] = cum
        report.append((cat, len(skills), total_cost, catj.get('spent_points_limit'), lim, table,
                       [t for t, _, _ in parsed_sources], reward_attrs))

    # ---- report
    print('=' * 100)
    for cat, n, cost, spent, lim, table, srcs, attrs in report:
        print('%-10s nodes=%d  total_cost=%d  spent_limit=%s  level_limit=%s' % (cat, n, cost, spent, lim))
        print('           cumulative XP to level: %s' % ', '.join('L%d=%d' % kv for kv in table.items()))
        print('           sources: %s' % ', '.join(s.split(':')[1] for s in srcs))
    print('=' * 100)
    for wmsg in warnings[:40]:
        print('WARN ', wmsg)
    if len(warnings) > 40:
        print('... %d more warnings' % (len(warnings) - 40))
    for e in errors:
        print('ERROR', e)
    print('errors=%d warnings=%d' % (len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
