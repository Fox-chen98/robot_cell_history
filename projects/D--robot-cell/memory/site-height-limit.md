---
name: site-height-limit
description: "冷库净高 2.1m, 路径限高定 1.9m(离地, 底座 0.5); 现役 12 条路径超高, 现场规划时加天花板重做; A-L6/A-L2 已验证能压到 1.9 以内"
metadata:
  node_type: memory
  type: project
  originSessionId: 600697e2-60a3-4d18-a896-189ef5a5ce1b
  modified: 2026-11-06T07:26:55.525Z
---

2026-11-06 用户: 冷库高 2.1m, 限高定 1.9m(留 20cm 给安装误差/路径偏差/管线包)。待现场确认顶上有没有冷风机/灯具等吊挂物(有就要从最低点算)。

摸底(data/stocktake/path_height_check.json, 算吸盘端+法兰端, 没算肘部): 超 1.9m 的 12 条 = A-L2~L6 去回(2.10~2.37m, 工具翻转甩过头顶) + A-L12 去回(1.91)。超 1.8m 再加 L9/L11/R12。

可行性(MoveIt 只规划未实跑, data/plans/ceiling/): `scripts/serverside/ceiling.py add 1.9` 加天花板后 A-L6/A-L2 去回 8 候选成功 5~7 条, 最高 1.69~1.80m。代价: 原始路程 A-L6 9.8→13.6~15.3rad(+40~55%), A-L2 回 10.6→15.2 / 去 20.6→15.5(反而短)。

**Why:** 到现场货架/臂要重标, 路径本来全要重规划, 现在只验证可行性, 不全量做。

2026-11-06 全量试跑(data/plans/path_best, 未入库): 12 条全部判卷通过, 最高 1.63~1.81m, 飞行 5.7~12.4s; 但 11 条各留 1 处停顿, 第 1 轮后加跑 5 轮(每条 24 候选)没再改善, 现场再做时别指望加候选解决, 要看停顿处是否翻转必经.

**How to apply:** 现场部署第 8 步规划前先 `ceiling.py add 1.9`(只改运行中规划场景, 重启仿真栈就没了; 判卷也会算它), 再跑 path_plan; 还差: 确认后续实跑判卷/试飞、肘部高度、节拍影响。相关 [[deploy-new-site-plan]]
