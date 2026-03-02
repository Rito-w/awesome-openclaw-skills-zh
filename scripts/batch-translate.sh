#!/bin/bash
# batch-translate.sh - 使用 Claude Code 批量翻译 Markdown 文件
# 用法：./batch-translate.sh <file-or-directory>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
UPSTREAM_DIR="/Volumes/myDisk/workplace/awesome-openclaw-skills"
LOG_FILE="$SCRIPT_DIR/translate-log.txt"

translate_file() {
    local input_file="$1"
    local output_file="$2"
    
    echo "📝 翻译：$input_file → $output_file"
    
    # 检查是否需要从上游复制
    if [ ! -f "$PROJECT_DIR/$input_file" ] && [ -f "$UPSTREAM_DIR/$input_file" ]; then
        cp "$UPSTREAM_DIR/$input_file" "$PROJECT_DIR/$input_file"
    fi
    
    if [ ! -f "$PROJECT_DIR/$input_file" ]; then
        echo "  ⚠️  文件不存在：$PROJECT_DIR/$input_file" | tee -a "$LOG_FILE"
        return 1
    fi
    
    # 使用 Claude Code 翻译（后台运行）
    cd "$PROJECT_DIR"
    cat > "$SCRIPT_DIR/translate-task.txt" << EOF
请翻译此 Markdown 文件为中文。

【翻译规则】
1. 保留所有链接、代码块、图片和 HTML 标签不变
2. 只翻译可见文本（标题、描述、元数据）
3. 保持技能名称和 URL 为英文
4. 保持 Markdown 结构完全不变
5. 输出 ONLY 翻译后的内容，不要解释

【输入文件】$PROJECT_DIR/$input_file
【输出文件】$PROJECT_DIR/$output_file

请直接读取输入文件，翻译后写入输出文件。
EOF
    
    # 启动 Claude Code 任务（异步）
    nohup claude "@$SCRIPT_DIR/translate-task.txt" > "$SCRIPT_DIR/claude-output.log" 2>&1 &
    CLAUDE_PID=$!
    
    echo "  🔄 Claude Code 任务已启动 (PID: $CLAUDE_PID)" | tee -a "$LOG_FILE"
    echo "$input_file|$output_file|$CLAUDE_PID|$(date '+%Y-%m-%d %H:%M:%S')" >> "$SCRIPT_DIR/pending-translations.csv"
    
    return 0
}

# 主逻辑
if [ -z "$1" ]; then
    echo "用法：$0 <file-or-directory>"
    echo ""
    echo "示例:"
    echo "  $0 README.md"
    echo "  $0 categories/git-and-github.md"
    echo "  $0 categories/  # 翻译所有分类文件"
    exit 1
fi

TARGET="$1"

if [ -d "$PROJECT_DIR/$TARGET" ]; then
    # 目录：翻译所有 .md 文件
    echo "📂 翻译目录：$TARGET"
    echo ""
    
    SUCCESS=0
    FAILED=0
    
    for file in "$PROJECT_DIR/$TARGET"/*.md; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            # 跳过已翻译的文件
            if [[ "$filename" == *.zh.md ]]; then
                continue
            fi
            
            output_name="${filename%.md}.zh.md"
            input_path="$TARGET/$filename"
            output_path="$TARGET/$output_name"
            
            translate_file "$input_path" "$output_path"
            if [ $? -eq 0 ]; then
                ((SUCCESS++))
            else
                ((FAILED++))
            fi
        fi
    done
    
    echo ""
    echo "=== 翻译完成 ==="
    echo "成功：$SUCCESS"
    echo "失败：$FAILED"
    
elif [ -f "$PROJECT_DIR/$TARGET" ]; then
    # 单文件
    filename=$(basename "$TARGET")
    output_name="${filename%.md}.zh.md"
    output_path="${TARGET%.md}.zh.md"
    
    translate_file "$TARGET" "$output_path"
    
else
    echo "❌ 文件/目录不存在：$TARGET"
    exit 1
fi
