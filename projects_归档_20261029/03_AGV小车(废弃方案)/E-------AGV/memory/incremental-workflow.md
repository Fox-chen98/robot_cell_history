---
name: incremental-workflow
description: 用户偏好：AGV装配设计要一步一步来，一次只安装验证一个零件
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d5b56e19-ed2d-49f9-b670-5d290a8d0616
---

用户明确要求：不要一次性把所有零件摆进装配体，而是**一次安装验证一个零件**，通过后再进行下一个。

**Why:** 用户第一次做AGV，逐件推进便于理解每一步、出问题能定位原因；符合其试错式开发思路（底板阵列孔+转接件也是为此）。

**How to apply:** 每轮只处理一个零件：设计/放置该零件（及其转接件）→ 干涉检查/渲染验证 → 用户确认后再做下一件。不要抢跑批量布局。安装顺序见 [[agv-parts-dimensions]] 的分层方案。
