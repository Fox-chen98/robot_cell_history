---
name: ssh-controlmaster-hosting-pitfall
description: blue-space服务托管: 2026-10-29起视觉/工作站/上位机后端=Windows服务(WinSW, 无窗口/开机不登录/退出5s系统重启), 扫码仍计划任务; 勿经ssh直接拉进程; 历史坑汇总
metadata:
  type: feedback
---

~/.ssh/config 对 100.106.76.91 开了 ControlMaster auto; 视觉服务/工作站服务/上位机后端/隧道都是Mac侧 nohup ssh 托管的, 全挤在一条主连接上. 2026-09-09 清理隧道时杀到主连接 → 视觉服务两次无故消失, 工作站服务全站500(stdout断).

**Why:** 复用连接共享一个进程, 任一"杀掉某个ssh"都可能杀到主连接.
**How to apply:** 托管长驻服务与隧道的 ssh 一律加 `-o ControlMaster=no -o ControlPath=none`(vision_service.sh/cell_service.sh 已改); 按端口找进程杀隧道(lsof)而不是 pkill 模式. **根治已落地(2026-09-10)**: 计划任务 robot_cell_services_logon(登录时)+robot_cell_services_watchdog(每5分钟)跑 services\ensure_services.bat → run_service.bat 循环拉起, 桌面会话(Session 1)内, 开机即有; Mac 脚本 start 只发 `schtasks /run /tn robot_cell_services_watchdog`, cell_service.sh stop=重启. 经 ssh 直接跑 ensure 拉起的进程随会话死(实证). 旧孤儿进程占着端口时看门狗不接手, 要手动 taskkill. 手动开关三入口(scripts/svc.sh / services\svc.bat / 网页服务管理块+/services接口)同一机制, 按服务 hold_<name>.flag; bat 里 timeout 在 ssh 无 stdin 下会报错退出, 等待用 ping -n. 细节 docs/服务托管.md. 关联 [[deploy-wait-lesson]].

**2026-09-14 服务加固(实证三坑)**: ①端口在听≠活着: 扫码/视觉都出过僵死(扫码 ping 超时; 视觉相机 USB 断后 SDK 卡死不退出) → 看门狗 `ensure_services.bat` 加 `services/probe.py <name>` 按协议探活(20s 超时, 5s 后二次确认才杀; 单线程服务忙时 ping 会排队, 短超时会误杀), 计划任务改每 1 分钟(导出 XML 改 PT1M 重导入); `vision_server.py` 取帧>25s 自杀 / 相机重启失败即退出交给循环重连. ②看门狗每分钟查 + 循环启动器 5s 重启空档 → 会拉出第二个 `run_service` 循环, 症状是窗口报"另一个程序正在使用此文件"(活循环的 `>>` 重定向独占 service.log) → `run_service.bat` 开头数同名循环 >1 就退出(计数走临时文件, `for /f` 里套 PowerShell 引号会碎). ③bat 坑: 必须 CRLF+ASCII 注释(start_scan_service.bat 曾 LF+中文 rem 报"不是内部命令"); 子程序里标签不能带 %1(`goto :start_%1_chk` 找不到标签, 整个看门狗中断). 扫码键盘钩子的根治=扫码器切 USB-COM(德沃 DEWOD 7200DHS, 同系列官网标 USB-COM/RS232, 要设置码手册), 用户暂缓; 手动起停 `services\svc.bat status|start|stop|restart <name|all>`.

**2026-09-14 "卡死无报错"的第四坑 = 控制器客户端连接泄漏**: actions/guard.py 的运动看门狗每个任务开 1 条独立 DucoCobot 监视连接, 从不关闭; 8 个任务后 DUCO 控制器 7003 的客户端数占满(观察到 9 条 ESTABLISHED 全属 cell 进程), 之后任何 RPC(流程下一步、read_pose)都无限挂住、无任何报错. 诊断法: blue-space `netstat -ano | findstr 192.168.0.20:7003` 数 ESTABLISHED 并看归属 PID; 正常一个 DucoCobotArm connect=2 条(RPC+心跳)+guard 1 条, disconnect 后应归 0. 修复: guard.install 把监视连接挂 arm._guard_monitor 并包装 arm.disconnect 一起关(已实测归零). 应急: `svc.sh restart cell` 释放全部连接.

**2026-09-16 补**: 工作站服务(8902)常驻 → deploy_cell 推了新 .py 它仍跑内存旧代码, 而账本 json/yaml 是每次现读会立即生效, 两者混用最迷惑(当天网页任务用新账本层板高+旧公式推进量 499.2 而非 502.9). 规矩: 改了 scripts/bluespace 下 .py, 空闲时 `svc.sh restart cell`; deploy_cell 已加提醒. CLI act.sh/flow.sh 每次新进程不受影响, 验证要区分"CLI 过了"≠"网页过了".

**2026-10-29 改为 Windows 服务(现行)**: 用户嫌桌面黑窗口"不是成熟产品", 要"工业软件标准做法""足够稳定". vision/cell/upper → WinSW v2.12.0 服务 RobotCellVision/Cell/Upper(LocalSystem, Session 0, Automatic), 主体 `services\svc_run.bat <name>`: python 怎么结束都 exit 1(→SCM 5s 重启, 不限次), 有 hold 旗才 exit 0(服务停住); 看门狗照旧每分钟探活, 端口不在就 `sc start`. 安装 `services\install_services.ps1 install|uninstall|status`(一条命令). **自动模式分类器会拦"下载 WinSW 并安装"**, 要用户自己 `! ssh ... install`. 普通权限窗口杀不动系统账户进程 → 设备控制台重启改走 `POST /services/<名>/restart`. 相机/CUDA 在系统账户下正常(实测). 扫码不能做服务(键盘钩子只在登录桌面会话), 可隐藏窗口, 根治仍是 USB-COM. 待用户: 重启电脑不登录验证自启. 详见 docs/服务托管.md 开头"现状".

**2026-10-29 续**: 扫码改隐藏窗口(任务动作 wscript scan_hidden.vbs, 实测钩子照常收码). 桌面控制台换 tkinter 图形版 console_gui.py(pythonw, 平时不必开). ⚠ 坑: 控制台首版每 2 秒 connect 8901/8900 探活 → 单线程服务日志刷 "unknown cmd" 且可能抢任务连接; 改查 netstat 监听表. 探活别连单线程服务. 排查表/待优化清单在 docs/服务托管.md.
