---
name: scene-sim-rebuild
description: "参数化场景重建进度——生成器/碰撞管线/演示套件已交付,待实测数据(2026-08-12)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-08-12T08:31:01.077Z
---

2026-08 起项目转向:换了新吸盘(已重新TCP标定)+新货架(插槽式2列9层=18格,层高可调),**旧16格路径库作废**。重建以参数化为地基,工作区在 `~/Desktop/robocenter`(git,能力目录见其 CLAUDE.md/help,操作一律用 scripts/ 现成脚本)。

**已交付(全部实测验收)**:
- 参数化场景生成器:`config/scene_params.yaml`(唯一参数源)→`build_scene.py`(URDF+碰撞清单+自检)→`deploy_scene.sh`(推送+底座高度同步RSP+按需重启栈+终验)。货架=盒子模型(6柱+9板+顶),层高链按8+1层全量实测拟合节距196.4mm,全层误差≤2.2mm(第9板预测1786mm获实测证实)
- 碰撞管线:货架16盒进MoveIt规划场景(`serverside/load_scene.py`,restore自动重载);红绿验收通过(红=吸盘↔第4层板精准命中)
- 体验套件:`show_collision_world.sh`(看覆盖范围)/`demo_motion.sh green|red`(控制器实跑→逐点检查→Foxglove回放,撞则冻结+红色高亮被撞物,marker话题/collision_markers已在用户布局开启)
- 底座参数化(圆柱高/半径),显示与RSP双侧同步机制;`serverside/kill_stack.sh`(pkill自匹配陷阱的解法:服务器端脚本杀栈)

**关键值**:pedestal.height=0.49(用户实测);货架pose_xyz=[0,0.75,0]粗估待码牌标定;MID=[-0.046,0.471,-1.718,-0.066,1.571,0.000]rad;演示红点=第4层板内,绿点=货架前悬停(直达大摆必撞——link_2扫层板,老"盲撞"现象在新碰撞世界复现)

**2026-08-12下午已完成**:①桌子参数化(710x395x564取自台面.STEP,含扫码口蓝色标识,碰撞17障碍物)②末端工具完整接入:STL显示(SolidWorks法兰面建参考坐标系导出,整体组合.STL)+自动切2碰撞盒+RSP/MoveIt双侧同步+TCP=控制器get_tcp_offset原样存yaml[0.037903,0.017895,0.36972](法兰系,build自动按mount_rpy_z=180°换算)。统一入口`replace_tool.sh`,全程见`docs/末端工具更换手册.md`。踩坑三连:STL默认坐标系导出会飘(必须法兰面建系)/检验要圆拟合别赌中心孔(吸盘板没φ31.5孔曾误判)/mesh必须内容指纹命名tool_<md5>.stl(Foxglove按URL缓存,同名换内容不刷新)。blue-space新增read_tcp_offset.py(只读控制器工具标定)。

**2026-08-13 标定线全线闭环(重大里程碑)**:ArUco标定链(相机PnP×手眼×FK)交付并完成全场景标定——①桌子pose实测[-0.9669,0.1784]yaw90.79°(修正18cm)②底座高实测0.50(地面码ID4,双视角互证,修正+1cm)③货架pose实测[-0.0271,0.9365]yaw0.47°(修正18.7cm,三码正对采集+三点拟合,间距自检差0.1mm)。**场景已无估计值**。工具链:aruco_snap.sh(视觉体检)/calibrate_table.sh/calibrate_scene.py的floor|shelf|where|shot|solve模式(blue-space,conda robot环境)。核心经验:**斜视角PnP有+27mm级系统偏差(零畸变内参),必须正对拍摄**;质检门槛(间距自检/高度差/拟合残差)成功拦截了斜拍坏数据;贴码约定=仿真里放码牌;深度图只当哨兵不进结果。

**剩余待办**:①post_section立柱截面(仅显示)②新路径库调试(标定已齐,可开工)③货架标定的shot/solve流程可包装成.sh。参见 [[industrialization-roadmap]](迁移方案/贴码/工业化)、[[duco-controller-in-loop-bridge]](三机架构)、[[shelf-path-debug-workflow]](路径方法论,构型种子/q_near迁移讨论已定稿)
