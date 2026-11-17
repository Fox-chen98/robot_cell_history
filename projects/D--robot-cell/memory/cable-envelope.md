---
name: cable-envelope
description: "波纹管管线包碰撞包络(2026-08-20上线):真机碰撞事故→保守包络建模→双向试金石验证,含显隐开关与全部踩坑"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-08-20T07:25:51.976Z
---

**事故**: L3_left真机首跑,腕部管线环(波纹管)在轨迹53%处蹭主货架上缘,急停。根因=碰撞世界没有管线包,判卷对该空间"自信的盲区"(纸面绿≠真绿)。

**方案**: 保守包络(不模拟柔性体,包住所有可能位置)——5个link/7形体: 大臂凸条(朝主货架侧,偏置123mm)+肘球(朝第二货架侧)+小臂凸条(顶面,偏置124mm/Z偏-123mm=STL包围盒实测的肘部错层!)+腕环三球r=80(案发主嫌,Z渐变)+末端箍球。方位由用户在cable_ref姿态(L形基准,poses.yaml)用参照物描述→FK翻译成连杆局部坐标(fk验证:mid TCP差2mm)。参数: 管Ø28/抱箍凸出80/腕环鼓出80。

**豁免(关键设计)**: 包络vs全部臂连杆+包络互相=SRDF豁免60对(管贴臂是常态非事故);包络vs环境=唯一使命。独立挂件连杆而非加粗臂连杆(避免幻影自碰撞)。

**验证**: 试金石A=replay run_L3_left在46-67点翻红(真机急停点53正中判红带,contacts=cable_loop×scene_shelf_14)✅;试金石B=20条老路径批量重判(**用户一直没跑,待办**)。重新规划后L3_left真机双向实弹通过✅=现实给模型盖章。

**工具**: `scripts/serverside/cable_envelope_gen.py`(幂等注入URDF/SRDF,标记块可整体还原;参数在头部)+`scripts/show_cable_envelope.sh [off]`(显隐)。**两份URDF都要注**: 判卷份(install/duco_support)+显示份(web_serve/gcr10_1300.urdf,Foxglove的URL通道);栈重启后还有话题通道(/robot_description)也显示判卷份的visual。

**踩坑全录**: ①"栈在跑"≠"栈是新的"——restore_autodl见栈存活就跳过,改URDF后必须先杀栈(kill launch主进程,子进程会respawn要连坐)再restore ②无visual的碰撞体被Foxglove画成白色 ③visual alpha=0被画成黑色 ④删显示份的块管不住话题通道 → **唯一渲染器无关的隐藏=visual缩成0.1mm小点**(外观与碰撞体允许不同) ⑤显隐切换后要重启栈(话题通道)+改?v(URL通道)。

**方法论**: 抽象可以丢细节,不能丢体积;实测金标准>模型判决(已实弹路径不因模型改版作废);双向试金石校准(抓得住已知事故+不误杀已知安全)。真机侧遗留: AutoDL的duco_ros2_driver是git仓库,基线840fc34可整体回退。

参见 [[slot-path-production]] [[moveit-plan-pipeline]]
