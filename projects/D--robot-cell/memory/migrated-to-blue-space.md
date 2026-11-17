---
name: migrated-to-blue-space
description: 2026-10-29 主线 Claude Code 从 Mac 迁到 blue-space 本机 D:\robot_cell; 旧记忆多为 Mac 视角(ssh 到设备), 按项目 CLAUDE.md 顶部换算表理解
metadata:
  type: project
---

2026-10-29 起主线在 blue-space(Windows 设备电脑)的 `D:\robot_cell` 运行 Claude Code; Mac 停用, AutoDL 已关停。主线长对话(9953535e…)从 Mac 原样搬来, 工作目录字段改写为 D:\robot_cell。

**Why:** 交接——设备、代码、对话都集中到公司电脑, 便于他人接手。
**How to apply:** 读到旧记忆/对话里的 `ssh 26293@100.106.76.91`、`scripts/*.sh`、`/usr/bin/python3`、`deploy_cell.sh`、`git push origin` 等, 都是"从 Mac 远程操作设备"的写法, 现在直接在本机执行(换算表在项目 CLAUDE.md 顶部"已从 Mac 迁到 blue-space"一节)。deploy 本机化、两目录合并、仓库备份方案尚未做, 动之前先问用户。迁移步骤记录在 docs/交接整理/Claude对话迁移.md。相关: [[ssh-controlmaster-hosting-pitfall]] [[sim-x-4070s-setup]]

**过渡期**: Mac 未关, blue-space 可 `ssh mac`(免密, Tailscale 100.67.85.97, 用户 chen)登录 Mac 取文件/跑 Mac 专有工具; 以 blue-space 为主、同一时间只在一边干活、代码走 git(Mac 的 origin=D:\robot_cell)、两边对话已分叉需互通进度。用户说停用时: 关 Mac 远程登录 + 删 authorized_keys 里 blue-space-to-mac + 删 blue-space 的 Host mac。

**2026-10-29 运行目录已并入主仓库**: 设备直接从 D:\robot_cell 运行(3 个 Windows 服务 binPath 与 3 个计划任务已改指新目录), 不再 deploy; 原 scripts/bluespace/<x> 现在仓库根 actions/flows/services/hardware/tools/...; 旧目录改名 D:\Destop\robot_cell_旧运行目录_20261029 只作备份。记录与验证进度: docs/交接整理/运行目录合并记录.md。
