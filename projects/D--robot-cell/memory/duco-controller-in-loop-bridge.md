---
name: duco-controller-in-loop-bridge
description: DUCO 真机控制器(仿真模式)接入 AutoDL 仿真的桥接架构、脚本与端口
metadata: 
  node_type: memory
  type: project
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-07-22T07:54:35.030Z
---

把 DUCO 机械臂真机控制器（仿真模式 get_simulation_state=True）的运动数据接入 AutoDL 的 ROS2/Foxglove 仿真，2026-05-27 验证打通。**完整流程参考文档**：`D:\code\duco_sim_bridge\WORKFLOW_real_to_sim.md`(blue-space，git管理；Mac 副本在 ~/Desktop/仿真资料收集/代码/duco_sim_bridge/)——含架构、一次完整操作命令、脚本清单、DUCO API 踩坑、网络排查、AutoDL 仿真栈、中柱可达性结论。新对话优先读它。目标：**运动用真机控制器原生指令（Mac 本地调），可视化/碰撞/规划留在 AutoDL 仿真**。参见 [[sim-as-validation-platform]]、[[ros2-foxglove-setup]]。

**数据流**：真机控制器(192.168.0.20:**7003** Thrift RPC，7000 是网页 HMI) → Mac 用 DUCO API 读 `get_actual_joints_position()` → SSH 隧道转发端口 **9095** → AutoDL 中继节点 → 发布 `/joint_states`(50Hz) → robot_state_publisher → TF → Foxglove。关节名映射 DUCO `joint_1..6` → URDF `arm_1_joint_1..6`(顺序/弧度一致)。只发关节角即可，robot_state_publisher 用 URDF 做 FK，显示天然正确，无需 TCP/基座标定。

**关键脚本**(均在 git 管理的 `~/Desktop/仿真资料收集/代码/duco_sim_bridge/`；注意 `仿真资料收集/` 根目录非 git, `代码/` 才是 git 仓库)：`duco_read_test.py`(只读)、`duco_stream_to_sim.py [hz] [secs]`(流式发送)、`duco_goto.py [j1..j6]`(movej 到目标, 缺省=中间点)、`README.md`。DUCO API 在同级 `代码/RPC_V4.4.0/RPC_Python_V4.4.0/DucoCobotAPI_py源码`，自带 thrift 在其 `lib/`(不用 pip 装)。AutoDL `/root/autodl-tmp/duco_joint_relay.py`(TCP 9095→发 /joint_states，autodl 仓库已提交)。

**RPC 下发运动的前提(踩过的坑, 2026-05-27 验证)**：
1. 仿真模式机器人本就 SR_Enable(6)，无需 power_on/enable。
2. **必须先 `switch_mode(1)` 切自动模式**(手动模式 0 控制权在示教器, 会拒绝运动并关连接)。
3. **运动指令(movej2/movel...)必须传填满字段的 `Op`**, 不能用默认空 `Op()`(字段全 None→控制器解析失败, 报 "TSocket read 0 bytes" 关连接)；用 `Op(0,1,False,0.0,0.0,"",0,1,False,0.0,0.0,"")`(无触发)。文档 develop-v4.3 的 1.3.5 证实 C++ 默认是已初始化的 op_。
4. 长运动用非阻塞 movej2(block=False) + 轮询 `get_noneblock_taskstate(id)`(终态 3..8, 4=ST_Finished)。

**性能瓶颈(2026-05-27)**：每个 DUCO RPC 调用 ~0.8s, 导致轮询只有 ~1.2Hz, Foxglove 显示卡顿。根因是网络：Mac(192.168.31.x)经 Tailscale 访问机械臂(192.168.0.20)，但 `netcheck` 显示 `UDP: false`(网络/全局VPN屏蔽UDP)+附近无DERP(最近丹佛~330ms)，Tailscale 无法直连只能走 SFO 中继(~400ms RTT)。Mac 上还有另一全局VPN/代理(默认路由走utun4, 见198.18.0.1)干扰打洞。**这是网络问题非架构问题**。真正解法：①Mac接入机械臂局域网直访 ②或在能LAN访问机械臂的机器(blue-space Windows子网路由100.106.76.91)上跑采集再转发 ③或关全局VPN+放行UDP让Tailscale直连。**重要踩坑**：中继类方法不能命名 `handle`(覆盖rclpy.Node.handle属性→节点创建崩 `AttributeError:__enter__`)。代码改为本地编辑+scp部署(不再在服务器heredoc/sed直改)。

**LAN采集方案(2026-05-27 选定)**：因 Mac→机械臂经 Tailscale 中继 0.8s/次太慢, 改在能 LAN 直连机械臂的 blue-space(Windows) 上做高频录制。SSH 免密已配好: `ssh 26293@100.106.76.91`(主机名 Blue-Space, 用户 blue-space\26293, Mac id_rsa 公钥已加入其 administrators_authorized_keys, 经 Tailscale)。计划: 在 blue-space 上跑 DUCO 录制(LAN~1ms 密集采样)→取回轨迹文件→AutoDL 仿真端 duco_joint_relay 的 traj 回放播放。SDK 支持 Windows。**已验证(2026-05-27)**：blue-space→机械臂 RPC 延迟 ~44ms/次(Mac 经中继是 800ms, 快18倍), 可轮询 ~23Hz(44ms 是 DUCO 控制器 RPC 固定响应周期~40ms, 非网络, 即轮询天花板; 但23Hz×移动时长=上百点, 够密够顺)。**blue-space 环境**: 用英文/ASCII 路径(中文经SSH命令行会乱码, 但写在脚本文件里经scp传则OK); 代码已同步到 `D:\code`(git仓库, 含 duco_sim_bridge/ 脚本 + RPC_V4.4.0 SDK); DUCO API 已复制成 ASCII 路径 `D:\code\duco_sim_bridge\duco_api`(含DucoCobot.py/gen_py/lib); Python 3.14 (C:\Python314) 需 `pip install six`(thrift依赖)已装。开发方式: Mac本地写英文脚本→scp到 D:/code/duco_sim_bridge/→ssh运行(ASCII命令行)。

**模式互斥**：DUCO 模式下 `joint_state_broadcaster` 须停用(`ros2 control set_controller_state joint_state_broadcaster inactive`)，由中继独占 /joint_states；此时旧 mock 回放(goto_joints/replay_file 走 arm_1_controller)不在 Foxglove 显示。回 mock 回放模式：停发送端 + jsb 设回 active。

**踩坑(2026-06-01): 重启/重起服务后 Foxglove 连杆 link_1~link_6 报黄色三角警告**(悬停提示"数据源未提供参考系 link_1，将使用默认 URDF 变换")。**根因**：DUCO 模式下中继独占 /joint_states，但重启后还没给中继发过任何帧/轨迹 → /joint_states 空 → robot_state_publisher 算不出转动关节连杆的**动态 TF** → Foxglove 找不到 link_1~6 参考系而报警(退回 URDF 零位)。规律：固定关节连杆(base_link/suction_cup_link/suction_tcp/shelf/right_shelf/ground)的变换在 `/tf_static`，一直有，**不报警**；靠转动关节(arm_1_joint_1~6)驱动的 link_1~6 在动态 `/tf`，依赖 /joint_states 有数据。**解法：给中继发任意一帧即可**(单帧 `list[6]` 关节角或一条 `{"traj":...}`，经隧道 9095)，/joint_states 立刻恢复 50Hz、/tf 补齐 link_1~6、报警消失。**诊断命令**：`ros2 topic echo /tf --once`(动态 child_frame 是否含 link_1~6)、`ros2 topic hz /joint_states`(是否 50Hz)、`ros2 topic echo /joint_states --once`(关节名应为 arm_1_joint_1~6，与 RSP 的 URDF 匹配，无前缀错配)。可选根治：中继启动时自动发布一个默认姿态(零位/中间点)，使 /joint_states 永不空，重启后不再报警。

---

**【货架路径库 - 正确路径 + 可复用脚本清单】(2026-06-02 跑完 L7_Left 整格后系统总结，开头因路径找错走了弯路，固化于此)**

**三机地址**：blue-space(Win, LAN直连臂) = `ssh 26293@100.106.76.91`(Tailscale, 不是"blue-space"别名)；AutoDL(仿真栈) = `ssh -p 38814 root@connect.nmb2.seetacloud.com`(端口重启会变)；Mac 本地镜像/编辑源 = `~/Desktop/仿真资料收集/代码/duco_sim_bridge/`(改这里→scp到远程)。开发铁律：**本地写脚本→scp→远程运行**；**中文路径只能写在脚本文件里**(scp UTF-8安全)，命令行走ASCII；**多行 `python -c` 经SSH会被截断→必用脚本文件**；`scp -P <端口>` 端口要放源/目标之前。

**blue-space 目录(都在 `D:\code` git)**：
- `D:\code\` 根 = 流程脚本：`_track_run_tier1.py <path.json> [--out]`(复位MID→稠密入队~80→trackJointMotion连续跑+录制, **执行任意路径的通用执行器**)、`_teach_mid_to_safe.py --safe-from <pose.json> [--out]`(读安全点+2段安全复位 当前→safe→mid+录 mid→safe)、`_teach_safe_to_final.py`、`_save_approach_*.py`(截取接近段, 中文路径内置)、`_save_path_<格口>_*.py`(拼接/存档, 中文路径内置)。
- `D:\code\duco_sim_bridge\` 子目录 = **核心API脚本(开头在这找漏了)**：**`blue_space_record.py j1..j6 [--out]`**(movej2从当前到目标关节角+录制, **种子/任意movej段录制器**)、`blue_space_record_movejpose.py x y z rx ry rz`(movej_pose2到TCP)、`blue_space_record_movel.py`、**`blue_space_state.py`**(只读臂状态)；`duco_api/`(SDK, sys.path插lib/gen_py)；`recordings/`(所有录制json)。
- 真机路径存档 = `D:\Destop\robot_code\轨迹探索\<格口>\<cell>_path_full.json`（2026-07-22 从 `C:\Users\26293\Desktop\robot_code` 迁到 D 盘, 文件夹名就是 Destop 无k; **注意旧 `_save_*.py` 脚本内写死的中文存档路径还是 C 盘旧址, 下次用前须改**）(含 `enqueue_track`少量路点+`recorded_traj`实测+元数据。**真机跑用 enqueue_track 喂trackJointMotion，recorded_traj仅供仿真复验/回放**)。

**AutoDL 目录(`/root/autodl-tmp` git)**：`duco_joint_relay.py`(中继, 听9095)、`collision_check_traj.py <traj.json>`(逐点碰撞, shelf在URDF走自碰撞)、`_select_config*.py`(步骤0: FK已知/邻格构型得TCP→多q_near种子IK→`_manip_score.py`可操作性分)、`_pose_*.py`(解IK+发中继显示某构型)、**`_multi_plan.py [prefix j1..j6]`**(泛化: MoveIt多规划器N候选→`candidate_<prefix>_i.json`)。**rclpy脚本必须先source ROS**：`source /opt/ros/humble/setup.bash && source /root/autodl-tmp/duco_ros2_driver/duco_ros2_driver_V4.2.0/duco_ros2_driver/install/setup.bash`，用系统`python3`；纯socket/json(发中继)用`/root/miniconda3/bin/python3.12`。

**中继(仿真显示)协议(9095)**：发单个`[j1..j6]`(换行结尾)→冻结仿真在该姿态(中继50Hz持续republish)；发`{"traj":[[t,j1..j6],...]}`→回放整条。在AutoDL本机连`127.0.0.1:9095`，Mac经隧道。

**每步用哪个脚本(新格口照搬)**：
0. **选构型**(AutoDL,ROS)：邻格构型FK+货架标定行/列偏移(货架标定信息.md, 行高196.347mm/列±362.544mm)得本格TCP → `_select_config*.py`枚举种子+评分 → 选PASS(minσ≥0.12且w角≥1.0, +Y插入优先) → `_pose_*.py`仿真看 → 写`calibrated_poses.yaml`。
1. **种子**(blue-space)：`blue_space_record.py <MID>`复位 → `blue_space_record.py <grasp> --out seed_<cell>.json`录 movej中间点→抓取。
2. **测碰撞**(AutoDL)：scp种子→`collision_check_traj.py seed_<cell>.json`。
3a. **无碰/要选形状→全局规划(零示教, =L7_Left)**：`_multi_plan.py <cell> <grasp_j1..j6>`→候选; 各条发中继`{"traj"}`回放给用户挑; 选定条scp到blue-space→`_track_run_tier1.py candidate_<cell>_N.json`执行录制→scp回→`collision_check_traj.py`→`_save_path_<cell>_*.py`存档。
3b. **撞了/要加余量→示教(=L6_Left/L6_Right/L7_Left加余量)**：中继冻结各帧选退点; 用户jog真机到余量更大的安全姿态; `blue_space_state.py`或单行读关节角存`_safe_pose_<cell>.json`; `_teach_mid_to_safe.py --safe-from`录mid→safe + `blue_space_record.py <grasp>`录safe→final; 拼接+`collision_check_traj.py`复验; 存档。(分段保余量有停顿 vs trackJointMotion连续削余量, 见 [[shelf-path-debug-workflow]])
- 验证只能用控制器实录轨迹, 不能用lerp插值替, 见 [[controller-record-not-interpolation]]。

已完成格口(2026-06-02): L6_Left、L6_Right、L7_Left、L8_Left、L8_Right (5/16)。
