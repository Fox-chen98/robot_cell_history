# 全局规则

## 语言

- 始终使用简体中文回复

## 自动版本管理

在任何 git 仓库中工作时（本地或远程服务器），主动遵循以下版本管理规则：

### 何时自动 commit
- 完成一个功能模块或逻辑单元的编写后
- 累计修改了 3 个以上文件后
- 进行重构或大量删除代码之前（先提交当前状态作为安全快照）
- 修复一个 bug 后
- 收到 hook 的版本管理提醒时

### commit 规范
- 使用简洁的中文 commit message
- 格式：`<类型>: <描述>`，如 `feat: 添加用户登录功能`
- 类型：feat / fix / refactor / docs / style / test / chore
- 这是用户的明确授权，无需每次征求确认，直接提交即可
- 每次 commit 后简要告知用户提交了什么

### 远程服务器（SSH）版本管理
通过 SSH 在远程服务器上工作时，同样执行 git 版本管理：
- 通过 SSH 修改远程文件后，用 SSH 执行远程 git commit
- 每完成一个逻辑单元或连续执行多次文件修改后，主动通过 SSH 运行 `git add` + `git commit`
- 在远程服务器上开始新任务前，先通过 SSH 检查 `git status`，如有未提交变更先提交
- 远程 commit 示例：`ssh -p PORT user@host "cd /project && git add -A && git commit -m 'feat: 描述'"`

### 注意事项
- 不要提交 .env、密钥、credentials 等敏感文件
- 如果项目还没有 git 初始化，先询问用户是否需要 git init
- 不要使用 --no-verify 跳过 hooks

## 本机说明(blue-space, 2026-10-29 自 Mac 迁入)

- 本机 = 货架机器人的设备电脑(Windows)。主线在 `D:\robot_cell` 启动 Claude Code; 设备服务从 `D:\Destop\robot_cell` 运行。
- 主线对话、记忆、本文件里的规则都是 2026-10-29 从 Mac 迁来的; 迁来的对话和记忆里"ssh 到 blue-space"的写法 = 现在直接在本机执行, 换算表见 `D:\robot_cell\CLAUDE.md` 顶部。
- 本文件 = Mac 的全局规则 + 本机原有的"简体中文"规则合并; 原文件备份 `CLAUDE.md.bak_20261029`。
- 上面"远程服务器(SSH)版本管理"一节主要是 Mac 时代用的; 本机仓库直接 git commit。
