---
name: project-handeye-calibration
description: 用户当前在做 Gemini335 相机 + DucoCobot 机械臂的手眼标定，代码移植自阿凯爱玩机器人原项目（原版面向 xCoreSDK 机械臂）
metadata: 
  node_type: memory
  type: project
  originSessionId: 8c4f48d0-6baf-4e23-952d-34665af120de
---

用户拥有**两台不同的机械臂**：xCoreSDK 系列（罗博医疗/罗博医研类）和 DucoCobot（达明/Duco 类）。手眼标定脚本最初是给 xCoreSDK 那台用的（`handeye_calibration_sampling.py`，RPY 欧拉角约定），后移植到 DucoCobot 得到 `handeye_calibration_ducocobot.py`。

**Why:** xCoreSDK 那台已经在 RPY 约定下能正常工作，所以原脚本是稳的。移植到 DucoCobot 时，位姿读取/发送接口换成了 `DucoCobot.get_tcp_pose()` / `movej_pose2()`，但脚本中处理 (rx, ry, rz) → 旋转矩阵的代码 ([L462-467](xcoresdk_python-v0.6.0/example/handeye_calibration_ducocobot.py#L462-L467)) 仍沿用原版的 `Pose.set_euler_angle`（RPY）。DucoCobot SDK 文档把这三个量描述为 "Rx, Ry, Rz" — 该术语在协作臂里有时指旋转向量 (UR/AUBO 风格)，有时指 RPY 欧拉角 — 需要经验性验证才能确认。

**结论（2026-05-26 已验证）：RPY 约定是正确的，隐患排除。** 用户用 `handeye_calibration_ducocobot_v2.py`（手动示教版，按 RPY 处理 TCP 位姿）实跑 16 组数据，TSAI 标定一致性误差为：位置平均 2.16mm / 最大 3.34mm，姿态平均 0.227° / 最大 0.503°。姿态误差若约定搞反会是几十度量级，0.2° 量级直接证明把 DucoCobot 的 (rx,ry,rz) 当 RPY 欧拉角处理是对的。标定结果存于 `handeye_data_ducocobot/T_wrist2cam.npy`（平移 x=30.3 y=-112.4 z=-451.6 mm，相对 TCP `tool_0526_v1`，z 偏大属正常）。

**How to apply:** 该约定不要再当作待解 bug；后续 DucoCobot 位姿↔矩阵转换继续沿用 RPY (Z-Y-X intrinsic)。验证脚本 `verify_pose_convention.py` 已不必再跑。讨论标定问题时仍要区分是哪台机械臂（xCoreSDK vs DucoCobot）。

相关：[[memory-handeye-calibration-issues]]（如果之后建立标定脚本问题清单）
