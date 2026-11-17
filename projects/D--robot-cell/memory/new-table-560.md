---
name: new-table-560
description: "新工作台定 70×40 cm 离地 56 cm(2026-11-05), 到货后要改写死的桌面高度 0.064→0.060 三处并重标桌子"
metadata:
  node_type: memory
  type: project
  originSessionId: 600697e2-60a3-4d18-a896-189ef5a5ce1b
  modified: 2026-11-05T07:50:12.105Z
---

2026-11-05 用户定新上苗机工作台: 台面 70×40 cm(原 71×39.5), 离地 56 cm(原 56.4), 出苗口离台面 10 cm、内宽 24 cm、靠机械臂一侧离近边 7 cm(11-05 晚现机挪后 100 盒全抓起, 最远离底座 1.095m)。早先依据: 控制器仿真实跑可抓区 + 11-05 现机 30 盒落点实测全抓起(data/landing/, scripts/landing_stats.py / table_overlay.py; 曾想挪到 3 cm, 实测证明不必, 且挪多会从近边掉)。要求写在 docs/硬件清单.xlsx 上苗机行 + docs/硬件资料/上苗机出苗口示意图.svg。

**Why:** 用户要凑整数给厂家; 桌高 0.4 cm 差异对抓取覆盖略有利。

**How to apply:** 新桌到货部署时: ①"桌面在基座系高度" TABLE_Z 0.064 写死在 actions/table_guard.py、tools/grasp/pick_one_box.py、tools/grasp/step1_target.py, 改 0.060(以实测为准) ②scene_params table.size 改 [0.70, 0.40, 0.56] 并重标桌子码牌 ③table_guard 的 Y_OUTLET/落料带按新出苗口位置核对。相关 [[deploy-new-site-plan]]
