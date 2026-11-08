"""Sanity-test the checker: every injected fault must produce at least one error."""
import copy
import io
import json
import os
import shutil
import sys
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_skills as C  # noqa: E402

SRC = C.PACK
TMP = os.path.join(HERE, '_mut_pack')


def run_with(mutate):
    if os.path.isdir(TMP):
        shutil.rmtree(TMP)
    shutil.copytree(SRC, TMP)
    mutate(TMP)
    C.PACK = TMP
    C.errors.clear()
    C.warnings.clear()
    with contextlib.redirect_stdout(io.StringIO()):
        C.main()
    return list(C.errors)


def edit(rel, fn):
    def m(root):
        p = os.path.join(root, rel)
        d = json.load(open(p, encoding='utf-8'))
        fn(d)
        json.dump(d, open(p, 'w', encoding='utf-8'))
    return m


def first_var(d, src=0):
    return d['sources'][src]['data']['variables']


cases = {
    'unknown item in test': edit('categories/yellow/experience.json',
                                 lambda d: first_var(d)['c0']['operations'][1]['data'].update(item='create:nope')),
    'unknown variable': edit('categories/red/experience.json',
                             lambda d: d['sources'][0]['data']['experience'][0].update(expression='mh * nosuchvar')),
    'extra key in data': edit('categories/orange/experience.json',
                              lambda d: d['sources'][0]['data'].update(anti_farming_per_chunk={'limit_per_chunk': 1, 'reset_after_seconds': 1})),
    'bad op on prototype': edit('categories/red/experience.json',
                                lambda d: first_var(d)['mh']['operations'].append({'type': 'get_world'})),
    'non-player attribute': edit('categories/red/definitions.json',
                                 lambda d: d['red_root']['rewards'][0]['data'].update(attribute='minecraft:generic.follow_range')),
    'unknown tag': edit('categories/violet/experience.json',
                        lambda d: first_var(d)['undead']['operations'][2]['data'].update(entity_type='#minecraft:nope')),
    'dangling connection': edit('categories/blue/connections.json',
                                lambda d: d['normal']['bidirectional'].append(['blue_root', 'blue_ghost'])),
    'missing definition': edit('categories/green/skills.json',
                               lambda d: d['green_root'].update(definition='nope')),
    'syntax error': edit('categories/indigo/experience.json',
                         lambda d: d['sources'][2]['data']['experience'][0].update(condition='crop & (crops >= 2')),
    'bad spell': edit('categories/indigo/experience.json',
                      lambda d: d['sources'][3]['data']['variables']['spell_0']['operations'][1]['data'].update(spell='irons_spellbooks:nope')),
    'unknown key in category': edit('categories/adventurer/category.json', lambda d: d.update(comment='x')),
}

ok = True
for name, mut in cases.items():
    errs = run_with(mut)
    status = 'caught' if errs else 'MISSED'
    if not errs:
        ok = False
    print('%-26s %s  %s' % (name, status, (errs[0][:110] if errs else '')))
shutil.rmtree(TMP)
print('ALL CAUGHT' if ok else 'SOME MISSED')
