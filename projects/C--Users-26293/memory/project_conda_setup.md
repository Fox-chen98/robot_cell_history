---
name: project-conda-setup
description: 用户的 conda 安装位置、环境列表、PowerShell 7 兼容性修复要点
metadata: 
  node_type: memory
  type: project
  originSessionId: ba687cb7-0b5d-4863-925d-4d0753969381
---

# 用户的 conda 安装

- **conda 本体**：`D:\miniconda`（Miniconda3，conda 版本 23.5.2）
- **环境目录**：`C:\Users\26293\.conda\envs\`
  - `camera_test`
  - `robot`
- **base 环境**：`D:\miniconda`（不在 .conda 下）

# 已知坑：conda 23.5.2 + PowerShell 7 不兼容

**症状**：在 pwsh（7+）里跑 `conda` 报 `'conda' is not recognized` 或 `Missing '{' in configuration statement`，但在 `powershell.exe`（5.1）和 Anaconda Prompt（cmd）里正常。

**根因**：conda 23.5.2 自带的 `D:\miniconda\shell\condabin\Conda.psm1` 用 `& $Env:CONDA_EXE $Env:_CE_M $Env:_CE_CONDA ...` 调用 conda，这两个环境变量是空字符串。PS 5.1 自动丢弃空参数，PS 7 会把空字符串当真实参数传过去，conda.exe 收到无效命令返回 help 文本，被当 PowerShell 代码解析时崩溃。

**修复**：在 PS 7 profile `C:\Users\26293\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` 顶部加：
```powershell
$PSNativeCommandArgumentPassing = 'Legacy'
```
然后是标准的 conda hook 那段。

**Why**：用户在 2026-05 报告"conda 突然用不了了"，怀疑是 C 盘清理导致——实际是 VSCode/Windows 终端切到了 pwsh 暴露的隐患。conda 24+ 已修。

**How to apply**：用户升级 conda 到 24+ 就可以删掉 Legacy 那行。如果未来用户报告类似"某个 shell 里的命令突然失效"，先确认是不是 pwsh 7 与某个老脚本的传参不兼容，而不是怀疑是清理动作误删。
