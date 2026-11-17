---
name: l6-path-optimization-method
description: L6_left 路径优化(任务1)产出的标准化调试法 + v2 避障路径 + 1.2/1.0 稳定速度结论
metadata: 
  node_type: memory
  type: project
  originSessionId: bf187ce8-2d08-4180-af37-01d6d80d4d3b
---

2026-06-01 在 L6_left 上完成路径优化([[storage-rollout-next-tasks]] 任务1),产出一套可复用方法,并定下工作配置。

**工作配置(已定档)**
- 新避障路径:`轨迹探索/L6_left/L6left_path_trackjoint_v2.json`(`enqueue_track` 稠密关节点,抬肩/手腕 j4 换更大余量,仿真 197/197 零碰撞),已替换旧 RDP 17 关键帧。`play_trajectory` 升级为自动识别 `.json`(`enqueue_track` 取[0:6] / `traj` 取[1:7])与旧 `.yaml`(`points[].positions`)。
- 终点 `final_L6_Left` 其实是**货架外的外中心**(命名误导),与放置基准外中心关节角差 ≤1.5°,放置用绝对位姿不受影响,翻腕+穿横杠+每格放置全不动。
- 稳定速度:`trackJointMotion` **1.2/1.0**(`SHELF_TRAJ_VEL/ACC` 默认)。实测 1.6/1.4 太快,1.2/1.0 最稳。
- 连续化技巧:`play_trajectory` 加 `lead_in`(prepend 当前关节)/`tail`(append 下一目标),把"扫码位→mid""mid→拍照点"两段 `move_joint` 并进同一条 `trackJointMotion`,消除 mid 处停顿。注意:`trackJointMotion` 按**末端线速度**计速,这两段是重定姿(关节大转、TCP 位移小),1.2 档下比分段 `move_joint`(关节计速 0.75)反慢 ~0.6s;要更快需提 `SHELF_SPEED`。

**标准化调试法(复用到其他仓位 = 任务3)**
1. `python tools/play_seed_path.py <json>` 慢速播放探索轨迹,`--reverse` 退回起点,`--speed/--acc` 调速,Ctrl-C 急停;
2. `SHELF_SPEED='vel,acc'` 环境变量**不改代码阶梯测速**(只覆盖 track,不动货架内 `LINEAR_VEL`);
3. `mark_segment` 段耗时 + `print_segment_summary()` 末尾汇总表读 baseline;
4. `FORCE_CELL='col,row,layer'` 单格真盒验证(0-based,放完不记库存)。

**各库位速度表**:`storage/data/shelf_path_speeds.yaml` 记录每库位「中间点→货架口」稳定 trackJointMotion 速度。当前(10 库位,L4~L8)L4_left=1.0/0.9、L4_right=0.7/0.7、L5_left=1.2/1.0、L5_right=0.9/0.8、L6_left=1.2/1.0、L6_right=0.8/0.8、L7_left=1.2/1.0、L7_right=1.0/0.9、L8_left=1.0/0.9、L8_right=0.7/0.7(最慢)。规律:速度天花板多由「末段进抓取点余量」决定;但 L4_right 反例——末段余量给到 230mm 仍只 0.7,说明「右摆四段+双安全点的姿态切换」也能成瓶颈。右侧右摆普遍比左侧慢。`play_seed_path` 加载器优先 `enqueue_track`,再 `traj`/`recorded_traj`(打印 `源=` 确认)。

**Why:** 任务1的核心就是"产出可复用路径调试方法",这套已在 L6_left 跑通,是拓展样板。
**How to apply:** 其他仓位直接套这套工具链;关键文件 `business/pick_and_scan_v1.py`(`play_trajectory`/`load_track_points`/`_env_speed`)、`tools/play_seed_path.py`、`utils/segment_marker.py`。整套放置管线见 `docs/placement_pipeline.md`。相关 [[stage-final-trajectory]]。
