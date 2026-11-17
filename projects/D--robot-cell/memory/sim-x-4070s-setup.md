---
name: sim-x-4070s-setup
description: robocenter_x 仿真支线改用自有 4070S 机器(sim_x)而非租 AutoDL; 接入方式/网络现状/Isaac Sim 4.5 决定(2026-08-24)
metadata: 
  node_type: memory
  type: project
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-08-24T03:23:06.270Z
---

2026-08-24 决定: Isaac Sim 支线不租 AutoDL, 用用户自有 RTX 4070 SUPER 12GB 机器(Ubuntu 22.04.5, 31GB RAM, 驱动 560, 主机名 Agent, 在**家里**网络)。Mac 别名 `ssh sim_x`(Tailscale 100.123.241.105, 用户 chen, 免密 sudo)。

**Isaac Sim 选 4.5.0**(conda env `isaac`, py3.10, pip 装 `isaacsim[all,extscache]==4.5.0` 自 pypi.nvidia.com): 最新是 6.0.1(2026-06), 但 5.x/6.x 官方最低 RTX4080 16GB + 驱动≥580/595, 4.5 是唯一官方覆盖这台机器的版本; 4.5 文档随 6.1 下线→要离线存一份。

**网络**(术语: 公司=Mac 所在网, 家里=4070S 所在网): 公司↔家里只能香港中继 300~600ms(稳); 公司三层 NAT(光猫→iStoreOS→小米)对称型无 IPv6, 家里 UPnP 映射在 CGNAT 后对外不可达(用 tcpdump 实证; 早先"中转服务器探到了"是 wc -l 空行假象——**macOS 无 timeout 命令**, 抓包脚本要注意)。Mac 切手机热点可直连 56ms(热点侧 NAT 宽松)。根治=公司光猫开 IPv6/桥接(iStoreOS wan6 已配好)。工作方式: 开发/无头仿真走公司网, 看桌面切热点。

**已固化**: Mac LaunchDaemon `local.tailscale-route-fix`(小火箭 TUN 抢 100.64/10 路由, 每 60s 补回 utun); 小火箭规则 100.64.0.0/10 与 112.87.195.138 DIRECT; iStoreOS HomeProxy 改仅 Redirect TCP + 直连列表; 4070S: openssh + Sunshine 用户服务(网页 47990 账号 chen)+ Moonlight 已配对(1080p/HEVC/≤15Mbps)。

**资产**: robocenter_x/inherited 已同步到主线 ddc7149(手眼/TCP 账本/内参/mesh 真身/urdf); 4070S 上副本 ~/robocenter_x(rsync 自 Mac, Mac 为 git 主副本)。AutoDL 主线服务器换到端口 33763, 栈需 restore_autodl.sh 重启(用户手动)。

**✅装机完成(08-24)**: isaacsim 4.5.0 pip 装入 conda env isaac(15GB), 无头自检 SMOKE-OK kit=106.5.0(scripts/isaac_smoke.py, 首启编译几分钟); 4.5 文档离线在 sim_x ~/isaac_docs_4.5(934M)。装机踩坑: ①机器闲置自动休眠断线→已 mask sleep/suspend target; ②插网线后稳(enp5s0); ③pip 卡死用 --resume-retries 断点续传重启; ④`pkill -f isaac_smoke` 会杀到自己的 ssh shell(命令行含同串)→用 `pkill -f "[i]saac_smoke"`; ⑤macOS 无 timeout 命令, 抓包/限时脚本注意。**✅首个实验·落料统计(08-24)**: 药盒60x37x22mm/50g(config/box_specs.yaml); `scripts/drop_stats.py`(isaacsim.core.api World+DynamicCuboid, 两盒先后落+σ散布, 按最小轴倾角/垫高分类) 30回合σ=2cm → flat 73%/leaning 23%(垂直随机下落模型)。**随后按真实机构重建(`ramp_stats.py`): 传送带→36°不锈钢斜坡(实测坡长11cm)→坡口离桌27cm→桌面, 盒平躺入坡 → flat 97%/leaning 3%/stacked 0%(50cm坡长同样)。结论: 真实机构困难局面仅个位数%, 全部来自两盒同落; 垂直下落27%是错误假设的悲观值; 主流程按平放设计, 扰动+重试仅作兜底, 落料错开节奏是最便宜的改善**。假设已标注(摩擦0.22/带速0.1)。DROP_GUI=1可出画面(DISPLAY=:0经Moonlight看)。待办: σ/落高/错位扫参找机构改进方向; 吸盘唇边直径与容忍角待用户实测(yaml留空位); URDF→USD导臂。相关: [[robot-arm-tailscale-access]] [[servers]]

**理想局面细分(08-24晚, ramp_stats五分类+截图)**: 理想=两盒不贴+大面朝上。30回合(30%侧立入坡假设): **ideal 33% / side_up 43% / leaning 17% / close 3% / stacked 3%**——最大敌人是侧立不是叠放, 且几乎由入坡姿态决定。**下一步关键实测: 传送带上侧立盒真实比例**(决定要不要做拨倒机构, 可先仿真验证横杆方案)。截图验证流程: RAMP_SHOTS_DIR=~/桌面/ramp_shots 每回合按类别存图(isaacsim.sensors.camera.Camera, 必须set_world_pose(camera_axes="world")否则USD约定拍空地); 曾出空图, 教训=截图类产物必须scp回来亲眼核验再交付。侧立盒顶面仅60x22mm, 吸盘唇边直径待用户量(决定侧立可不可吸)。

**✅落料机构结论(08-24, 报告 robocenter_x/data/ramp_sweep_2026-08-24.md)**: ①入坡姿态是最大单项改进——30%侧立入坡 ideal 33%, 全平入坡 ideal 57%(值24个点); 但全平入坡仍有17%侧立+13%倾斜是**27cm落地冲击摔出来的**(带前冲速度落地会绕前棱翻立), 推翻了我"落下过程不改变姿态"的判断。②坡口高度扫描(全平, 各30回合): 5cm ideal40%但叠放20%(散不开) / **10cm ideal70%零叠放(用户采纳为目标高度, 已写 config/box_specs.yaml ramp.mouth_height_target_mm)** / 15cm 33% / 20cm 30% / 27cm现状57%。③**数据可信度警告: 每档30回合, ideal标准误差±9个点, 中间三档起伏是噪声不是规律; 改机构前应各跑150回合复验**(用户暂不跑)。脚本参数化: RAMP_SIDE_P(侧立概率) / RAMP_MOUTH_H(坡口高度米)。
