#!/usr/bin/env python3
"""
dispatch-all.py - 批量派发翻译任务（简化版）

直接输出所有待翻译任务的提示词，方便手动或脚本派发。

用法:
    python3 dispatch-all.py              # 输出所有待翻译任务
    python3 dispatch-all.py --list       # 仅列出文件名
    python3 dispatch-all.py --next 5     # 输出接下来 5 个任务
"""

import json
import sys
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(__file__).parent.parent
UPSTREAM_DIR = Path("/Volumes/myDisk/workplace/awesome-openclaw-skills")
SCRIPT_DIR = Path(__file__).parent
STATE_FILE = SCRIPT_DIR / "dispatch-state.json"

CATEGORIES = [
    "ai-and-llms", "apple-apps-and-services", "browser-and-automation",
    "calendar-and-scheduling", "clawdbot-tools", "cli-utilities",
    "coding-agents-and-ides", "communication", "data-and-analytics",
    "devops-and-cloud", "gaming", "git-and-github", "health-and-fitness",
    "image-and-video-generation", "ios-and-macos-development",
    "marketing-and-sales", "media-and-streaming", "moltbook",
    "notes-and-pkm", "pdf-and-documents", "personal-development",
    "productivity-and-tasks", "search-and-research", "security-and-passwords",
    "self-hosted-and-automation", "shopping-and-e-commerce",
    "smart-home-and-iot", "speech-and-transcription", "transportation",
    "web-and-frontend-development",
]

# 已完成
COMPLETED = {"git-and-github", "ai-and-llms"}


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"completed": list(COMPLETED)}


def get_pending():
    state = load_state()
    completed = set(state.get("completed", COMPLETED))
    
    pending = []
    for cat in CATEGORIES:
        output_file = PROJECT_DIR / "categories" / f"{cat}.zh.md"
        if cat not in completed or not output_file.exists():
            pending.append(cat)
    
    return pending


def create_prompt(category):
    input_file = UPSTREAM_DIR / "categories" / f"{category}.md"
    output_file = PROJECT_DIR / "categories" / f"{category}.zh.md"
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    return f"""请翻译此 OpenClaw Skills 分类文件为中文。

【任务】
- 输入：{input_file}
- 输出：{output_file}

【翻译规则】
1. 完整翻译所有内容，包括每个技能的描述
2. 保持技能名称为英文（如 git-helper）
3. 保留所有链接、代码块、图片、HTML 标签不变
4. 移除所有赞助商相关内容（Gold/Silver/Bronze Sponsor 段落）
5. 在文件末尾添加来源标注

【来源标注格式】
---
*翻译自：https://github.com/VoltAgent/awesome-openclaw-skills/blob/main/categories/{category}.md*
*翻译时间：{date_str}*

请读取输入文件，翻译后写入输出文件。完成后回复"✅ 完成：{category}.zh.md"。"""


def main():
    pending = get_pending()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--list':
            print("待翻译文件:")
            for cat in pending:
                print(f"  - {cat}.zh.md")
            print(f"\n总计：{len(pending)}")
            return
        elif sys.argv[1] == '--next' and len(sys.argv) > 2:
            count = int(sys.argv[2])
            pending = pending[:count]
    
    if not pending:
        print("✅ 所有文件已翻译完成！")
        return
    
    print(f"=== 待翻译文件：{len(pending)} 个 ===\n")
    
    for i, cat in enumerate(pending, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(pending)}] {cat}.md")
        print(f"{'='*60}")
        print(create_prompt(cat))
        print(f"\n--- 任务 {i} 结束 ---")


if __name__ == '__main__':
    main()
