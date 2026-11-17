---
name: two-lines-shared-context
description: 主线robocenter与支线robocenter_x在同一对话里并行的边界:各自职责/共享概念/绿盒与斜坡的语义约定
metadata: 
  node_type: memory
  type: project
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-08-25T07:57:06.762Z
---

用户的两个项目共用一个对话(有意为之, 因为共享大量上下文), 压缩后容易混淆。边界与共享面已写进**两份 CLAUDE.md 顶部的"两条线的分界"节**, 动手前先看那里。

**职责**: 主线 robocenter = 真机/MoveIt/判卷/标定/路径库(AutoDL + blue-space); 支线 robocenter_x = Isaac Sim 物理仿真/落料/合成数据(自有4070S `ssh sim_x`)。两个独立 git, 主线是标定值源头, 支线 `inherited/` 只读继承, **绝不反向改主线**。

**最易丢的是"语义约定"——参数文件里没写、但决定怎么用参数的知识**(2026-08-25 我就因为丢了这条把斜坡摆错):
- `conveyor` 绿色大盒 = 上苗机**整机包络**, 不是机身。⚠️ `box_center` 是**桌子系**坐标(主线 build_scene.py 挂桌子系)——2026-08-25 按基座系直读酿了第二次错(出料口错放 y=0.300, 用户看图纠正)
- 正确语义: 绿盒长边沿桌长朝 −y 伸出, 与桌面只重叠约16cm(y −0.177~−0.017, 配置注释"0.16重叠"即此); 出料口 y≈−0.02, 下料朝 +y, 离桌面27cm; **落料带 y −0.02~0.533 约55cm**(不是曾记的23.6cm)
- 桌面基座系 z=0.064; Isaac 里上苗机用用户 CadQuery 模型 climbing_conveyor.py, 锚点=出料口

**Why:** 参数值(数字)在 yaml 里查得到, 但"这个盒子代表什么、哪块是什么"只存在于对话里, 压缩即丢, 而它直接决定建模对不对。
**How to apply:** 用户说"做主线/支线的事"时先重读对应 CLAUDE.md; 遇到"这个物体是什么"的问题先查分界节的语义约定, 查不到就问用户而不是从几何猜。相关: [[sim-x-4070s-setup]] [[sim-as-validation-platform]]
