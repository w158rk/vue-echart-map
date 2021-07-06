import os
import json
import copy

src = os.path.abspath('../static/json/map/world-original.json')
dst = os.path.abspath('../static/json/map/world.json')

sdata = None
ddata = None

with open(src, 'r') as f:
    sdata = json.load(f)

ddata = copy.deepcopy(sdata)

for spoly, dpoly in zip(sdata['features'],ddata['features']):
    print(spoly.keys())
    for scoord,dcoord in zip(spoly['geometry']['coordinates'], dpoly['geometry']['coordinates']):

        for s, d in zip(scoord, dcoord):
            if len(s)>2:
                for ss, dd in zip(s, d):
                    dd[0] = (ss[0] + 100)
                    if dd[0] > 180: 
                        dd[0] -= 360
            else:            
                d[0] = (s[0] + 100)
                if d[0] > 180: 
                    d[0] -= 360

with open(dst, 'w') as f:
    json.dump(ddata, f) 