# -*- coding: utf-8 -*-
"""把本机的 Claude Code 历史对话、记忆和配置原样收集到本仓库。

- 只复制, 不修改、不删除任何原始文件
- 超过 90MB 的文件按行切成多段 (xxx.part001, xxx.part002 ...),
  按顺序拼接即可还原成与原件完全相同的文件
- 不会复制登录凭证

用法: 把本脚本放在 robot_cell_history 仓库的根目录, 然后运行
    python collect_history.py
"""
import os
import re
import shutil
import sys
from pathlib import Path

HOME_CLAUDE = Path.home() / ".claude"
PROJECT = Path(os.environ.get("PROJECT_DIR", r"D:\robot_cell"))
DEST = Path(__file__).resolve().parent

SPLIT_OVER = int(os.environ.get("SPLIT_OVER", 90 * 1024 * 1024))   # 超过这个大小就切分
PART_SIZE = int(os.environ.get("PART_SIZE", 80 * 1024 * 1024))     # 每段的目标大小
SKIP_BAK = True   # 跳过 *.jsonl.bak_* 备份副本(与正式文件内容重复); 想一并上传就改成 False

# (来源, 在仓库里的位置)
ITEMS = [
    (HOME_CLAUDE / "CLAUDE.md", "global/CLAUDE.md"),
    (HOME_CLAUDE / "settings.json", "global/settings.json"),
    (HOME_CLAUDE / "history.jsonl", "global/history.jsonl"),
    (HOME_CLAUDE / "skills", "global/skills"),
    (HOME_CLAUDE / "scripts", "global/scripts"),
    (HOME_CLAUDE / "交接工具", "global/交接工具"),
    (HOME_CLAUDE / "projects", "projects"),
    (HOME_CLAUDE / "projects_归档_20261029", "projects_归档_20261029"),
    (PROJECT / ".claude" / "settings.local.json", "project-local/settings.local.json"),
    (PROJECT / "CLAUDE.local.md", "project-local/CLAUDE.local.md"),
]

NEVER = {".credentials.json", ".claude.json"}
SECRET_RE = re.compile(rb"sk-ant-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}")

stats = {"files": 0, "bytes": 0, "split": [], "skipped": [], "errors": [], "secrets": [], "big_lines": []}


def scan_secrets(chunk, src):
    if SECRET_RE.search(chunk) and str(src) not in stats["secrets"]:
        stats["secrets"].append(str(src))


def copy_split(src, dst):
    """按行切分大文件, 每段不超过 PART_SIZE (单行超长时该行独占一段)。"""
    n = 0
    out = None
    size = 0
    with open(src, "rb") as fh:
        for line in fh:
            scan_secrets(line, src)
            if out is None or (size > 0 and size + len(line) > PART_SIZE):
                if out:
                    out.close()
                n += 1
                out = open(str(dst) + ".part%03d" % n, "wb")
                size = 0
            out.write(line)
            size += len(line)
            if len(line) > 95 * 1024 * 1024:
                stats["big_lines"].append("%s 第 %d 段" % (src.name, n))
    if out:
        out.close()
    stats["split"].append("%s (%.0f MB) -> %d 段" % (src.name, src.stat().st_size / 1048576, n))


def copy_file(src, dst):
    if src.name in NEVER:
        return
    if SKIP_BAK and ".jsonl.bak" in src.name:
        stats["skipped"].append(str(src))
        return
    try:
        size = src.stat().st_size
        dst.parent.mkdir(parents=True, exist_ok=True)
        if size > SPLIT_OVER:
            copy_split(src, dst)
        else:
            with open(src, "rb") as fh:
                data = fh.read()
            scan_secrets(data, src)
            with open(dst, "wb") as out:
                out.write(data)
        stats["files"] += 1
        stats["bytes"] += size
    except Exception as e:  # 权限不足等
        stats["errors"].append("%s: %s" % (src, e))


def copy_tree(src, dst):
    try:
        entries = sorted(os.scandir(src), key=lambda e: e.name)
    except Exception as e:
        stats["errors"].append("%s: %s" % (src, e))
        return
    for e in entries:
        p = Path(e.path)
        try:
            is_dir = e.is_dir(follow_symlinks=False)
        except Exception as ex:
            stats["errors"].append("%s: %s" % (p, ex))
            continue
        if is_dir:
            copy_tree(p, dst / e.name)
        else:
            copy_file(p, dst / e.name)


README = """# robot_cell_history

本仓库是 robot_cell 项目在本地 Windows 设备上用 Claude Code 开发期间的原始存档, 只读备查。

- `projects/D--robot-cell/`: 本项目的历史对话记录 (每个 .jsonl 是一次对话, 一行一条消息) 和 `memory/` 记忆文件
- `projects/` 下其他文件夹: 同一台设备上其他目录的对话
- `projects_归档_20261029/`: 2026-10-29 归档的更早期对话 (含本项目 robot_code 时期的早期调试)
- `global/`: 全局配置 (CLAUDE.md, settings.json, 自定义技能/脚本, history.jsonl 为输入过的全部提问)
- `project-local/`: 项目内仅本机的配置 (如果有)

超过 90MB 的对话文件按行切成了多段: `xxx.jsonl.part001`, `part002` ...
每段都是完整的若干行, 可以直接逐段读取或搜索; 按顺序拼接即还原为原文件。
对话文件里夹带大量 base64 图片数据, 搜索时建议用 grep/ripgrep 按关键词查找, 不要整个读入。
"""


def main():
    if not HOME_CLAUDE.is_dir():
        sys.exit("找不到 %s" % HOME_CLAUDE)
    if not (DEST / ".git").exists():
        sys.exit("请把本脚本放在 robot_cell_history 仓库的根目录下再运行 (当前目录不是 Git 仓库: %s)" % DEST)
    for src, rel in ITEMS:
        if not src.exists():
            print("  (不存在, 跳过) %s" % src)
            continue
        print("复制 %s" % src)
        if src.is_dir():
            copy_tree(src, DEST / rel)
        else:
            copy_file(src, DEST / rel)
    (DEST / "README.md").write_text(README, encoding="utf-8")

    print("\n===== 结果 =====")
    print("共复制 %d 个文件, %.1f MB" % (stats["files"], stats["bytes"] / 1048576))
    for s in stats["split"]:
        print("已切分: " + s)
    for s in stats["skipped"]:
        print("已跳过备份副本: " + s)
    for s in stats["errors"]:
        print("!! 没能复制: " + s)
    for s in stats["big_lines"]:
        print("!! 单行超过 95MB, GitHub 可能拒收: " + s)
    for s in stats["secrets"]:
        print("!! 发现疑似密钥(API key / GitHub token), 推送前请先告诉我: " + s)
    if not (stats["errors"] or stats["big_lines"] or stats["secrets"]):
        print("没有发现问题。")


if __name__ == "__main__":
    main()
