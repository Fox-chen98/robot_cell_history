---
name: local-sim-wsl
description: "2026-10-29 AutoDL 仿真栈已搬到本机 WSL2(Ubuntu-22.04): sim_stack.sh 管理, Foxglove ws://127.0.0.1:8766(8765 被百度输入法占), 判卷与 AutoDL 一致已验证"
metadata:
  node_type: memory
  type: project
  originSessionId: 600697e2-60a3-4d18-a896-189ef5a5ce1b
  modified: 2026-10-29T08:27:19.356Z
---

MoveIt/判卷/Foxglove 仿真栈 2026-10-29 起在 blue-space 本机 WSL2 里(用户 robot, 根目录 /home/robot/sim), 取代 AutoDL。详见 docs/交接整理/仿真环境本机化记录.md。

- 管理: `wsl -d Ubuntu-22.04 -- bash /mnt/d/robot_cell/scripts/serverside/stack/sim_stack.sh deploy|start|stop|restart|status`; 批量判卷 `scripts/serverside/judge_batch.sh`。
- Foxglove: `ws://127.0.0.1:8766`(8765 被 Windows 上百度输入法占用, 连到输入法上 → bridge 改 8766); 参考系 pedestal_link; URDF `http://localhost:9090/gcr10_1300.urdf`; Mesh up axis 必须 Z-up(否则末端与手腕错位); 主题里手动打开 /scene_overlay_markers 和 /tool_collision_markers。用户 10-29 已目视确认正常。
- 一致性已验: 44 条生产路径零碰撞; 495 条筛查录制自碰撞统计与 AutoDL 完全相同; 09-18 真撞录制 link_2↔link_4 @J3 −164.9° 相同。
- 仍待: 规划/判卷类 .sh(仍 ssh autodl + /usr/bin/python3 写法) 逐个本机化并接进工具箱; 规划质量验证。

**Why:** 用户目标是"本机环境和效果与 AutoDL 完全一致", 以便手眼重标(巡拍判碰撞)和以后路径规划。

**How to apply:** 不要再让用户开 AutoDL, 除非本机结果与存档对不上需要两边对跑; WSL 命令从 PowerShell 跑时 $变量会被 PowerShell 吃掉, 复杂命令写成脚本文件再 `wsl -- bash 文件`。相关: [[deploy-new-site-plan]] [[controller-record-not-interpolation]]
