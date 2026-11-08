import json,math
import os
D=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "server", "kubejs", "data", "greenlanterns", "loot_table", "chests") + "/"
def rolls_mean(r):
    return r if isinstance(r,(int,float)) else (r['min']+r['max'])/2
for t in range(1,6):
    d=json.load(open(D+'injected_tier_%d.json'%t))
    line=['T%d'%t]
    for luck in (0,2,5):
        parts=[]
        for p in d['pools']:
            ws=[]
            for e in p['entries']:
                w=max(0,math.floor(e.get('weight',1)+e.get('quality',0)*luck))
                ws.append((w,e))
            tot=sum(w for w,_ in ws)
            emp=sum(w for w,e in ws if e['type']=='minecraft:empty')
            junk=sum(w for w,e in ws if e.get('quality',0)<0 and e['type']!='minecraft:empty')
            rolls=rolls_mean(p['rolls'])+math.floor(rolls_mean(p.get('bonus_rolls',0))*luck)
            parts.append('%.1f rolls, %d%% blank, %d%% junk'%(rolls,100*emp/tot,100*junk/tot))
        line.append('luck%d: '%luck+' | '.join(parts))
    print('\n   '.join(line))
