---
name: industrialization-roadmap
description: "项目从手工原型转向工业化部署的路线图与关键决策(2026-07-22),详见 Obsidian 工业化路线图.md"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-08-13T01:39:20.370Z
---

2026-07-22 项目重心新增:解决"换场地全部重标定重调试"痛点,目标工业级稳定。完整方案存 Obsidian `机器人/工业化路线图.md`(权威文档,新对话先读它)。主项目代码在 blue-space `D:\Destop\robot_code`(模块化:business/calibration/config/hardware/vision/storage/tools,含入库 pick_and_scan.py/出库 retrieve_from_storage.py/点位 waypoints.yaml 约20点/16格 new_init_trajectories)。参见 [[shelf-path-progress]] [[duco-controller-in-loop-bridge]]。

核心结论:
- 两层解法:机械标准化(一体底架+定位销,几何由设计保证)为主 + 软件相对化(wobj化+贴AprilTag自动建系)为辅;"机械定几何、标定收残差、软件相对化保灵活"
- 相机/吸盘每次现场重装→TCP/手眼不可省,优化方向=自动化提速(TCP定位安装参数固化;手眼采集位姿库全自动~10min;建议手眼改标到法兰 get_flange_pose 与TCP解耦)
- 路径库迁移:存货架系笛卡尔途经点+首点构型(IK种子),平移<5cm/转<3°构型不变,AutoDL仿真复验兜底
- **已发现疑点待查**:手眼标定用 tool_0526_v1、主流程用 toolv1,不一致可能是 X/Y/Z_COMPENSATION(8/2/6mm) 手调补偿的来源
- 待用户决策:①产品形态(一体机柜vs现场散装,决定技术路线权重) ②任务总容差实测(格口-药盒间隙,卡尺量)

**感知仿真备选项——Isaac Sim(2026-08-13讨论定调)**:现平台(MoveIt+Foxglove)只模拟几何世界(运动学/碰撞/路径),够路径阶段用。Isaac Sim 补:深度相机渲染(RGB+深度+噪声)/吸盘物理抓取/标定流程演练/Replicator合成YOLO训练数据(最值钱)。冷水:标定的"值"永远要真机标(仿真只验流程代码);需RTX常开+~30GB安装+USD学习曲线(立项级投入)。资产可平移(参数化URDF直接导入)。**触发条件(到了再启动)**:要给YOLO批量造合成数据/要排练拍照→识别→抓取闭环;仅规划相机拍摄位姿用现有camera_link+针孔投影即可,不需Isaac。
