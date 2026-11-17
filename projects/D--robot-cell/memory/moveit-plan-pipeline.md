---
name: moveit-plan-pipeline
description: MoveIt规划→仿真验证→控制器实跑→真机 五步流水线已全线打通(2026-08-13首跑成功)
metadata: 
  node_type: memory
  type: project
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-08-14T01:33:41.710Z
---

2026-08-13 五步流水线首次端到端跑通真机(手摆姿态→mid, 6.7s, 0.25速): ①`plan_motion.sh <位姿>`(MoveIt规划,AutoDL move_group,避开全部障碍) ②`replay.sh plan_<位姿>`(自家判卷器复核+回放) ③`run_plan.sh <位姿>`(控制器仿真模式trackEnqueue+trackJointMotion流式实跑+25Hz录制)→`replay.sh run_<位姿>`终判 ④`save_path.sh`入库data/paths/(场景变更后`replay.sh <文件路径>`批量复验) ⑤`run_real.sh <位姿>`真机(YES确认+真实模式断言+起点比对±0.05rad+默认0.25速)。流程文档`docs/MoveIt规划到真机流程.md`。

踩坑三连:
- **MoveIt错误码99999=起点超模型限位**——URDF关节限位原是±180°,真机规格J1/2/4/5/6=±360°,J3=±160°,已改双侧URDF(2026-08-13)
- **仿真模式下读关节=仿真控制器虚拟姿态**,不是物理编码器;对齐协议=示教器"切真→切仿"一个来回(切换瞬间仿真继承物理姿态)
- 轨迹文件命名约定: /tmp/check_<名>.json; plan_<位姿>=纸面规划, run_<位姿>=仿真实跑录制, runreal_<位姿>=真机录制; 同名覆盖,资产要save_path转正

2026-08-13晚补充: ①`solve_ik.sh "x y z rx ry rz" <名>`=标定值算目标点+控制器IK入库poses.yaml(此SDK的cal_ikine的tool参数是TCP数值列表非名字!); 实战scan_hover(扫码口上方10cm)=标定的第一次实战应用,check_motion直连PASS ②replay.sh已合并判卷+回放(原recheck删除),支持文件路径回放路径库 ③run_real支持直连验证过的录制(不再强制要求规划) ④restore新增5c叠显复活+开头清SSH复用僵尸通道; **远程起常驻进程完整咒语=`( setsid nohup … >log 2>&1 </dev/null & )`,外层子壳双重脱离才是关键,确认用第二条独立ssh查日志** ⑤Foxglove按mesh URL缓存失败加载,?v刷不动,须整个重启应用 ⑥**2026-08-14 scan_hover真机执行+量尺验证通过**——标定体系实弹考试PASS,"码牌标定→标定值算点→IK→真机执行"全链条可信,18格口批量算点方法论已获实证。

方法论: 判卷/回放全复用`replay.sh`(规划输出与录制同格式的巧思);终裁只认控制器实跑录制(controller-record-not-interpolation)。下一步: 用此流水线批量建18格口新路径库。参见 [[scene-sim-rebuild]] [[shelf-path-debug-workflow]]
