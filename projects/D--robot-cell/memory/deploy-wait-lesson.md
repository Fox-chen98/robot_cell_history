---
name: deploy-wait-lesson
description: "部署后不要长时间阻塞等ssh回显——实际生效远快于回显,用户画面早已更新"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9953535e-7aeb-4fd0-b37d-4185895077fe
  modified: 2026-08-13T01:26:46.054Z
---

2026-08-13 用户打断长等待:"运行太久了,而我的仿真页面早就出现了,成功了"。AutoDL 的 ssh 回显经常慢/卡(假超时),但服务器端命令实际早已执行完,Foxglove 画面已更新。

**Why:** 我的 until-loop 等回显动辄 2-5 分钟,用户被晾着;而真正的验收人是看着 Foxglove 的用户,不是我的 grep。

**2026-08-13定稿铁规: 所有 .sh 脚本一律用户手动执行**——我只给出命令,需要结果时请用户贴回输出;我仅在必须程序化解析输出且用户不在场时才代跑。诊断用的单条只读命令(ssh探活/ls/grep)不受限。

**How to apply:** deploy/overlay 类操作发出后,后台跑即可,立刻告诉用户"请刷新查看";验证交给用户目视或事后快速单查(pgrep/单条ssh),不要前台阻塞等长输出。ssh 卡≠失败,先单独探一条 `ssh autodl echo OK` 判活。2026-08-13补充: 用户反馈"你(AI代跑)比我手动运行慢多了"——AI工具通道有调用开销+轮询等待,终端是即时流式。**部署/构建类操作默认让用户手动跑**(告知命令即可),AI只在需要程序化解析输出时代跑。另: 服务器常驻进程启动必须 `>log 2>&1 </dev/null &` 三件套,少了stdin重定向ssh会假挂起不返回。参见 [[scene-sim-rebuild]]。
