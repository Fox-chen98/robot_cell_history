# robot_cell_history

本仓库是 robot_cell 项目在本地 Windows 设备上用 Claude Code 开发期间的原始存档, 只读备查。

- `projects/D--robot-cell/`: 本项目的历史对话记录 (每个 .jsonl 是一次对话, 一行一条消息) 和 `memory/` 记忆文件
- `projects/` 下其他文件夹: 同一台设备上其他目录的对话
- `projects_归档_20261029/`: 2026-10-29 归档的更早期对话 (含本项目 robot_code 时期的早期调试)
- `global/`: 全局配置 (CLAUDE.md, settings.json, 自定义技能/脚本, history.jsonl 为输入过的全部提问)
- `project-local/`: 项目内仅本机的配置 (如果有)

超过 90MB 的对话文件按行切成了多段: `xxx.jsonl.part001`, `part002` ...
每段都是完整的若干行, 可以直接逐段读取或搜索; 按顺序拼接即还原为原文件。
对话文件里夹带大量 base64 图片数据, 搜索时建议用 grep/ripgrep 按关键词查找, 不要整个读入。
