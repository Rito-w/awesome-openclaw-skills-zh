#!/bin/bash
# sync-from-upstream.sh - 从上游仓库同步更新
# 用法：./sync-from-upstream.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
UPSTREAM_URL="https://github.com/VoltAgent/awesome-openclaw-skills.git"
UPSTREAM_NAME="upstream"

cd "$PROJECT_DIR"

echo "=== OpenClaw Skills 中文版同步脚本 ==="
echo "项目目录：$PROJECT_DIR"
echo "上游仓库：$UPSTREAM_URL"
echo ""

# 1. 添加或更新 upstream remote
if git remote | grep -q "^${UPSTREAM_NAME}$"; then
    git remote set-url "$UPSTREAM_NAME" "$UPSTREAM_URL"
    echo "✓ 更新 upstream remote"
else
    git remote add "$UPSTREAM_NAME" "$UPSTREAM_URL"
    echo "✓ 添加 upstream remote"
fi

# 2. 获取上游最新提交
echo ""
echo "📥 获取上游最新提交..."
git fetch "$UPSTREAM_NAME" main --depth=1

# 3. 识别变更文件
echo ""
echo "🔍 识别变更文件..."
CHANGED_FILES=$(git diff --name-only HEAD.."$UPSTREAM_NAME/main" 2>/dev/null || echo "")

if [ -z "$CHANGED_FILES" ]; then
    echo "✅ 没有新变更，已是最新状态"
    exit 0
fi

echo "发现变更文件:"
echo "$CHANGED_FILES" | while read -r file; do
    echo "  - $file"
done

# 4. 筛选需要翻译的文件（.md 文件）
MD_FILES=$(echo "$CHANGED_FILES" | grep "\.md$" || echo "")

if [ -z "$MD_FILES" ]; then
    echo ""
    echo "ℹ️  变更中没有 Markdown 文件，无需翻译"
else
    echo ""
    echo "📝 需要翻译的文件:"
    echo "$MD_FILES" | while read -r file; do
        echo "  - $file"
    done
    
    # 保存到待翻译列表
    echo "$MD_FILES" > "$SCRIPT_DIR/pending-translate.txt"
    echo ""
    echo "💾 待翻译列表已保存到：$SCRIPT_DIR/pending-translate.txt"
fi

# 5. 拉取上游更新（保留本地翻译）
echo ""
echo "🔄 拉取上游更新..."
git merge "$UPSTREAM_NAME/main" --strategy-option=ours --no-commit || true

# 6. 生成同步报告
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
cat > "$SCRIPT_DIR/sync-report.md" << EOF
# 同步报告 - $TIMESTAMP

## 变更摘要
- 上游提交：$(git rev-parse --short "$UPSTREAM_NAME/main")
- 本地提交：$(git rev-parse --short HEAD)
- 变更文件数：$(echo "$CHANGED_FILES" | wc -l | tr -d ' ')
- 待翻译文件：$(echo "$MD_FILES" | grep -c "\.md$" || echo 0)

## 变更文件列表
\`\`\`
$CHANGED_FILES
\`\`\`

## 下一步
1. 审查变更内容
2. 翻译新增/修改的 Markdown 文件
3. 提交翻译结果
EOF

echo ""
echo "📊 同步报告已生成：$SCRIPT_DIR/sync-report.md"
echo ""
echo "✅ 同步完成！请审查变更并翻译新增内容。"
