---
name: webhook-proposal
description: "设备事件 webhook 推送: 方向定案(推送+轮询兜底)、绑定方式定案(配置写死)、待定项与实现要点; 2026-09-21 梳理"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-09-21T12:49:57.129Z
---

2026-09-18 管理软件团队建议: 设备事件由轮询(GET /tasks/{id}/events?since=N, 网页 0.5s 一次)改为设备主动 webhook 推送。用户当时"先不急, 先讨论"; 2026-09-21 详细梳理了一轮。

**已定案**
- **加, 不是换**: 事件 JSON/seq 不变; `events?since=` 永久保留作断线补拉。可靠性来自兜底那一半, 推送只是"快 + 对方省事"(事件频率低: 一盒 11.9s 约 19 条, 轮询 0.5s 延迟本就无所谓)。
- **绑定方式 = 配置写死**(2026-09-21 用户定): `config/cell.yaml` 加 `webhook{url, token, timeout_s, retries, events}`。不做注册接口 —— 上位机地址固定, 且注册接口必须连带做鉴权(事件含追溯码/格口位置/库存变动, 无鉴权则内网任意机器可把事件流重定向)。用户: "先做A, 后续有具体要求再说"。
- **网络方向**: 用户确认最终一定通(设备主动连上位机, 与现在方向相反)。

**待定**: 推哪些事件(建议白名单 stored/discarded/lost/retrieved/pit_empty/code_scanned/stocktake/needs_human/fault/task_end; card/text 刷屏的让对方按需拉)。

**Why:** 对方被动收更简单; 但推送必须有补拉兜底否则掉线丢账。
**How to apply:** 实现要点(最易写错的几处) —
1. **绝不在 `Task.emit()`(cell_server.py:435, 跑在机械臂执行线程) 里同步 POST** —— 上位机重启时 3s 超时×3 次 = 机械臂举着盒子/伸在格口里僵 9s。必须 `queue.put()` 后立刻返回, 另起送信线程。用户对这点反复追问才理解, 讲清楚的关键是"设备内部是两条并行的线, 图里画成一条所以看不出谁在等"。
2. **单线程串行投递保序** —— 43 没发完不发 44, 否则 task_end 可能抢在 stored 前到。
3. **幂等键 = `task_id + seq`**(已有, 放 `X-Event-Id` header), 重试时不变; 接口文档必须写死"上位机必须据此去重", 否则 stored 重投 = 账上多一盒。
4. 记账触发点是 `stored` 事件而非 `destination`(后者只是"打算放这儿", 中间可能 lost)。
5. 自检: 启动发 ping, `GET /device` 报 `webhook: ok/unreachable/401`, 不能默默失败。
6. 验证全部可离线做: 8903 上位机后端改成假接收端(正常 200/故意慢 5s/直接宕机三种模式) + 流程 `--dry` 干跑, 比对事件 `ts` 间隔是否变长; 真机 `flow.sh store` 那一趟由用户跑。
相关 [[cell-interface-layering]]
