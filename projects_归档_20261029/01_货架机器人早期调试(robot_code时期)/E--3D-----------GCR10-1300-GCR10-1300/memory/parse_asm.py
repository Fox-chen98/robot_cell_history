# -*- coding: utf-8 -*-
"""解析装配体 STEP:提取各零部件的装配变换,把相机关键特征换算到下盖坐标系做验证"""
import re, sys
import numpy as np

path = sys.argv[1]
text = open(path, encoding='utf-8', errors='replace').read()
body = text[text.find('DATA;'):].replace('\n', ' ')

simple = {}   # id -> (type, args)
complexe = {} # id -> inner string
for m in re.finditer(r'#(\d+)\s*=\s*([A-Z_0-9]+)\s*\((.*?)\)\s*;', body):
    simple[int(m.group(1))] = (m.group(2), m.group(3))
for m in re.finditer(r'#(\d+)\s*=\s*\(\s*(.*?)\s*\)\s*;', body):
    eid = int(m.group(1))
    if eid not in simple:
        complexe[eid] = m.group(2)

def refs(s): return [int(x) for x in re.findall(r'#(\d+)', s)]
def floats(s): return [float(x) for x in re.findall(r'(-?\d+\.?\d*(?:[Ee][+-]?\d+)?)', s)]

def get_point(eid):
    return np.array(floats(simple[eid][1])[-3:])

def get_placement(eid):
    r = refs(simple[eid][1])
    o = get_point(r[0])
    z = get_point(r[1]) if len(r) > 1 else np.array([0,0,1.])
    x = get_point(r[2]) if len(r) > 2 else np.array([1,0,0.])
    z = z/np.linalg.norm(z); x = x/np.linalg.norm(x)
    y = np.cross(z, x)
    R = np.column_stack([x, y, z])  # 列为局部坐标轴在全局中的方向
    return o, R

# 产品名
pd_name = {}  # PRODUCT_DEFINITION id -> product name
prod_name = {}
for eid,(t,a) in simple.items():
    if t == 'PRODUCT':
        nm = re.findall(r"'([^']*)'", a)
        prod_name[eid] = nm[1] if len(nm)>1 else (nm[0] if nm else '?')
pdf2prod = {}
for eid,(t,a) in simple.items():
    if t == 'PRODUCT_DEFINITION_FORMATION_WITH_SPECIFIED_SOURCE' or t=='PRODUCT_DEFINITION_FORMATION':
        r = refs(a)
        for x in r:
            if x in prod_name: pdf2prod[eid]=prod_name[x]
for eid,(t,a) in simple.items():
    if t == 'PRODUCT_DEFINITION':
        r = refs(a)
        for x in r:
            if x in pdf2prod: pd_name[eid]=pdf2prod[x]

# NAUO: parent, child
nauo = {}
for eid,(t,a) in simple.items():
    if t == 'NEXT_ASSEMBLY_USAGE_OCCURRENCE':
        r = refs(a)
        nauo[eid] = r  # [parentPD, childPD]

# PRODUCT_DEFINITION_SHAPE -> nauo
pds2nauo = {}
for eid,(t,a) in simple.items():
    if t == 'PRODUCT_DEFINITION_SHAPE':
        r = refs(a)
        for x in r:
            if x in nauo: pds2nauo[eid]=x

# IDT
idt = {}
for eid,(t,a) in simple.items():
    if t == 'ITEM_DEFINED_TRANSFORMATION':
        r = refs(a)
        idt[eid] = r  # [plac1, plac2]

# CDSR (simple form)
results = []
for eid,(t,a) in simple.items():
    if t == 'CONTEXT_DEPENDENT_SHAPE_REPRESENTATION':
        r = refs(a)
        results.append(('CDSR', eid, r))

# 复合实体里找 RR_WITH_TRANSFORMATION
for eid, inner in complexe.items():
    if 'REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION' in inner:
        m = re.search(r'REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION\s*\(([^)]*)\)', inner)
        tr = refs(m.group(1)) if m else []
        m2 = re.search(r"REPRESENTATION_RELATIONSHIP\s*\('[^']*'\s*,\s*'[^']*'\s*,\s*([^)]*)\)", inner)
        reps = refs(m2.group(1)) if m2 else []
        results.append(('RRWT', eid, {'transform': tr, 'reps': reps}))

print('=== 复合RR实体(含变换) ===')
comp_transforms = []
for kind, eid, data in results:
    if kind == 'RRWT':
        tr = data['transform']
        for tid in tr:
            if tid in idt:
                p1, p2 = idt[tid][0], idt[tid][1]
                o1,R1 = get_placement(p1)
                o2,R2 = get_placement(p2)
                comp_transforms.append((eid, (o1,R1), (o2,R2)))
                print(f'#{eid}: IDT#{tid}')
                print(f'   plac1 原点={o1.round(3)}')
                print(f'   plac2 原点={o2.round(3)} z轴={R2[:,2].round(3)} x轴={R2[:,0].round(3)}')

# 找出 CDSR 对应的 NAUO 名称(简单实体形式时)
print()
print('=== 装配关系(NAUO) ===')
for eid, r in nauo.items():
    names = [pd_name.get(x,'?') for x in r if x in pd_name]
    print(f'NAUO#{eid}: {names}')

print()
print('=== CDSR → 组件 ===')
for kind, eid, r in results:
    if kind == 'CDSR':
        # r = [rep_rel(复合), pds]
        for x in r:
            if x in pds2nauo:
                n = pds2nauo[x]
                names = [pd_name.get(y,'?') for y in nauo[n] if y in pd_name]
                print(f'CDSR#{eid} 引用复合实体 {[y for y in r if y in complexe]} → 组件 {names}')
