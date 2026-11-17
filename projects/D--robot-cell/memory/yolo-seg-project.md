---
name: yolo-seg-project
description: "YOLO11n-seg \"box\" 实例分割项目（AutoDL 服务器 /root/YOLO_SEG）状态、模型路径与关键经验"
metadata: 
  node_type: memory
  type: project
  originSessionId: 48723019-f6de-4af4-9e07-d7911347dc05
---

AutoDL 服务器（见 [[ros2-foxglove-setup]] 同一台 RTX 4090）上的 YOLO11n-seg 单类别 `box` 实例分割项目，路径 `/root/YOLO_SEG`，是 git 仓库。

**当前最优模型（部署用）**：`/root/YOLO_SEG/runs/segment/train_v2/weights/best.pt`（v2，2026-05-19 训练）。旧 v1 在 `runs/segment/runs/segment/train/weights/best.pt`（路径双层 runs/segment 是因为 v1 训练时多传了 project 参数，v2 已去掉）。

**关键经验**：v1 训练集 90 张每张只有 1 个 box，模型学成"一图一框"强先验，部署后遇到 2 个 box 会糊成 1 个（或碎检）。解决办法 = 采集失败难例→标注双 box→并入训练集重训。v2 加了 9 张双 box 样本（val 留 2 张验证），双 box 检出从 2/11 提升到 11/11，val mAP50 0.961→0.995。

**已验证的迭代闭环**：部署 → 收集失败样本 → LabelMe/YOLO 格式标注 → 构建 dataset_vN（不污染原 my_dataset）→ 从 yolo11n-seg.pt fine-tune → 新旧模型对比推理（数量+可视化）。

环境：ultralytics 8.4.50，conda python `/root/miniconda3/bin/python3.12`，torch 2.8+cu128。本地可视化结果暂存 `/Users/chen/Desktop/_yolo_seg_scratch/`。
