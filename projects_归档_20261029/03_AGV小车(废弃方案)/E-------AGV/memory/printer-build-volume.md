---
name: printer-build-volume
description: 用户3D打印机最大打印尺寸 256×256×260mm
metadata: 
  node_type: memory
  type: project
  originSessionId: d5b56e19-ed2d-49f9-b670-5d290a8d0616
---

用户的3D打印机最大打印尺寸为 256mm × 256mm × 260mm（X×Y×Z）。

**设计约束**：AGV 所有 3D 打印件（底板、外壳、托架、转接件等）单件尺寸不得超过此范围；超过时需拆分成多件再拼接。当前底板 231×231 和外壳 231×231×145 均在范围内，见 [[agv-parts-dimensions]]。
