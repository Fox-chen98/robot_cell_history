---
name: feeder-integration
description: 上苗机(FeederService)与机械臂取苗主流程的握手集成设计与联调约定
metadata: 
  node_type: memory
  type: project
  originSessionId: 545fecab-d744-48f6-a8fd-a5b95541f076
---

上苗设备 Modbus 控制整合进项目并与 `business/pick_and_scan_v1.py` 取苗主流程联调（2026-05-19 起）。

**代码归置**：`测试例程/传感器及电机控制/` 的逻辑已整理进项目，勿再引用测试例程：
- `hardware/feeder/controller.py` = `ConveyorController`（Modbus RTU，COM 口可配，默认 COM11，加 connect/close）
- `hardware/feeder/service.py` = `FeederService`：后台守护线程跑三段皮带自治联动（Y2 中转/Y3 料斗/Y1 平台暂停，逻辑原样移植，含 3 次防抖、0.5s 停机冷却、料斗清空 1.5s 确认）
- `config/feeder_baseline.json` 空载基准（已标定，X1/X2/X3=true,X6=false,X7=true,X8=false,X9/X10=true，**联调勿再标定**）；`tools/calibrate_feeder.py` 仅备用
- pymodbus 3.13.0 已在 conda robot 环境，COM11 同机可达（见 [[teach-replay-pipeline]] 环境）

**握手机制**（合并单进程 + threading.Event，无 IPC，取代原键盘 Enter 模拟）：
- 上苗机→臂：X1/X2/X3 任一触发=药盒到平台 → 自停 Y1 + `_box_arrived.set()`；臂用 `feeder.wait_box_arrived(timeout)` 等
- 臂→上苗机：`feeder.notify_resume()` 置 `_resume_req`，后台 `_handle_resume` 清暂停+清 box_arrived+强制 Y1 重判

**关键不变式**：机械臂只有在**视觉确认取料台已空**时才 `notify_resume()`，绝不每抓一盒就 resume。原因：一次送多盒上苗机只触发一次，靠逐盒复查抓完再放行，使抓取次数与上苗机触发次数解耦。主循环：拍摄位→YOLO→有盒则抓取卸盒→`continue`回顶复查（不 resume）；无盒则 notify_resume+wait_box_arrived+continue。

**联调范围**：仅验证"视觉↔上苗机握手+循环"。扫码/真实货位上架仍是桩——抓取后无论扫到与否都走 feeder1/feeder2 卸回上苗机料斗回流（`continue` 而非 return），TODO 逐步放开真实上架。pick_and_scan_v1.py 中 L600+ 仍是历史 dead code，未清理。
