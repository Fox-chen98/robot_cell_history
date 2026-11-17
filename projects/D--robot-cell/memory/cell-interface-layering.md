---
name: cell-interface-layering
description: 设备对上位机的分层与账本归属定案(2026-09-07): 动作/流程不可见, 设备只暴露任务/回报/查询; 占位表由设备维护且以设备为准
metadata:
  type: project
---

2026-09-07 用户定案:
- 动作层、流程层对上位机(库存管理软件)**不可见**. 上位机只面对一个"设备"(将来的常驻服务): 下任务(上苗N支/N分钟, 可指定格口或坑位; 出库按码或位置; 停/暂停/继续)、收回报(每成功一支: 码/位置/用时; 异常: 类型/货在哪/要不要人; 任务结束原因)、查询(设备状态; 能力=格口清单与每格列排层/可达坑位; 占用).
- 任务异步: 下任务返回任务号, 回报主动推.
- **一张表(2026-09-09复议定案)**: 占用表与库存账都在上位机; 设备不记占用, 只校验坑位在账本内/可达+DI4物理核实, 忠实回报. 去处(格口+坑位)由上位机在"扫到码"事件后算出并POST给设备(v1可任务内固定格口+坑位列表). 命令行flow.sh=简易上位机(调试口).
- 设备服务(FastAPI, blue-space 端口8902, 与视觉8900/扫码8901并列; 部署时上位机同机调localhost): POST /tasks(类型+停止条件+去处模式)→202 task_id; GET /tasks/{id}; GET /tasks/{id}/events?since=N(seq递增落盘, 上位机0.5s轮询; kind: stage/code_scanned/stored/discarded/fault/task_end); POST /tasks/{id}/destination(等去处10s超时丢回); pause/resume/stop; GET /device; GET /capability. 一次一个任务, 命令行与服务互斥.
- 调试法(用户定): 先做设备服务, 再做Mac上的简易上位机网页(操作区+事件卡片流+调试窗口记每次请求/响应+本地占用表自动答去处), 真机迭代后从/docs导出API文档. 一步一步来, 每步用户确认.
- 环境(2026-09-09): robot env已装 fastapi 0.141/uvicorn 0.52/pydantic 2.13; Mac经Tailscale访问 blue-space:8902 已验通(绑0.0.0.0, 防火墙不拦).

**Why:** 用户要一个可控的设备边界, 上位机按业务调用而不知道内部动作; 占位表关系到物理安全(垛顶/空坑)与断电恢复, 必须在设备侧.
**How to apply:** 设计新功能先问"这属于设备内部还是上位机"; 不要把业务规则(选格口策略/先进先出)放进流程层; 占位表只记物理占用不记码. 关联 [[action-driver-layer-plan]] [[slot-place-calibration]].

**2026-09-10 退苗/锁苗/去处定案**: 退苗对设备=普通出库任务(type=retrieve), 只差 dest(命名去处: drop/outbound/return, 位置标定了才 available, 账本 config/drop_point.yaml destinations) 与 reason(自由文本回显不解释); 不新增事件类型, retrieved 带 dest. 锁苗纯上位机(批号状态, 选盒跳过+下发前校验). 摆放策略单层(只用第0层, ledger.js SINGLE_LAYER), 因高堆阴影规律与退苗冲突; 换硬件(通道式立放)后位置仍三元组(通道,序号,0), 接口不变. 接口文档由 scripts/api_doc.py 生成. 2026-09-11 真机验证通过: 锁苗(选不到/拒下发)、退苗3盒(L7_left 单层, 73s, task_start带reason/dest, retrieved带dest, 账标已退苗).

**2026-09-16 立放位置抽象定案(去网格)**: 用户提出"通道网格是拿一种盒宽当尺子切的, 换规格就不对; 不能抽象成接口". 定案: 格口只有物理量(可用宽度 left_lim~right_lim, 深度, 列间隙); **列 = 上位机开在某横向位置 x_mm 上的一队同规格同批号盒**, 位置字段 slot+x_mm+index+box_mm(每盒尺寸随任务传); 新增纯计算接口 `POST /plan/store`(上位机传各格口现有列表+盒尺寸+分组键 → 接同键列队尾 / 空余宽度一维装箱从左到右开新列 / 都放不下 ok=false), 设备不存列表(单一真相在上位机, 避免双账本); 出库顺序规则简单(同列序号从大到小)上位机自排, 设备校验物理范围(400 pit_out_of_range). 新规格只需进尺寸表 sku_dims.yaml. 文档 V2.0 已出(19 接口). 网页参照实现: ledger.columns/planTables/standSvg, upper.answerDestination 调 /plan/store. 教训: 抽象要贴物理真实(宽度/深度), 不要把某一种货的参数固化成结构.
