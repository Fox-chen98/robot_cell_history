# -*- coding: utf-8 -*-
"""解析 STEP 文件,提取平面/圆柱/圆锥/圆的几何参数,用于反推建模步骤"""
import re, sys
from collections import defaultdict

path = sys.argv[1]
text = open(path, encoding='utf-8', errors='replace').read()
# 合并续行
data_sec = text[text.find('DATA;'):]
body = data_sec.replace('\n', ' ')
entities = {}
for m in re.finditer(r'#(\d+)\s*=\s*([A-Z_0-9]+)\s*\((.*?)\)\s*;', body):
    eid, etype, args = int(m.group(1)), m.group(2), m.group(3)
    entities[eid] = (etype, args)

def refs(args):
    return [int(x) for x in re.findall(r'#(\d+)', args)]

def floats(args):
    return [float(x) for x in re.findall(r'(-?\d+\.?\d*(?:[Ee][+-]?\d+)?)', args)]

def get_point(eid):
    etype, args = entities[eid]
    nums = floats(args)
    return tuple(nums[-3:]) if len(nums) >= 3 else None

def get_dir(eid):
    return get_point(eid)

def get_placement(eid):
    """AXIS2_PLACEMENT_3D -> (origin, z_axis, x_axis)"""
    etype, args = entities[eid]
    r = refs(args)
    origin = get_point(r[0])
    z = get_dir(r[1]) if len(r) > 1 else None
    x = get_dir(r[2]) if len(r) > 2 else None
    return origin, z, x

def fmt(v, nd=4):
    if v is None: return 'None'
    return '(' + ', '.join(f'{x:.{nd}g}' for x in v) + ')'

print('=' * 70)
print('## 平面 PLANE')
for eid, (etype, args) in sorted(entities.items()):
    if etype == 'PLANE':
        origin, z, x = get_placement(refs(args)[0])
        print(f'#{eid:<5} 原点={fmt(origin)}  法向={fmt(z)}')

print('=' * 70)
print('## 圆柱面 CYLINDRICAL_SURFACE')
cyls = []
for eid, (etype, args) in sorted(entities.items()):
    if etype == 'CYLINDRICAL_SURFACE':
        r = refs(args)
        origin, z, x = get_placement(r[0])
        radius = floats(args.split(')')[-2] if ')' in args else args)
        # 半径是最后一个数字参数
        all_nums = floats(args)
        radius = all_nums[-1]
        cyls.append((eid, origin, z, radius))
        print(f'#{eid:<5} R={radius:<8.4g} 轴点={fmt(origin)}  轴向={fmt(z)}')

print('=' * 70)
print('## 圆锥面 CONICAL_SURFACE (半径, 半角)')
for eid, (etype, args) in sorted(entities.items()):
    if etype == 'CONICAL_SURFACE':
        r = refs(args)
        origin, z, x = get_placement(r[0])
        nums = floats(args)
        radius, semi_angle = nums[-2], nums[-1]
        import math
        print(f'#{eid:<5} R={radius:<8.4g} 半角={math.degrees(semi_angle):.2f}° 轴点={fmt(origin)}  轴向={fmt(z)}')

print('=' * 70)
print('## 圆 CIRCLE (按半径分组)')
circles_by_r = defaultdict(list)
for eid, (etype, args) in sorted(entities.items()):
    if etype == 'CIRCLE':
        r = refs(args)
        origin, z, x = get_placement(r[0])
        radius = floats(args)[-1]
        circles_by_r[round(radius, 4)].append((eid, origin, z))
for radius in sorted(circles_by_r):
    lst = circles_by_r[radius]
    print(f'--- R={radius}  (共{len(lst)}个)')
    for eid, origin, z in lst:
        print(f'    #{eid:<5} 圆心={fmt(origin)}  法向={fmt(z)}')

print('=' * 70)
print('## 包围盒 (基于所有 VERTEX 顶点)')
vps = []
for eid, (etype, args) in entities.items():
    if etype == 'VERTEX_POINT':
        p = get_point(refs(args)[0])
        if p: vps.append(p)
xs = [p[0] for p in vps]; ys = [p[1] for p in vps]; zs = [p[2] for p in vps]
print(f'X: {min(xs):.4f} ~ {max(xs):.4f}  (range {max(xs)-min(xs):.4f})')
print(f'Y: {min(ys):.4f} ~ {max(ys):.4f}  (range {max(ys)-min(ys):.4f})')
print(f'Z: {min(zs):.4f} ~ {max(zs):.4f}  (range {max(zs)-min(zs):.4f})')

print('=' * 70)
print('## 单位检查')
m = re.search(r'(MILLI.*?METRE|METRE)', text[:5000] + text[text.find('DATA;'):text.find('DATA;')+50000])
si = re.findall(r"SI_UNIT\s*\(\s*([^)]*)\)", body)
print('SI_UNIT:', si[:5])
