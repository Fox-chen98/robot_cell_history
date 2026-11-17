#!/bin/bash
# Claude Code PostToolUse Hook - 自动版本管理提醒
# 在 Edit/Write 操作后检测未提交变更，超过阈值时提醒 Claude 执行 commit

# 不在 git 仓库中则静默退出
git rev-parse --is-inside-work-tree &>/dev/null || exit 0

# 冷却机制：同一仓库 2 分钟内不重复提醒
REPO_PATH=$(git rev-parse --show-toplevel 2>/dev/null | tr '/' '_')
COOLDOWN_FILE="/tmp/claude-autocommit${REPO_PATH}"

if [ -f "$COOLDOWN_FILE" ]; then
    last_remind=$(cat "$COOLDOWN_FILE" 2>/dev/null)
    now=$(date +%s)
    elapsed=$((now - last_remind))
    if [ "$elapsed" -lt 120 ]; then
        exit 0
    fi
fi

# 统计未提交的文件数（已修改 + 未跟踪）
changed_files=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')

# 无变更则退出
[ "$changed_files" -eq 0 ] 2>/dev/null && exit 0

# 文件阈值
FILE_THRESHOLD=${CLAUDE_AUTOCOMMIT_THRESHOLD:-5}

if [ "$changed_files" -ge "$FILE_THRESHOLD" ] 2>/dev/null; then
    # 记录提醒时间
    date +%s > "$COOLDOWN_FILE"

    # 输出 JSON 反馈给 Claude
    cat <<HOOKEOF
{
  "decision": "block",
  "reason": "版本管理提醒：当前有 ${changed_files} 个文件存在未提交的变更，已超过阈值(${FILE_THRESHOLD})。请先执行 git add 和 git commit 创建版本节点保存当前进度，然后再继续工作。"
}
HOOKEOF
fi

exit 0
