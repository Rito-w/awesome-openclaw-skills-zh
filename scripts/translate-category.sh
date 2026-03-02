#!/bin/bash
# translate-category.sh - 翻译分类文件
# 用法：./translate-category.sh <category-file.md>

set -e

if [ -z "$1" ]; then
    echo "用法：$0 <category-file.md>"
    echo "示例：$0 categories/git-and-github.md"
    exit 1
fi

INPUT_FILE="$1"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 检查文件是否存在
if [ ! -f "$PROJECT_DIR/$INPUT_FILE" ]; then
    UPSTREAM_DIR="/Volumes/myDisk/workplace/awesome-openclaw-skills"
    if [ -f "$UPSTREAM_DIR/$INPUT_FILE" ]; then
        echo "📥 从上游复制：$INPUT_FILE"
        cp "$UPSTREAM_DIR/$INPUT_FILE" "$PROJECT_DIR/$INPUT_FILE"
    else
        echo "❌ 文件不存在：$PROJECT_DIR/$INPUT_FILE"
        exit 1
    fi
fi

echo "📝 准备翻译：$INPUT_FILE"

# 读取文件内容
CONTENT=$(cat "$PROJECT_DIR/$INPUT_FILE")

# 提取标题（第一行）
TITLE=$(echo "$CONTENT" | head -1 | sed 's/^# //')

# 简单翻译映射
case "$TITLE" in
    "Git & GitHub") CN_TITLE="Git & GitHub" ;;
    "Coding Agents & IDEs") CN_TITLE="编码代理与 IDE" ;;
    "Browser & Automation") CN_TITLE="浏览器与自动化" ;;
    "Web & Frontend Development") CN_TITLE="Web 与前端开发" ;;
    "DevOps & Cloud") CN_TITLE="DevOps 与云" ;;
    "AI & LLMs") CN_TITLE="AI 与大语言模型" ;;
    "Data & Analytics") CN_TITLE="数据分析" ;;
    "Communication") CN_TITLE="通讯" ;;
    "Productivity & Tasks") CN_TITLE="生产力与任务" ;;
    "Search & Research") CN_TITLE="搜索与研究" ;;
    "Image & Video Generation") CN_TITLE="图像与视频生成" ;;
    "Media & Streaming") CN_TITLE="媒体与流媒体" ;;
    "PDF & Documents") CN_TITLE="PDF 与文档" ;;
    "Apple Apps & Services") CN_TITLE="Apple 应用与服务" ;;
    "Notes & PKM") CN_TITLE="笔记与 PKM" ;;
    "Self-Hosted & Automation") CN_TITLE="自托管与自动化" ;;
    "Security & Passwords") CN_TITLE="安全与密码" ;;
    "Calendar & Scheduling") CN_TITLE="日历与日程" ;;
    "Shopping & E-commerce") CN_TITLE="购物与电商" ;;
    "Smart Home & IoT") CN_TITLE="智能家居与 IoT" ;;
    "Speech & Transcription") CN_TITLE="语音与转录" ;;
    "Transportation") CN_TITLE="交通" ;;
    "Personal Development") CN_TITLE="个人发展" ;;
    "Gaming") CN_TITLE="游戏" ;;
    "Health & Fitness") CN_TITLE="健康与健身" ;;
    "CLI Utilities") CN_TITLE="CLI 工具" ;;
    "Clawdbot Tools") CN_TITLE="Clawdbot 工具" ;;
    "Moltbook") CN_TITLE="Moltbook" ;;
    "Finance") CN_TITLE="金融" ;;
    "iOS & macOS Development") CN_TITLE="iOS 与 macOS 开发" ;;
    "Agent-to-Agent Protocols") CN_TITLE="Agent 间协议" ;;
    *) CN_TITLE="$TITLE" ;;
esac

# 提取技能数量
SKILL_COUNT=$(echo "$CONTENT" | grep -E '\*\*[0-9]+ skills\*\*' | grep -oE '[0-9]+' | head -1)
if [ -z "$SKILL_COUNT" ]; then
    SKILL_COUNT="未知"
fi

echo "原标题：$TITLE"
echo "中文标题：$CN_TITLE"
echo "技能数量：$SKILL_COUNT"

# 创建翻译版本
OUTPUT_FILE="${INPUT_FILE%.md}.zh.md"

cat > "$PROJECT_DIR/$OUTPUT_FILE" << EOF
# $CN_TITLE

[← 返回主列表](../README.md#目录)

**技能数量：** $SKILL_COUNT

---

> 📝 **说明：** 以下技能列表保持英文原文，以确保链接和描述准确性。
> 分类名称和元数据已翻译为中文。

---

$CONTENT

---

*本分类翻译由社区维护。如需改进翻译质量，欢迎提交 PR。*
EOF

echo ""
echo "✅ 翻译完成：$OUTPUT_FILE"
