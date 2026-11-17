---
name: shelf-path-progress
description: 货架16格路径库进度与L3_Left候选构型/待办交接(2026-06-04)
metadata: 
  node_type: memory
  type: project
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
---

货架取放路径库进度（2026-06-04 交接，详见 [[shelf-path-debug-workflow]] / [[duco-controller-in-loop-bridge]]）。

**已完成 10/16 + L4_Right加余量版**：L4_L/R、L5_L/R、L6_L/R、L7_L/R、L8_L/R（L4–L8 五行）全部两台机 git 提交（blue-space `D:\code` + AutoDL `/root/autodl-tmp`）；`calibrated_poses.yaml` 含这 10 格构型 + 安全点；路径存档在 `轨迹探索\<格口>\`。剩 **L1~L3 共 6 格**（最低三行，最难，构型贴关节极限）。

**混合套路（L4 验证，重要）**：低难格直达 movej 种子常广撞（深格连 link_2 上臂/link_3-6 前臂都撞）。三条路按需组合：①纯 MoveIt 多候选（`_multi_plan.py` 部分规划器成功）→选条 trackJointMotion 执行（L4_Right 一次干净 152/152）；②若末段插入残留几点（trackJointMotion 融合抄近）→**退到候选靠后某点示教安全点对齐直插**清残留（L4_Left）；③纯人工示教单/双安全点（L5，左列无 safe_center）；右列可复用 L8R 的 `safe_center`。加余量=再退点示教一个 TCP 退后的安全点（可能引入末段 1 点→再加预备点 safe2 清零，L4_R/L5_R）。

**L3_Left 进行中（步骤0已选构型，未录路径）**：左格→左摆 PASS。穷举（`_enum_ik.py`）得 4 个 PASS：
- 左摆肘上#2 `[130.4,166,-147,-19,-130,-0.3]`：J2=166° 抬肩近极限，+Y=0.61。
- 左摆肘下#3 `[130.4,33,147,180,-130,-0.3]`：种子**已测→整条前臂 link3-6+吸盘全撞**，要重示教，兜底用。
- **#1(首选) `[130.36,-6.04,142.06,43.59,130.31,179.7]°` rad `[2.275259,-0.105365,2.479397,0.76087,2.274346,3.136408]`**：腕翻转+肩中性(J2=-6°,避 link_2)，minσ最高0.184，**未测种子**。
- #4 `[130.4,124,-142,-163,130,180]`：抬肩+腕翻转。

用户倾向 #1 与肘下。**下一步**：用 **#1** 录种子测碰撞；撞了走混合套路。新对话先重连 AutoDL(`ssh -p 38814 root@connect.nmb2.seetacloud.com`，重启 `start_foxglove.sh`+停jsb+起 `duco_joint_relay.py`)+建本地隧道(8765/9090/9095)，确认臂 `sim_mode=True`。
