#!/usr/bin/env python3
"""
auto-dispatch.py - 翻译任务派发助手

由于 sessions_spawn 必须在 OpenClaw 会话内运行，
此脚本生成所有待翻译任务的提示词，方便你复制使用。

用法:
    python3 scripts/auto-dispatch.py --status     # 查看翻译状态
    python3 scripts/auto-dispatch.py --next 3     # 生成接下来 3 个任务的提示词
    python3 scripts/auto-dispatch.py --all        # 生成所有待翻译任务的提示词
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


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"completed": ["git-and-github", "ai-and-llms"]}


def save_state(state):
    state["last_update"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_pending():
    state = load_state()
    completed = set(state.get("completed", []))
    
    pending = []
    for cat in CATEGORIES:
        output_file = PROJECT_DIR / "categories" / f"{cat}.zh.md"
        if cat not in completed or not output_file.exists():
            pending.append(cat)
    
    return pending


def mark_completed(category):
    state = load_state()
    if "completed" not in state:
        state["completed"] = []
    if category not in state["completed"]:
        state["completed"].append(category)
    save_state(state)


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


def show_status():
    state = load_state()
    completed = set(state.get("completed", []))
    
    print("\n=== 翻译状态 ===\n")
    
    done = 0
    pending = 0
    
    for cat in CATEGORIES:
        output_file = PROJECT_DIR / "categories" / f"{cat}.zh.md"
        if cat in completed and output_file.exists():
            print(f"✅ {cat}.zh.md")
            done += 1
        else:
            print(f"⏳ {cat}.zh.md")
            pending += 1
    
    print(f"\n总计：{len(CATEGORIES)} | 已完成：{done} | 待翻译：{pending}")
    print(f"\n💡 使用 `python3 scripts/auto-dispatch.py --next 5` 生成接下来 5 个任务的提示词")


def generate_tasks(limit=None):
    pending = get_pending()
    
    if limit:
        pending = pending[:limit]
    
    if not pending:
        print("✅ 所有文件已翻译完成！")
        return
    
    print(f"\n=== 待翻译任务：{len(pending)} 个 ===")
    print(f"\n💡 使用方法：")
    print(f"1. 复制下面的提示词")
    print(f"2. 在 OpenClaw 会话中运行：sessions_spawn(task=\"\"\"...提示词...\"\"\")")
    print(f"3. 子代理完成后会自动通知你")
    print(f"\n{'='*70}")
    
    for i, cat in enumerate(pending, 1):
        print(f"\n### 任务 {i}/{len(pending)}: {cat}")
        print(f"{'='*70}")
        print(create_prompt(cat))
        print(f"\n--- 任务 {i} 结束 ---\n")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == '--status':
        show_status()
    elif arg == '--next' and len(sys.argv) > 2:
        count = int(sys.argv[2])
        generate_tasks(limit=count)
    elif arg == '--all':
        generate_tasks()
    else:
        print(f"未知参数：{arg}")
        print(__doc__)


if __name__ == '__main__':
    main()
