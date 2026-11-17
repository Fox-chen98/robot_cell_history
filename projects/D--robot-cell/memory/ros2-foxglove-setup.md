# ROS2 + MoveIt + Foxglove 调试环境

## 服务器信息

| 项目 | 值 |
|------|-----|
| 平台 | AutoDL 云 GPU |
| 系统 | Ubuntu 22.04 LTS (容器) |
| 主机 | connect.nmb2.seetacloud.com |
| SSH 端口 | 38814 (每次重建可能变化，需检查 AutoDL 控制台) |
| 用户 | root |
| GPU | RTX 4090 24GB |
| 数据盘 | /root/autodl-tmp (50GB，持久化) |
| Python | /root/miniconda3/bin/python3.12 |

## 已安装的软件

- ROS2 Humble Desktop (`/opt/ros/humble/`)
- MoveIt2 2.5.9 (`ros-humble-moveit`)
- Foxglove Bridge (`ros-humble-foxglove-bridge`)
- ros2_control + ros2_controllers
- 环境已写入 `/root/.bashrc`: `source /opt/ros/humble/setup.bash`

## 机械臂项目

- **机械臂型号**: DUCO GCR10-1300
- **驱动包位置**: `/root/autodl-tmp/duco_ros2_driver/duco_ros2_driver_V4.2.0/duco_ros2_driver/`
- **MoveIt 配置包**: `duco_gcr10_1300_moveit_config`
- **工作空间已编译**: `duco_support` + `duco_gcr10_1300_moveit_config`
- **原始 URDF**: `/root/autodl-tmp/duco_ros2_driver/.../src/duco_support/urdf/duco_gcr10_1300.urdf`
- **Mesh 文件**: `/root/autodl-tmp/duco_ros2_driver/.../src/duco_support/meshes/GCR10_1300/*.stl` (base_link ~ link_6)

## 启动方式

### 一键启动（服务器端）

```bash
ssh -p 38814 root@connect.nmb2.seetacloud.com "nohup bash /root/autodl-tmp/start_foxglove.sh > /root/autodl-tmp/startup.log 2>&1 &"
```

启动脚本 `/root/autodl-tmp/start_foxglove.sh` 会自动执行：
1. source ROS2 和工作空间环境
2. 启动 HTTP 服务器 (端口 9090，提供 URDF 和 mesh 文件)
3. 启动 `foxglove_demo.launch.py`（包含 robot_state_publisher + move_group + ros2_control + foxglove_bridge）

等待约 10 秒后检查是否就绪：
```bash
ssh -p 38814 root@connect.nmb2.seetacloud.com "strings /root/autodl-tmp/startup.log | grep -E 'You can start planning|Server listening'"
```
应看到 `Server listening on port 8765` 和 `You can start planning now!`

### 本地 SSH 隧道（一条命令，合并两个端口）

```bash
ssh -CNg -L 8765:127.0.0.1:8765 -L 9090:127.0.0.1:9090 root@connect.nmb2.seetacloud.com -p 38814
```

- 8765: Foxglove Bridge WebSocket
- 9090: HTTP 服务器（URDF + STL mesh 文件）

此命令需在后台运行（加 `&` 或用 `run_in_background`）。

### Foxglove Desktop 连接

1. 打开 Foxglove Studio（已安装在 `/Applications/Foxglove.app`）
2. 连接 `ws://localhost:8765`
3. 添加 **三维 (3D)** 面板
4. **关键设置**: 3D 面板 → 左侧 **场景** → **Mesh up axis** 改为 **Z-up**（不设此项机械臂 mesh 会错位）
5. 左侧 **自定义图层** → 点 **+** → 添加 **URDF**
6. Source: **URL** → 填 `http://localhost:9090/gcr10_1300.urdf`

## 重要注意事项

### Mesh up axis 必须设为 Z-up
Foxglove 和 RViz 对 STL 坐标轴默认不同。不设置会导致 base_link/link_1 和 link_5/link_6 之间出现间隙，mesh 错位。这是 Foxglove 的已知问题。

### URDF 通过 HTTP URL 加载（非 Topic）
`/robot_description` 话题使用 TRANSIENT_LOCAL QoS，foxglove_bridge 无法正常中继。因此 URDF 通过 HTTP URL 加载，mesh 路径已从 `package://duco_support/` 替换为 `http://localhost:9090/`。

### HTTP 提供的 URDF 文件
- 路径: `/root/autodl-tmp/web_serve/gcr10_1300.urdf`
- Mesh 目录: `/root/autodl-tmp/web_serve/meshes/GCR10_1300/`
- 这些是原始 `duco_support` 包中文件的副本，仅替换了 mesh 路径前缀

### foxglove_demo.launch.py
自定义 launch 文件位于: `.../src/duco_gcr10_1300_moveit_config/launch/foxglove_demo.launch.py`
- 不启动 RViz（无头模式）
- 不启动 duco_ros_driver（不需要真实机械臂）
- 使用 `mock_components/GenericSystem` 模拟硬件
- 包含 foxglove_bridge（端口 8765，asset_uri_allowlist 允许 package://）

### 停止所有服务
```bash
ssh -p 38814 root@connect.nmb2.seetacloud.com "killall -9 foxglove_bridge ros2_control_node move_group robot_state_publisher spawner static_transform_publisher 2>/dev/null; kill \$(pgrep -f 'http.server 9090') 2>/dev/null; echo done"
```

## 完整启动流程（给模型执行用）

当用户说"启动 Foxglove 调试环境"或类似指令时，按以下顺序执行：

```
步骤 1: 启动服务器端服务
ssh -p 38814 root@connect.nmb2.seetacloud.com "nohup bash /root/autodl-tmp/start_foxglove.sh > /root/autodl-tmp/startup.log 2>&1 &"
等待 10 秒

步骤 2: 验证服务就绪
ssh -p 38814 root@connect.nmb2.seetacloud.com "strings /root/autodl-tmp/startup.log | grep -E 'You can start planning|Server listening'"

步骤 3: 建立本地 SSH 隧道（后台运行）
ssh -CNg -L 8765:127.0.0.1:8765 -L 9090:127.0.0.1:9090 root@connect.nmb2.seetacloud.com -p 38814

步骤 4: 打开 Foxglove Desktop
open /Applications/Foxglove.app

步骤 5: 提示用户手动操作
- 连接 ws://localhost:8765
- 添加 3D 面板
- 场景 → Mesh up axis → Z-up
- 自定义图层 → URDF → URL: http://localhost:9090/gcr10_1300.urdf
```

## 学术加速（可选）

AutoDL 访问 GitHub/HuggingFace 慢时，在命令前加：
```bash
ssh -p 38814 root@connect.nmb2.seetacloud.com "source /etc/network_turbo && <command>"
```
