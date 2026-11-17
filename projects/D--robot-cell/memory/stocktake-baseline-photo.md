---
name: stocktake-baseline-photo
description: "盘点\"比基准照\"(用户方案): 入/出库后在该列拍照点拍基准, 盘点逐列同点拍比; B-L10 11-04 真机全过; 两个已知问题用户定先记录不处理"
metadata:
  node_type: memory
  type: project
  originSessionId: 600697e2-60a3-4d18-a896-189ef5a5ce1b
  modified: 2026-11-04T07:25:26.506Z
---

2026-11-03 用户定盘点原理: 不数盒, 入库/出库后拍基准照量队首(front_mm 交上位机记账), 盘点在同一拍照点拍一张和账上 front_mm 比. 详见 docs/盘点基准照方案.md.

2026-11-04 用户改: 拍照点 = **每列各一个**(盘点也逐列横移拍, 拍完直接接头飞回, 不回中间). 正对拍遇镜面热斑 → 往格口中间错开 80mm(slots.yaml photo_offset_mm). 下午 CRV 真机测 4 列/3 药/1~5 盒/取空/手动拿走 1 盒, 全部正确.

**Why:** 节距、校正值都是会变的经验值, 用户明确不接受"凑数"校正.
**How to apply:** 开关 slots.yaml stand.baseline_shot_slots=[B-L10]. 用户定"先记录不处理"的两个问题(文档待办 6/7): ①账外物体查不到(逐列拍照 stray=None) ②手动拿走一列最后一盒判"整列被碰动"(空→1 盒差 31~35mm 超容差). 用户没提前别主动去改. 讨论时用户易信息过载: 先讲原理再讲动作, 别插入新概念, 用户自己的方案优先顺着做(11-04 我两次理解偏了用户的拍照点方案, 先确认再动手). 相关 [[stocktake-design]] [[keep-it-simple]]
