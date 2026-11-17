---
name: wrist-io-trigger
description: "新腕部电机IM42ET-P改IO硬线触发方案——驱动器程序/接线/WristRotatorIO类,已验收电机侧"
metadata: 
  node_type: memory
  type: project
  originSessionId: 27b2fe1a-80d8-409d-91ca-360d3fa81c0c
  modified: 2026-07-22T01:56:52.506Z
---

腕部旋转电机换新(IM42ET-P,42机座)并从 485 直控改为**柜子 DO 硬线触发**(2026-07-22 电机侧验收通过):

- **驱动器内部程序**(上位机写入+断电保存):ProgSwith 链是"阻塞式多路等待",**无 fall-through,N 个动作必须 N 条条件**(实测踩坑得出)。三条件:X0亮→@22(+1000)、X1亮→@28(−1000)、都灭→@16(回0);动作段=ProgSetReg2(208,pos)+ProgWaitOff+ProgDelay(100)+ProgJump(0)。占格:首条ProgSwith 6格、后续5格、SetReg2 3格、其余1格。
- **参数走断电保存**,不写初始化程序段(避免程序覆盖参数页改动);空闲电流提到 60% 解决 +90° 方向被气管扭力拽回(985→1000)。
- **接线**:电机黄Xcom→柜0V、黄黑X0→DO1(端子6)、蓝X1→DO2(端子8);Y 反馈**未接**,到位靠固定延时 1.2s;Y1 到位(常闭)留待转产前补线。485/USB 只作维护调参通道。
- **代码**:hardware/wrist_rotator/rotator_io.py 的 `WristRotatorIO`(接口与旧 WristRotator 对齐,close 故意不动 DO 电平防货架内转出);测试 tools/test_wrist_rotator_io.py(机械臂侧联调已通过,DO 逻辑号 1/2 确认正确)。主流程尚未切换(仍 COM10 旧电机)。

**Why:** 固定 3 位置场景,IO 硬线比串口少 6 个故障环节,失效模式仅断线;电平=状态可随时重读。
**How to apply:** 主流程切换=把 WristRotator(COM10) 换成 WristRotatorIO(复用/新建 IOController);改动电机逻辑先查 [[leesn-stepper-docs]] 手册与上位机程序。
