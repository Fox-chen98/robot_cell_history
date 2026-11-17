---
name: leesn-stepper-docs
description: "立三LEESN步进电机资料位置(D:\\电机资料)与关键寄存器表,腕部IM28ET-P/新IM42ET-P"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 27b2fe1a-80d8-409d-91ca-360d3fa81c0c
  modified: 2026-07-21T08:50:15.191Z
---

立三机电(LEESN)一体化总线步进电机资料在 `D:\电机资料\`:

- `IM42ET-P硬件手册.pdf` — 42 机座硬件(接线/尺寸/IO)。2026-07-21 新加入;项目现用腕部电机是 **IM28ET-P**(28 机座),同协议不同规格,疑似准备换装/新增轴。
- `485通讯手册_sv126.1(2).pdf` — Modbus RTU 寄存器映射(SV126.1 固件),小端字序。
- `ModBUS RTU编程参考手册V3_3(1).pdf` — 高级功能:内部编程区、中断定位、回零模式、限位/急停、IO 触发、力矩模式。
- `参数设置流程(1).pdf` — Leesn-config 上位机(USB转485)设参+断电保存流程。
- `上位机操作视频/` — 各功能演示 mp4(无法直接读取)。

关键寄存器(与 hardware/wrist_rotator/rotator.py 一致):
0x0004 位置INT32 | 0x0006 状态(Bit8~9运行态) | 0x0024 细分(默认4000) |
0x00D4 使能(0=使能,FC6 不响应须用 FC16) | 0x00D8 速度(0.01rpm) | 0x00E8 绝对位置(写即触发)

**How to apply:** 改动腕部电机功能(调速/回零/限位)或接入 IM42ET-P 时,先查这套手册;通讯默认 115200-8N1, slave=1, COM10。相关:[[feeder-integration]]
