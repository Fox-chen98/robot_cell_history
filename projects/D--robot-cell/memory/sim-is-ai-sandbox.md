---
name: sim-is-ai-sandbox
description: "分工约定: 用户只跑真机; 控制器仿真模式是AI的验证沙盘, AI用完必须自己切回真实模式; 仿真回执对用户没有直观感受"
metadata:
  type: feedback
---

**2026-09-02 用户定案**: "以后我跑真机, 仿真环境供你自己验证"。用户对仿真干跑的反馈是"就是一段文字, 没有任何直观感受", 要体会动作层/回执必须真机。

**Why:** 用户的理解方式是现场看臂动+看终端回执对照; 仿真只对AI有价值(抓奇异/可达/回归, 不动真机不需AutoDL)。控制器模式是共享状态, AI切到仿真后忘了切回, 用户会被"控制器在仿真模式"挡住。
**How to apply:** act.sh --dry / probe_pits.sh 结束自动 sim_mode off(已固化)。给用户的命令一律真机版(不带--dry); AI自己验证用--dry且验证完确认模式已回真实。相关: [[integration-seam-analysis]] [[read-script-before-advising]]

**2026-09-03 事故补充**: 机器人未使能时切仿真, 控制器报错但仿真标志仍变True(实际真机), 干跑序列在真机执行进了格口(用户急停, 无损). 修: sim_mode.py切前使能+切后比对新增错误; 调用方pipefail. 铁律: 切仿真必须自证成功(标志+无新错误), 不能只信 get_simulation_state().
