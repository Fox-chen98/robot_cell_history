---
name: no-controller-while-user-runs
description: "用户在跑真机命令期间, AI 绝不能碰控制器(干跑/sim_mode/探测都会切模式打断真机运动); 2026-09-18 事故"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-09-18T02:53:53.403Z
---

用户在真机跑 flow/act 命令的时候, 我为了"顺手"干跑另一个坑位, 跑了 `act.sh ... --dry`, 它把控制器切成仿真模式, 用户的真机运动当场停止(持货悬在半路)。用户: "你直接给我命令呀, 你是不是刚才修改了东西, 导致我的运动停止了"。

**Why:** 干跑/横向探测/plan_smooth/go_home 全都要控制器仿真模式, 切模式对正在执行的真机程序就是急停。控制器只有一个, 谁在用谁独占。

**How to apply:**
- 给了用户真机命令之后, 到用户说"跑完了/臂空闲"之前, 不跑任何会碰控制器的命令(--dry, sim_mode, lateral_probe, plan_smooth, run_plan, go_home, check_motion, fly_probe)。只读的 read_pose/日志可以。
- 需要干跑时先问"臂现在空闲吗", 得到肯定再动。
- 部署(deploy_cell)和重启服务也尽量避开用户真机流程中途(常驻服务重启会让网页任务断)。
相关 [[sim-is-ai-sandbox]] [[read-script-before-advising]]
