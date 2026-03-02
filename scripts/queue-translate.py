#!/usr/bin/env python3
"""
queue-translate.py - 创建翻译任务队列

为每个文件创建任务描述文件，然后可以使用 sessions_spawn 批量处理。

用法:
    python queue-translate.py --all         # 创建所有翻译任务
    python queue-translate.py --status      # 查看状态
    python queue-translate.py --process     # 处理任务队列
"""

import json
import sys
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(__file__).parent.parent
UPSTREAM_DIR = Path("/Volumes/myDisk/workplace/awesome-openclaw-skills")
SCRIPT_DIR = Path(__file__).parent
TASKS_DIR = SCRIPT_DIR / "tasks"
STATE_FILE = SCRIPT_DIR / "translate-queue-state.json"

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

TRANSLATE_TASK_TEMPLATE = """请翻译此 OpenClaw Skills 分类文件为中文。

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
*翻译时间：{date}*

请读取输入文件，翻译后写入输出文件。完成后回复"✅ 完成：{category}.zh.md"。"""


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"tasks": [], "last_update": None}


def save_state(state):
    state["last_update"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def create_tasks():
    """创建所有翻译任务"""
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    
    state = load_state()
    created = 0
    skipped = 0
    
    print("=== 创建翻译任务 ===\n")
    
    for category in CATEGORIES:
        input_file = UPSTREAM_DIR / "categories" / f"{category}.md"
        output_file = PROJECT_DIR / "categories" / f"{category}.zh.md"
        
        # 检查是否已完成
        if output_file.exists():
            print(f"⏭️  已完成：{category}.zh.md")
            skipped += 1
            continue
        
        # 检查上游文件
        if not input_file.exists():
            print(f"⚠️  上游文件不存在：{category}.md")
            continue
        
        # 创建任务文件
        task_file = TASKS_DIR / f"{category}.json"
        
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        task = {
            "category": category,
            "input_file": str(input_file),
            "output_file": str(output_file),
            "prompt": TRANSLATE_TASK_TEMPLATE.format(
                input_file=str(input_file),
                output_file=str(output_file),
                category=category,
                date=date_str
            ),
            "status": "pending",
            "created": date_str
        }
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 创建任务：{category}.json")
        created += 1
        
        state["tasks"].append(task)
    
    save_state(state)
    
    print(f"\n=== 完成 ===")
    print(f"创建：{created} 个任务")
    print(f"跳过：{skipped} 个（已完成）")
    print(f"任务目录：{TASKS_DIR}")


def show_status():
    """显示翻译状态"""
    print("\n=== 翻译任务状态 ===\n")
    
    completed = 0
    pending = 0
    
    for category in CATEGORIES:
        output_file = PROJECT_DIR / "categories" / f"{category}.zh.md"
        if output_file.exists():
            print(f"✅ {category}.zh.md")
            completed += 1
        else:
            print(f"⏳ {category}.zh.md")
            pending += 1
    
    print(f"\n总计：{len(CATEGORIES)} | 已完成：{completed} | 待翻译：{pending}")
    
    # 显示任务文件
    if TASKS_DIR.exists():
        task_files = list(TASKS_DIR.glob("*.json"))
        print(f"\n任务文件：{len(task_files)} 个")


def print_task_commands():
    """打印用于处理任务的 sessions_spawn 命令"""
    state = load_state()
    
    print("\n=== 处理任务队列 ===\n")
    print("使用以下 sessions_spawn 命令处理每个任务：\n")
    
    for task_file in sorted(TASKS_DIR.glob("*.json")):
        with open(task_file, 'r', encoding='utf-8') as f:
            task = json.load(f)
        
        if task.get("status") == "pending":
            print(f"# {task['category']}")
            print(f"sessions_spawn(task=\"\"\"{task['prompt']}\"\"\")")
            print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == '--all':
        create_tasks()
    elif arg == '--status':
        show_status()
    elif arg == '--process':
        print_task_commands()
    else:
        print(f"未知参数：{arg}")
        print(__doc__)


if __name__ == '__main__':
    main()
