---
name: teach-replay-pipeline
description: 示教录制→转换→回放工作流、conda环境、点位角色映射
metadata:
  type: project
---

机械臂"示教录制轨迹并回放"功能（2026-05 进行中）。

**conda 环境**：代码必须在 conda `robot` 环境跑，python 路径
`C:\Users\26293\.conda\envs\robot\python.exe`（thrift 链依赖 `six` 等，系统默认 python 缺）。
机械臂 RPC: 192.168.0.20:7003。

**三段工作流**：
1. `tools/teach_record_trajectory.py` —— 纯只读采样（不控制机器人，用户在示教器牵引拖动）。回车开始，`q` 结束。实测自由跑采样率≈11Hz。输出 `recordings/teach_<ts>.csv/.json`。
2. `tools/teach_to_trajectory.py` —— CSV→回放YAML。`--dedup --min-delta 0.001`（≈0.057°，正好卡在停顿抖动之上、真实运动之下）`--reverse` 反转点序。
3. `tools/run_moveit_trajectory.py` —— 现成回放工具（trackEnqueue+trackJointMotion），勿对已反转YAML再加 `--reverse`。

**点位角色映射（容易搞混）**：`scan_position`(waypoints.yaml) = 起始点位；用户先把机器人摆到的"当前在线位姿/初始位姿"(J1≈135.76°) = 目标点位。用户从目标拖向 scan 录制，再 `--reverse` 得到 scan→目标 的回放轨迹。

2026-05-18 已用测试数据全链路验证成功（起点偏差0.00°，精确到达目标）。注意 155435 那次测试**没真正拖到 scan_position**，仅验证管线；真实 scan 轨迹待正式录制。后续清洗策略（平滑/抽稀）待分析真实数据再定。
