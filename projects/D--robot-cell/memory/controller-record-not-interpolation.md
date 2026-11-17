---
name: controller-record-not-interpolation
description: 验证机械臂路径段必须用控制器实跑+录制的真实轨迹，绝不能用软件插值(lerp)代替——插值对不上真机
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
---

验证任何机械臂运动段是否碰撞/可行时，**必须让控制器实际 movej / trackJointMotion 跑一遍（仿真模式）并录制真实关节轨迹，再拿录制轨迹去仿真逐点碰撞检测**。**绝不能用我自己在关节空间做线性插值（lerp）的"几何估算"代替真机录制。**

**Why**：自己插值往往和真机对不上。控制器有自己的加减速规划、movej 各关节归一化时序、trackJointMotion 的拐角融合/过冲——这些只有控制器（仿真模式）实跑录制出来才知道。拿 lerp 去"验证"等于自己验证自己，不算数。实证：L6_Left 3 点几何插值估 8.78s 零碰撞，真机实跑 10.07s 且撞 link_2。用户在 2026-06-02 多次纠正此点（直连 L6_Right、L7_Left 种子时我又犯）。

**How to apply**：步骤1-2 永远是「控制器 movej 点到点(中间点→构型) → 录制 = 种子轨迹 → 发 AutoDL 逐点碰撞检测」。任何"先看会不会撞/顺不顺"的需求，都走「控制器跑 + 录制 + 复验」，不要图省事走 lerp 一步到位。详见 [[shelf-path-debug-workflow]] 的"几何估算会骗人"条。
