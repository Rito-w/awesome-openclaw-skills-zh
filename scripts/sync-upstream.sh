#!/bin/bash
# sync-upstream.sh - 同步上游仓库更新并重新翻译变更的文件
# 
# 用法:
#   ./sync-upstream.sh           # 检查并同步更新
#   ./sync-upstream.sh --force   # 强制重新翻译所有文件
#   ./sync-upstream.sh --status  # 查看同步状态

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
UPSTREAM_DIR="/Volumes/myDisk/workplace/awesome-openclaw-skills"
UPSTREAM_URL="https://github.com/VoltAgent/awesome-openclaw-skills.git"
SYNC_LOG="$SCRIPT_DIR/sync-log.txt"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$SYNC_LOG"
}

# 分类列表
CATEGORIES=(
    "ai-and-llms" "apple-apps-and-services" "browser-and-automation"
    "calendar-and-scheduling" "clawdbot-tools" "cli-utilities"
    "coding-agents-and-ides" "communication" "data-and-analytics"
    "devops-and-cloud" "gaming" "git-and-github" "health-and-fitness"
    "image-and-video-generation" "ios-and-macos-development"
    "marketing-and-sales" "media-and-streaming" "moltbook"
    "notes-and-pkm" "pdf-and-documents" "personal-development"
    "productivity-and-tasks" "search-and-research" "security-and-passwords"
    "self-hosted-and-automation" "shopping-and-e-commerce"
    "smart-home-and-iot" "speech-and-transcription" "transportation"
    "web-and-frontend-development"
)

show_status() {
    echo "=== 翻译状态 ==="
    echo ""
    
    completed=0
    pending=0
    
    for cat in "${CATEGORIES[@]}"; do
        output_file="$PROJECT_DIR/categories/${cat}.zh.md"
        if [ -f "$output_file" ]; then
            echo "✅ ${cat}.zh.md"
            ((completed++))
        else
            echo "⏳ ${cat}.zh.md"
            ((pending++))
        fi
    done
    
    echo ""
    echo "总计：${#CATEGORIES[@]} | 已完成：$completed | 待翻译：$pending"
}

check_upstream_changes() {
    log "📥 检查上游仓库更新..."
    
    cd "$UPSTREAM_DIR"
    
    # 获取最新提交
    git fetch origin main --depth=1 2>/dev/null || {
        log "⚠️  无法获取上游更新"
        return 1
    }
    
    # 比较本地和上游
    LOCAL_COMMIT=$(git rev-parse HEAD)
    UPSTREAM_COMMIT=$(git rev-parse origin/main)
    
    if [ "$LOCAL_COMMIT" == "$UPSTREAM_COMMIT" ]; then
        log "✅ 已是最新，无需同步"
        return 0
    fi
    
    log "📊 本地提交：$LOCAL_COMMIT"
    log "📊 上游提交：$UPSTREAM_COMMIT"
    
    # 获取变更的文件
    CHANGED_FILES=$(git diff --name-only "$LOCAL_COMMIT".."$UPSTREAM_COMMIT" | grep "^categories/" | grep "\.md$" || echo "")
    
    if [ -z "$CHANGED_FILES" ]; then
        log "✅ 分类文件无变更"
        return 0
    fi
    
    log "📝 发现变更的分类文件:"
    echo "$CHANGED_FILES" | while read -r file; do
        log "  - $file"
    done
    
    # 输出需要重新翻译的分类
    echo "$CHANGED_FILES" | sed 's|categories/||g' | sed 's|\.md||g' > "$SCRIPT_DIR/categories-to-update.txt"
    
    log "💾 待更新列表：$SCRIPT_DIR/categories-to-update.txt"
    return 0
}

sync_and_retranslate() {
    log "=== 开始同步并重新翻译 ==="
    
    # 拉取上游更新
    cd "$UPSTREAM_DIR"
    git pull origin main --ff-only || {
        log "⚠️  拉取失败，继续处理..."
    }
    
    # 读取需要更新的分类
    if [ ! -f "$SCRIPT_DIR/categories-to-update.txt" ]; then
        log "✅ 无需更新"
        return 0
    fi
    
    CATEGORIES_TO_UPDATE=$(cat "$SCRIPT_DIR/categories-to-update.txt")
    
    if [ -z "$CATEGORIES_TO_UPDATE" ]; then
        log "✅ 无需更新"
        return 0
    fi
    
    log "📝 需要重新翻译的分类:"
    echo "$CATEGORIES_TO_UPDATE" | while read -r cat; do
        log "  - $cat"
    done
    
    # 删除旧的翻译文件
    echo "$CATEGORIES_TO_UPDATE" | while read -r cat; do
        output_file="$PROJECT_DIR/categories/${cat}.zh.md"
        if [ -f "$output_file" ]; then
            rm "$output_file"
            log "🗑️  删除旧版：${cat}.zh.md"
        fi
    done
    
    # 使用 auto-dispatch.py 重新翻译
    log "🚀 派发重新翻译任务..."
    cd "$PROJECT_DIR"
    python3 "$SCRIPT_DIR/auto-dispatch.py" --all
    
    log "✅ 同步完成！"
}

# 主逻辑
case "${1:-}" in
    --status)
        show_status
        ;;
    --force)
        log "🔄 强制重新翻译所有分类..."
        for cat in "${CATEGORIES[@]}"; do
            output_file="$PROJECT_DIR/categories/${cat}.zh.md"
            if [ -f "$output_file" ]; then
                rm "$output_file"
                log "🗑️  删除：${cat}.zh.md"
            fi
        done
        python3 "$SCRIPT_DIR/auto-dispatch.py" --all
        ;;
    --check)
        check_upstream_changes
        ;;
    *)
        check_upstream_changes
        if [ -f "$SCRIPT_DIR/categories-to-update.txt" ] && [ -s "$SCRIPT_DIR/categories-to-update.txt" ]; then
            sync_and_retranslate
        else
            show_status
        fi
        ;;
esac
