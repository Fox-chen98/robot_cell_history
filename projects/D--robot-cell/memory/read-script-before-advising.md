---
name: read-script-before-advising
description: "给真机运动类指引前必须先读脚本本身,不能靠能力目录一行摘要;go_home.sh真实模式下拒动只刷显示"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-08-21T06:47:43.310Z
---

给用户"跑哪个脚本让真机动"的指引前,先读该脚本的分支逻辑,再下结论。

**Why:** 2026-08-21 我凭能力目录摘要"控制器实跑"告诉用户 `go_home.sh` 能让真机回 home,实际脚本在真实模式下主动拒绝运动只刷显示(安全设计),用户跑了没反应,追问"为什么给错了"。真机回命名位姿的正确链是 sim_mode on→check_motion→sim_mode off→run_real(同 handeye_try 内部)。

**How to apply:** 涉及真机/控制器的脚本,凡要告诉用户"会发生什么",grep 一下它的 abort/拒绝/模式分支再说;能力目录描述有歧义就顺手改准。相关: [[controller-record-not-interpolation]]

**2026-09-15 又犯一次(用户纠正)**: 要切控制器自动模式, 现成命令 `scripts/check_cell.sh opmode auto|manual|status` 早就有, 我只查了能力目录和 scripts/arm/ 就写了新脚本 op_mode.sh(已删). 教训: 找命令时除了能力目录, 还要 grep 整个 scripts/ 的用法头(`grep -rn "关键词" scripts/*.sh`)和记忆文件; 能力目录一行缺了子命令要顺手补全(已补 opmode).
