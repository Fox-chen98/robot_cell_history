# -*- coding: utf-8 -*-
"""新旧零件 STEP 全面比对:平面/圆柱/圆锥/包围盒,输出差异报告"""
import re, sys, math
from collections import Counter

def parse(path):
    text = open(path, encoding='utf-8', errors='replace').read()
    body = text[text.find('DATA;'):].replace('\n', ' ')
    ents = {}
    for m in re.finditer(r'#(\d+)\s*=\s*([A-Z_0-9]+)\s*\((.*?)\)\s*;', body):
        ents[int(m.group(1))] = (m.group(2), m.group(3))
    def refs(a): return [int(x) for x in re.findall(r'#(\d+)', a)]
    def floats(a): return [float(x) for x in re.findall(r'(-?\d+\.?\d*(?:[Ee][+-]?\d+)?)', a)]
    def pt(eid):
        n = floats(ents[eid][1]); return tuple(round(v, 3) for v in n[-3:])
    def place(eid):
        r = refs(ents[eid][1])
        return pt(r[0]), (pt(r[1]) if len(r) > 1 else None)
    out = {'PLANE': [], 'CYL': [], 'CONE': [], 'VERT': []}
    for eid, (t, a) in ents.items():
        if t == 'PLANE':
            o, z = place(refs(a)[0]); out['PLANE'].append((o, z))
        elif t == 'CYLINDRICAL_SURFACE':
            o, z = place(refs(a)[0]); out['CYL'].append((round(floats(a)[-1], 3), o, z))
        elif t == 'CONICAL_SURFACE':
            o, z = place(refs(a)[0]); n = floats(a)
            out['CONE'].append((round(n[-2], 3), round(math.degrees(n[-1]), 1), o, z))
        elif t == 'VERTEX_POINT':
            out['VERT'].append(pt(refs(a)[0]))
    return out

old = parse(sys.argv[1]); new = parse(sys.argv[2])

def cyl_key(c):
    r, o, z = c
    # 用半径+轴线位置(XZ)归并:同一孔的多个半圆柱面合并
    ax = (round(o[0], 2), round(o[2], 2)) if abs(z[1]) > 0.9 else (round(o[0],2), round(o[1],2), round(o[2],2))
    return (r, ax)

def summarize_cyls(d):
    c = Counter(cyl_key(x) for x in d['CYL'])
    return c

def summarize_planes(d):
    c = Counter()
    for o, z in d['PLANE']:
        if abs(z[1]) > 0.9:  # 水平面按 Y 高度归并
            c[('Y=', o[1])] += 1
        else:
            c[('other', o, z)] += 1
    return c

def summarize_cones(d):
    c = Counter()
    for r, ang, o, z in d['CONE']:
        c[(r, ang, round(o[1], 2))] += 1
    return c

print('===== 水平平面 (按Y高度) =====')
po, pn = summarize_planes(old), summarize_planes(new)
for k in sorted(set(po) | set(pn), key=str):
    print(f'  {k}: 原件x{po.get(k,0)}  重建x{pn.get(k,0)}  {"✓" if po.get(k)==pn.get(k) else "≠"}')

print('===== 圆柱面 (半径, 轴位置XZ) =====')
co, cn = summarize_cyls(old), summarize_cyls(new)
for k in sorted(set(co) | set(cn), key=str):
    print(f'  R={k[0]} @ {k[1]}: 原件x{co.get(k,0)}  重建x{cn.get(k,0)}  {"✓" if co.get(k)==cn.get(k) else "≠"}')

print('===== 圆锥面/倒角 (半径, 半角, Y位置) =====')
ko, kn = summarize_cones(old), summarize_cones(new)
for k in sorted(set(ko) | set(kn), key=str):
    print(f'  R={k[0]} {k[1]}° Y={k[2]}: 原件x{ko.get(k,0)}  重建x{kn.get(k,0)}  {"✓" if ko.get(k)==kn.get(k) else "≠"}')

print('===== 包围盒 =====')
for name, d in [('原件', old), ('重建', new)]:
    xs=[p[0] for p in d['VERT']]; ys=[p[1] for p in d['VERT']]; zs=[p[2] for p in d['VERT']]
    print(f'  {name}: X[{min(xs):.3f},{max(xs):.3f}] Y[{min(ys):.3f},{max(ys):.3f}] Z[{min(zs):.3f},{max(zs):.3f}]')
