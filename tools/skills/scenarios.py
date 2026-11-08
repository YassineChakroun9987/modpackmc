"""Evaluate the generated XP expressions for typical events (average over world time for stochastic rounding)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_skills as C  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')


def load(cat):
    return json.load(open(os.path.join(C.PACK, 'categories', cat, 'experience.json'), encoding='utf-8'))


def xp(cat, src_index, env, night=False):
    s = load(cat)['sources'][src_index]
    names = set(s['data'].get('variables', {}))
    exp = s['data']['experience']
    cases = [{'expression': exp}] if isinstance(exp, str) else exp
    base = {n: 0.0 for n in names}
    base.update(env)
    total = 0.0
    times = range(18000, 18100) if night else range(6000, 6100)
    for t in times:
        e = dict(base, t=float(t))
        for c in cases:
            if 'condition' in c and C.Expr(c['condition'], names).eval(e) == 0:
                continue
            total += round(C.Expr(c['expression'], names).eval(e))
    return total / len(times)


def show(label, v):
    print('  %-62s %7.2f' % (label, v))


print('ADVENTURER')
show('zombie kill (20 HP)', xp('adventurer', 0, {'mh': 20}))
show('enderman kill (40 HP)', xp('adventurer', 0, {'mh': 40}))
show('boss: Ender Dragon (200 HP), boss source', xp('adventurer', 1, {'mh': 200, 'bosst_0': 1}))
show('boss: 1000 HP boss', xp('adventurer', 1, {'mh': 1000, 'bosst_0': 1}))
print('RED')
show('zombie, greatsword, overworld, full HP', xp('red', 0, {'mh': 20, 'melee': 1, 'heavy_0': 1, 'hp': 20, 'maxhp': 20}))
show('zombie, greatsword, Nether, <40% HP', xp('red', 0, {'mh': 20, 'melee': 1, 'heavy_0': 1, 'nether': 1, 'hp': 6, 'maxhp': 20}))
show('zombie, fireball (fire magic)', xp('red', 0, {'mh': 20, 'fire_0': 1, 'hp': 20, 'maxhp': 20}))
show('zombie, bow (no XP for Red)', xp('red', 0, {'mh': 20, 'hp': 20, 'maxhp': 20}))
show('hit for 8 dmg while <40% HP', xp('red', 1, {'dmg': 8, 'melee': 1, 'hp': 6, 'maxhp': 20}))
show('cast 40-mana fire spell', xp('red', 2, {'mana': 40, 'ticks': 1, 'school_0': 1}))
show('nemesis Ignis', xp('red', 3, {'nem_0': 1, 'bosst_0': 1}))
show('other boss', xp('red', 3, {'bosst_0': 1}))
print('ORANGE')
show('diamond ore', xp('orange', 0, {'dia': 1, 'ore': 1}))
show('iron ore', xp('orange', 0, {'iron': 1, 'ore': 1}))
show('copper ore', xp('orange', 0, {'copper': 1, 'ore': 1}))
show('silk-touched diamond ore', xp('orange', 0, {'dia': 1, 'ore': 1, 'silk': 1}))
show('stone (avg per block: 1 XP every 15th)', sum(xp('orange', 0, {'stone': 1, 'mined_stone': i}) for i in range(150)) / 150)
show('stone after 45k mined', xp('orange', 0, {'stone': 1, 'mined_stone': 45000}))
show('zombie, mace, armor 20', xp('orange', 1, {'mh': 20, 'melee': 1, 'armor': 20, 'hammer_0': 1}))
print('YELLOW')
y = load('yellow')['sources'][0]['data']['variables']
idx = {v['operations'][1]['data']['item']: k for k, v in y.items()}
show('craft mechanical press', xp('yellow', 0, {idx['create:mechanical_press']: 1}))
show('craft MekaSuit bodyarmor', xp('yellow', 0, {idx['mekanism:mekasuit_bodyarmor']: 1}))
show('zombie, rapier, Speed effect', xp('yellow', 2, {'mh': 20, 'melee': 1, 'sword': 1, 'light_0': 1, 'speed': 1}))
show('zombie, plain sword', xp('yellow', 2, {'mh': 20, 'melee': 1, 'sword': 1}))
show('zombie, lightning bolt spell', xp('yellow', 2, {'mh': 20, 'bolt_0': 1}))
print('GREEN')
show('raid won', xp('green', 0, {'s0': 1}))
show('villager trade', xp('green', 0, {'s1': 1}))
show('pillager kill (24 HP)', xp('green', 3, {'mh': 24, 'raider_0': 1, 'melee': 1}))
show('zombie, sword', xp('green', 3, {'mh': 20, 'melee': 1}))
show('heal 8 HP burst', xp('green', 4, {'amount': 8}))
show('natural regen tick (1 HP)', xp('green', 4, {'amount': 1}))
print('BLUE')
show('zombie, ice spell', xp('blue', 1, {'mh': 20, 'icy_0': 1, 'magic': 1}))
show('stray, sword', xp('blue', 1, {'mh': 20, 'cold_0': 1, 'melee': 1}))
show('zombie, sword, warm biome', xp('blue', 1, {'mh': 20, 'melee': 1}))
show('party kill 40 HP, 50% share', xp('blue', 2, {'mh': 40, 'share': 0.5, 'participants': 2}))
show('elytra 400 blocks (crossing)', xp('blue', 3, {'is0': 1, 'tot0': 39990, 'amount': 20}))
print('INDIGO')
show('animal bred', xp('indigo', 0, {'s0': 1}))
show('mature wheat (1 wheat + 2 seeds)', xp('indigo', 2, {'crop': 1, 'crops': 1, 'seeds': 2}))
show('immature potato (1 potato) -> no XP', xp('indigo', 2, {'crop': 1, 'crops': 1}))
show('raise dead (mana 80)', xp('indigo', 3, {'mana': 80, 'ticks': 1, 'spell_0': 1}))
show('wolf kills zombie', xp('indigo', 4, {'mh': 20}))
show('bow kills zombie', xp('indigo', 5, {'mh': 20, 'proj': 1}))
print('VIOLET')
show('zombie, dagger, night, overworld', xp('violet', 0, {'mh': 20, 'melee': 1, 'dagger_0': 1, 'undead': 1, 'over': 1}, night=True))
show('zombie, dagger, invisible, night', xp('violet', 0, {'mh': 20, 'melee': 1, 'dagger_0': 1, 'undead': 1, 'over': 1, 'invis': 1}, night=True))
show('skeleton, bow, day', xp('violet', 0, {'mh': 20, 'proj': 1, 'undead': 1, 'over': 1}))
show('enderman, sword, End', xp('violet', 0, {'mh': 40, 'melee': 1, 'end': 1}))
