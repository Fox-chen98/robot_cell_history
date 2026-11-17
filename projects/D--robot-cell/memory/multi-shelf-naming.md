---
name: multi-shelf-naming
description: 格口名已改为带货架前缀 A-L10(2026-09-23 实施), 老名 L10 处处仍认; 加第二货架的后续步骤
metadata:
  type: project
---

2026-09-23 用户先说"一个货架基本够, 只要可拓展", 权衡后仍决定**现在就改名**(对方上位机尚未开始存数据, 是改名成本最低的时机)。已实施:

- 格口名 = `<货架>-<列><层>`: A-L10 / A-R4。现役货架 A。老名 L10 视为 A-L10, 设备输出一律新名。
- 验证法(可复用于任何批量数据迁移): 改前设备跑 slot_snapshot 打快照 → 迁移 → 改后再打 → slot_snapshot_diff 除名字外逐字段比对。本次 22 账本/22 位姿/44 路径逐点/396 坑位/3 装箱样例 PASS; path_check 44 条一致; /plan/store 老名进新名出; 盘点回归 PASS。
- 对接样例记录是改名前录的(显示 L2/R4), README 与网页已注明。
- poses.yaml 里 A-L5、A-R5 各写了两遍(改名前即如此, YAML 后者覆盖), 未处理。

**Why:** 数据里格口名到处当钥匙, 老名兼容靠入口归一化而不是改 40 处拼文件名代码。
**How to apply:** 真加第二货架(同一台臂): 先验可达性 → scene_params 货架列表化 → 每货架 mid(mid_B) → 双货架碰撞场景 → B 的格口按 `B-L10` 走五步生产。别再写 `[LR]\d+` 正则, 用 slotname.parse。相关 [[cell-interface-layering]]
