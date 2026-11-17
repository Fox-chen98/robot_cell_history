---
name: action-driver-layer-plan
description: "动作层: 8月Mock框架封存; 2026-09-02改走轻量版(回执+复位+动作表)在robot_cell/actions落地, 8动作全部真机验过; 下一步流程层"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-08-18T08:21:28.994Z
---

robot_code 重构=动作驱动层L1(17项动作三层架构),设计文档=`robocenter/docs/设计文档/动作驱动函数设计说明.docx`。**2026-08-17已启动**(机械臂售后停机期,Mock开发不需要硬件):

- **工作区**: `~/Desktop/robot_actions/`(独立git,第三工作区)。核心交付=`docs/动作驱动接口定稿.md` v0.1(已通俗化定稿):ActionResult回执单(含payload货物下落字段)/失败四分类(RETRYABLE/MANUAL/NEED_RESET/FATAL,**动作层不自动重试**)/五种设备状态(急停解除必经ERROR再reset)/**端口约定**(v0.2修订原"位置不变式": 每动作声明入口/出口点位,端口咬合直连——detect→pick→scan台区连续不回mid;货架组坚持mid进出=路径库资产接口;mid=全局恢复锚点;执法=_run的require_pose查岗。用户评审发现原版会造成台区无意义往返)/17动作签名7组/Mock策略。**术语约定(用户明确要求): 不用"值班牌"等比喻性叫法,统一说"设备状态/状态切换规则";测试输出不出现"断言/剧本"字样,要像真实操作过程,核对逻辑藏幕后只在异常时开口。**
- **五个默认决定**已填死(可议):①位置不变式 ②同步阻塞+急停独立通道 ③payload状态入回执 ④不自动重试 ⑤reset=从任意位置安全回mid(=robocenter"现录现跑"配方自动化,第二难仅次盘点)
- **开发方式**: 旁边盖新楼不拆老楼——robot_code/actions/全新包,只依赖hardware/(L0六类接口,已完成);1823行pick_and_scan_v1.py不动(安全网),抽取=复制不搬走。Mac写新文件scp推blue-space(robocenter模式);**Mock测试纯Python,Mac本地可跑**,不需要blue-space/AutoDL。
- **测试约定**: 用户手动执行 `python test_action.py <动作> [--fault <故障>]`,自描述+PASS/FAIL(robocenter脚本风格);Mock测行为层(指令序列/分类/状态转换),真机补物理层。
- **进度(2026-08-18)**: 定稿§7第2步完成——骨架(result/state/context/layer)+六类Mock+系统组connect/status/disconnect+test_action试运行入口,5项全过。已修一个真bug: connect失败=什么都没发生,状态应回IDLE不进ERROR(否则复位死锁)→_run加dirty_on_fail参数,动作自己声明失败会不会留下不干净现场。§7第3步分两批: 3a安全组(home/estop/estop_release/reset/mode_switch)已完成——五种状态全部可由真实动作触发,MockArm有position/move_to/stop,估计运动失败→position=unknown→ERROR;estop/release/reset/mode_switch不走_run流水线(各有准入规则),home走流水线dirty_on_fail=True。3b作业组已完成(Mock版): feed/feed_return/detect/pick/release/scan/jog_to,端口查岗require_pose上线(E_NOT_AT_PORT),错误码分类表CODE_CATEGORY进result.py,pick吸附失败自收场退回photo_safe(RETRYABLE),flow场景=台区全链串演(19/19全PASS)。端口名: photo_safe拍照避让位/hold握持位/grab吸附点/mid。货架组Mock版也已完成(定稿v0.3): shelf_store/shelf_retrieve签名改坐标传入(slot,target{lateral,depth,layer},box_size)——**行列层→坐标换算上移到planner/grid种子(未来独立库存管理软件地盘,用户评审定的边界,推理记录=docs/货架组动作设计讨论.md+四层架构图L3调度/L2编排/L1动作/L0硬件)**;动作层只验物理可达(config/shelf_profile.yaml=16格档案真值+正式路径名单L6-L8,L1-L5未转正下单即拒E_NO_PATH);五步编排(播去程→直线进格→放/吸→直线退→播返程);格内卡住=最脏现场进ERROR。flow=入库全链(台区直连+上架)24/24全PASS。第6步异常演练也已收尾(**Mock版动作层竣工**,27场景全绿): 新语义(用户拍板)=持货遭脏失败→payload置UNKNOWN且**复位不清除**(需人工确认,通道待定候选reset带申报参数);Mock故障注入支持nth延迟发作(演"进格顺利退出才卡")。deliver也已Mock实现(用户点破"骨架可先抽象,握手协议只是一步"→代码留【握手预留位】注释插座,出库全链通retrieve→deliver);L2菜谱flows/store_one_box也已完成(按失败分类自动处置:RETRYABLE步内重试2次/MANUAL报警停单/NEED_RESET复位后整单重来一次·货物UNKNOWN则转人工/FATAL停单报修;E_ARM_STALL改归NEED_RESET类)。**停机期Mock工程收官,32场景全绿**。剩余均等外部条件: 真硬件拆迁(等机械臂修好,从v1搬活到Real六类实现)/握手协议(填deliver插座)/感知方案(inventory)。注意: Mock版"活本身"是占位实现,真机版仍需从v1拆迁(用户要围观学设计)。用户学习进度: 已逐文件读完全部骨架代码,理解工单/流水线/持有链/干净脏失败/端口概念。
- robot_code现状: L0 hardware/六类接口✓;business/pick_and_scan_v1.py=1823行主流程(被拆对象);motion/空壳;retrieve_from_storage.py=旧出库(需重建)。

参见 [[slot-path-production]](主线:机械臂修好后转正L1-L5) [[industrialization-roadmap]]

**2026-09-02 转向轻量版(用户过载后重议)**: 8月17项框架封存不搬(只拷回执思想); 在现役库 robot_cell/actions/ 直接包8个动作(放置/飞路径/复位/丢回/吸取/识别/扫码/去命名位姿), 回执五栏(结果/下一步四分类/货物含"推定吸着"/臂在哪/说明), Mac入口`scripts/act.sh`, 部署`deploy_cell.sh`。全部真机验过(含急停→reset演练, 两趟单步全链)。原则: 动作=臂动了的那一段; 出口咬合下一动作入口(丢回出口=home); 只放行判过卷起点; 门卫宁拒不猜。判断(选盒/判大面/认脸/排坑位)待串流程时拎出。详见docs/格口路径库生产日志.md 2026-09-02下午。

**2026-09-02傍晚 流程层跑通**: flows/store_one_box.py(`flow.sh store`)真机9卡+4判断全绿34.5s(=串烧, 零开销)。"可控"交付: 停在哪/货在哪/下一步全在卡上。串烧未退役; 下一步 grasp.sh shelf→flow 与搬家, 或连抓循环。
