---
name: storage-rollout-next-tasks
description: L6_left 上架方案验证通过后的三个拓展任务:路径优化/拓展药盒/拓展仓位
metadata: 
  node_type: memory
  type: project
  originSessionId: bf187ce8-2d08-4180-af37-01d6d80d4d3b
---

L6_left × S20070026(麻腮风)上架方案在 2026-06-01 真机验证通过后,用户规划三个后续任务,优先级按顺序:

1. **路径优化**:优化「上架中间点(midListingStatus)→ L6_left」的运动路径,提升上架速度;**重点是探索出一套标准化的路径调试方法**,后续复用到其他仓位的路径优化。当前路径在 `recordings/stage_final_mid_to_L6left.yaml`(RDP 关键帧 + trackJointMotion 1.2/1.0)。

2. **拓展至其他药盒**:目前只注册了 SKU `S20070026`,需支持更多药盒(走 `calibration/register_sku.py` 注册 + `compute_placement_map.py` 重算)。

3. **拓展至其他仓储位**:目前只标定了 `L6_left`,需拓展到其它库位(L1~L8 × Left/Right)。每个库位要标外中心 + 6 极限位 + 内部抬升上限(`z_max_inside`),走 `build_slot_envelope.py` 换算。

**Why:** 当前 L6_left 这一套(0526 工具 / 双 z 上限不压底 / 126 盒 / 货架外翻 90°+固定进入巡航避横杠)已跑通,是后续拓展的样板。
**How to apply:** 任务 1 要产出「可复用的路径调试方法论」(不只是调好这一条);任务 2/3 复用现有 calibration 管线。整套流程见 `docs/placement_pipeline.md`。

相关:[[stage-final-trajectory]](路径文件与待优化点)、[[teach-replay-pipeline]](标定/录制管线)。
