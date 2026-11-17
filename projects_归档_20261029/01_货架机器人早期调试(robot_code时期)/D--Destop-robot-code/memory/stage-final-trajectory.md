---
name: stage-final-trajectory
description: midListingStatus↔L6_left上架点 阶段性最终回放轨迹与命令
metadata:
  type: project
---

机械臂 midListingStatus(上架中间点) ↔ listingPoint(L6_left上架点) 平滑回放，阶段性定稿于 2026-05-19。

**最终交付文件**（recordings/）：
- `stage_final_L6left_to_mid.yaml` — L6_left → 中间上架点（356点）
- `stage_final_mid_to_L6left.yaml` — 中间上架点 → L6_left（356点，反向）
- 起=L6_left `[133.88,87.84,-116.58,28.28,-133.86,0.06]°`，终=midListingStatus `[-2.63,26.98,-98.40,-3.77,90.01,0.06]°`

**生成链路**：原始手拖 CSV `teach_20260518_190443.csv`(2355点) → deglitch+smooth(w15)+resample → `listing_w15.yaml`(400点,安全稠密源) → RDP(ε=2°)抽16关键帧 + 直线加密 → `listing_rdp_dense.yaml`(356点,偏差≤1.44°) → replay_with_marks 标7处拐角 → retouch_marks 局部圆角(window22) → `listing_rdp_dense_fillet.yaml`(再偏≤1.26°,总≤~2.7°,安全走廊内) → 复制为 stage_final_*。

**回放命令**（机器人须在该方向起点，启动偏差必须≈0°才按y，否则N）：
```
python tools/run_moveit_trajectory.py recordings/stage_final_L6left_to_mid.yaml --speed 0.4 --acc 0.25
python tools/run_moveit_trajectory.py recordings/stage_final_mid_to_L6left.yaml --speed 0.4 --acc 0.25
```
不加 --reverse（文件已是成品方向）。conda robot 环境，见 [[teach-replay-pipeline]]。

**已知待优化（未做完）**：到 L6_left 终点最后一小段有顿挫——该段本身为避货架弯曲(~7.4°)不能拉直；下一步先试降 acc(已含命令)，不够再对终点段做有界局部圆角。J1方向约束见 [[j1-safe-direction]]。

**关键技术结论**：trackJointMotion 需"够密+干净无反向+有界"输入(RDP去脏+直线加密正好满足)；RPC顺序movej2无法融合(无预读)；safety_state=5=SS_RUN正常。
