---
name: shelf-center-unreachable-zone
description: 货架中柱附近是机械臂可达盲区——movel/movej 都到不了，是固有运动学极限
metadata: 
  node_type: memory
  type: project
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
---

DUCO GCR10-1300 当前布局下，**在"面朝货架"姿态下**货架中柱区域很难覆盖（2026-05-27 初步测试，**尚未严格证明"不可达"**，勿过度断言）。参见 [[货架标定信息]]、[[duco-controller-in-loop-bridge]]。

**确凿部分**：固定"面朝货架"姿态 + 直线(movel)约束下，朝中柱方向撞奇异点——L6_Left(X=−383) movel +X 止于 X=−180；L6_Right(X=+307) movel −X 止于 X=+112。这只对"该姿态的直线运动"成立。

**MoveIt IK 系统验证(2026-05-27)**：在 AutoDL 用 /compute_fk + /compute_ik (脚本 /root/autodl-tmp/moveit_reach_check.py 扫 X、moveit_reach_tilt.py 扫朝向；suction_tcp, pedestal_link 系) 严谨判定：
- **严格垂直货架朝向**(L6_Left 朝向 quat≈(0,0.705,0.709,0))下，IK 仅存在到 X≈−0.15m，X≥−0.10(含中柱 X=0)**无解**(NO_IK_SOLUTION) → 这个朝向下中柱确实够不到。
- **但放宽朝向即可达**：中柱 X=0 处，**yaw 偏摆约 −15° 就有 IK 解**(±20/30/40°也行；yaw 5°/10°仍无解，~15°是门槛)；pitch 需 ~40°。

**结论(修正之前的过度断言)**：中柱**不是不可达**，是被"严格垂直"约束卡住；**允许~15°偏摆(吸盘稍斜指中柱)即可达**。直觉上中柱在基座正前方、强行正对会陷奇异，偏个角度构型就松开。

**How to apply**：要覆盖中柱/内侧区，别强求严格垂直，给末端~15°偏摆余量即可。待验证：①真机 movej_pose2 带15°yaw到中柱;②加 avoid_collisions=True 看会不会撞中柱结构。X 系 DUCO TCP≈标定基座系(L6_Left DUCO X=−382.6≈标定−383；MoveIt suction_tcp X=−331)。
