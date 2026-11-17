---
name: servers
description: 服务器总览与对照表——中转服务器 relay 与 AutoDL GPU 服务器的连接方式、用途区分
metadata: 
  node_type: memory
  type: reference
  originSessionId: 59d4997a-48fd-44bb-9204-cce33cc52aa7
---

**用户的服务器清单（统一总览，方便区分）**

| 项目 | ① 中转服务器 | ② AutoDL GPU 服务器 |
|------|-------------|---------------------|
| 代号/别名 | `relay` | AutoDL / GPU / 仿真机 |
| 主机 | `199.180.117.149` | `connect.nmb2.seetacloud.com` |
| 端口 | `22`（固定） | 常变（租用实例频繁更换；唯一改动点=`~/.ssh/config` 的 `autodl` 条目，改完跑 restore_autodl.sh） |
| 用户 | `root` | `root` |
| 主机名 | `lucid-walk-1.localdomain` | — |
| 系统 | Linux RHEL 9 系（内核 5.14.0-611.55.1.el9_7），x86_64 | Ubuntu 22.04 LTS（容器） |
| 登录方式 | **SSH 密钥免密**（`ssh relay`，密码为备用后路，不存记忆） | 密码登录 |
| 用途 | 中转 / 跳板 | GPU 训练 + 机械臂 ROS2/MoveIt/Foxglove 仿真 |

**区分口径**：说「中转 / relay」= ①；说「AutoDL / GPU / 仿真」= ②。切勿混淆。

**连接示例**：
- 中转：`ssh relay "命令"`（已配 `~/.ssh/config` 别名，含保活参数）
- AutoDL：`ssh autodl "命令"`（别名，端口以 ~/.ssh/config 为准）；Python 用 `/root/miniconda3/bin/python3.12`，数据盘 `/root/autodl-tmp`

**2026-08-13 决策**：曾讨论把仿真栈 Docker 迁到 Mac 本地（负载纯 CPU 可行，未知数=duco 驱动 arm64 编译），用户决定**维持 AutoDL 现状**——换机成本已被骨架压到约 2 分钟，暂不折腾。仿真用无卡模式省钱。

AutoDL 的详细环境与仿真启动手册见 [[ros2-foxglove-setup]]。本机通过 Tailscale 访问机械臂见 [[robot-arm-tailscale-access]]。
