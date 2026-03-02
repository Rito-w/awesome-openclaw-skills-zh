#!/bin/bash
# dispatch-translate.sh - 使用 sessions_spawn 派发翻译任务
# 用法：./dispatch-translate.sh <category-name|--all>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
UPSTREAM_DIR="/Volumes/myDisk/workplace/awesome-openclaw-skills"
TASKS_LOG="$SCRIPT_DIR/translate-tasks.log"

# 分类列表
CATEGORIES=(
    "ai-and-llms"
    "apple-apps-and-services"
    "browser-and-automation"
    "calendar-and-scheduling"
    "clawdbot-tools"
    "cli-utilities"
    "coding-agents-and-ides"
    "communication"
    "data-and-analytics"
    "devops-and-cloud"
    "gaming"
    "git-and-github"
    "health-and-fitness"
    "image-and-video-generation"
    "ios-and-macos-development"
    "marketing-and-sales"
    "media-and-streaming"
    "moltbook"
    "notes-and-pkm"
    "pdf-and-documents"
    "personal-development"
    "productivity-and-tasks"
    "search-and-research"
    "security-and-passwords"
    "self-hosted-and-automation"
    "shopping-and-e-commerce"
    "smart-home-and-iot"
    "speech-and-transcription"
    "transportation"
    "web-and-frontend-development"
)

translate_category() {
    local category="$1"
    local input_file="$UPSTREAM_DIR/categories/${category}.md"
    local output_file="$PROJECT_DIR/categories/${category}.zh.md"
    
    if [ -f "$output_file" ]; then
        echo "⏭️  已存在：${category}.zh.md"
        return 0
    fi
    
    if [ ! -f "$input_file" ]; then
        echo "❌ 上游文件不存在：${category}.md"
        return 1
    fi
    
    echo "📝 派发翻译任务：${category}.md"
    
    # 创建任务描述
    local task="请将以下 Markdown 文件完整翻译为中文：

【输入文件】$input_file
【输出文件】$output_file

【翻译规则】
1. 完整翻译所有内容，包括每个技能的描述
2. 保持技能名称为英文（如 git-helper）
3. 保留所有链接、代码块、图片、HTML 标签不变
4. 移除所有赞助商相关内容（Gold/Silver/Bronze Sponsor 段落）
5. 在文件末尾添加来源标注：
   ---
   *翻译自：https://github.com/VoltAgent/awesome-openclaw-skills/blob/main/categories/${category}.md*
   *翻译时间：$(date '+%Y-%m-%d %H:%M:%S')*

请读取输入文件，翻译后写入输出文件。完成后回复确认。"

    # 使用 sessions_spawn 派发任务
    # 注意：这里我们创建任务文件，稍后由外部脚本处理
    local task_file="$SCRIPT_DIR/tasks/${category}.task"
    mkdir -p "$SCRIPT_DIR/tasks"
    
    echo "$task" > "$task_file"
    echo "${category}|${input_file}|${output_file}|pending|$(date '+%Y-%m-%d %H:%M:%S')" >> "$TASKS_LOG"
    
    echo "  ✅ 任务已创建：$task_file"
    return 0
}

# 主逻辑
if [ -z "$1" ]; then
    echo "用法：$0 <category-name|--all|--status>"
    echo ""
    echo "示例:"
    echo "  $0 git-and-github     # 翻译单个分类"
    echo "  $0 --all              # 翻译所有分类"
    echo "  $0 --status           # 查看翻译状态"
    exit 1
fi

if [ "$1" == "--status" ]; then
    echo "=== 翻译任务状态 ==="
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
    exit 0
fi

if [ "$1" == "--all" ]; then
    echo "=== 批量翻译所有分类 ==="
    echo "分类数：${#CATEGORIES[@]}"
    echo ""
    
    for cat in "${CATEGORIES[@]}"; do
        translate_category "$cat"
    done
    
    echo ""
    echo "=== 任务派发完成 ==="
    echo "任务文件位于：$SCRIPT_DIR/tasks/"
    echo "任务日志：$TASKS_LOG"
    echo ""
    echo "💡 下一步：使用以下命令处理任务队列"
    echo "   cd $PROJECT_DIR"
    echo "   # 手动或使用自动化脚本处理 tasks/ 目录中的任务"
    exit 0
fi

# 单个分类
translate_category "$1"
