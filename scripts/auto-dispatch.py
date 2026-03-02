#!/usr/bin/env python3
"""
auto-dispatch.py - 自动派发翻译任务

使用 sessions_spawn 批量派发翻译任务给子代理。
支持：
- 批量派发所有待翻译文件
- 并发控制（避免同时运行太多任务）
- 任务状态追踪
- 断点续传

用法:
    python auto-dispatch.py --all           # 派发所有待翻译任务
    python auto-dispatch.py --status        # 查看翻译状态
    python auto-dispatch.py --dispatch 5    # 派发 5 个任务
    python auto-dispatch.py --sync          # 同步上游更新并派发新任务
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict

PROJECT_DIR = Path(__file__).parent.parent
UPSTREAM_DIR = Path("/Volumes/myDisk/workplace/awesome-openclaw-skills")
SCRIPT_DIR = Path(__file__).parent
TASKS_DIR = SCRIPT_DIR / "tasks"
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

# 已完成的分类（硬编码，避免重复）
COMPLETED = {"git-and-github", "ai-and-llms"}


def load_state():
    """加载状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"dispatched": [], "completed": list(COMPLETED), "last_update": None}


def save_state(state):
    """保存状态"""
    state["last_update"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_pending_categories(state) -> List[str]:
    """获取待翻译的分类列表"""
    pending = []
    for cat in CATEGORIES:
        output_file = PROJECT_DIR / "categories" / f"{cat}.zh.md"
        if cat in state.get("completed", []) and output_file.exists():
            continue
        if cat in COMPLETED and output_file.exists():
            continue
        pending.append(cat)
    return pending


def create_translation_prompt(category: str) -> str:
    """创建翻译提示词"""
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


def dispatch_task(category: str) -> Dict:
    """派发单个翻译任务"""
    prompt = create_translation_prompt(category)
    
    print(f"  🚀 派发任务：{category}")
    
    # 使用 sessions_spawn 派发
    result = subprocess.run(
        ['openclaw', 'sessions_spawn', '--mode', 'run', '--label', f'translate-{category}', '--task', prompt],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_DIR)
    )
    
    if result.returncode == 0:
        # 解析输出获取 session key
        try:
            output = json.loads(result.stdout)
            session_key = output.get('childSessionKey', 'unknown')
            return {
                'status': 'dispatched',
                'session_key': session_key,
                'category': category,
                'timestamp': datetime.now().isoformat()
            }
        except:
            return {
                'status': 'dispatched',
                'session_key': 'unknown',
                'category': category,
                'timestamp': datetime.now().isoformat()
            }
    else:
        print(f"    ❌ 失败：{result.stderr[:100]}")
        return {
            'status': 'failed',
            'error': result.stderr[:200],
            'category': category,
            'timestamp': datetime.now().isoformat()
        }


def dispatch_all(limit: int = None):
    """批量派发翻译任务"""
    state = load_state()
    pending = get_pending_categories(state)
    
    if not pending:
        print("✅ 所有分类已翻译完成！")
        return
    
    if limit:
        pending = pending[:limit]
        print(f"=== 派发 {len(pending)} 个翻译任务 ===\n")
    else:
        print(f"=== 派发所有 {len(pending)} 个待翻译任务 ===\n")
    
    dispatched = 0
    failed = 0
    
    for category in pending:
        result = dispatch_task(category)
        
        if result['status'] == 'dispatched':
            state["dispatched"].append(result)
            dispatched += 1
            print(f"    ✅ {category} -> {result['session_key']}")
        else:
            failed += 1
        
        # 保存状态
        save_state(state)
        
        # 小延迟避免过快
        import time
        time.sleep(1)
    
    print(f"\n=== 派发完成 ===")
    print(f"成功：{dispatched}")
    print(f"失败：{failed}")
    print(f"\n💡 任务正在后台运行，完成后会自动通知")


def show_status():
    """显示翻译状态"""
    state = load_state()
    
    print("\n=== 翻译状态 ===\n")
    
    completed = 0
    pending = 0
    in_progress = 0
    
    for cat in CATEGORIES:
        output_file = PROJECT_DIR / "categories" / f"{cat}.zh.md"
        if output_file.exists():
            print(f"✅ {cat}.zh.md")
            completed += 1
        elif cat in [d['category'] for d in state.get('dispatched', [])]:
            print(f"🔄 {cat}.zh.md (翻译中)")
            in_progress += 1
        else:
            print(f"⏳ {cat}.zh.md")
            pending += 1
    
    print(f"\n总计：{len(CATEGORIES)} | 已完成：{completed} | 翻译中：{in_progress} | 待翻译：{pending}")
    print(f"最后更新：{state.get('last_update', '无')}")


def sync_from_upstream():
    """同步上游更新并派发新任务"""
    print("=== 同步上游更新 ===\n")
    
    # 获取上游变更
    result = subprocess.run(
        ['git', 'diff', '--name-only', 'origin/main', 'main'],
        cwd=str(UPSTREAM_DIR),
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("⚠️  无法获取上游变更，尝试直接拉取...")
        subprocess.run(['git', 'fetch', 'origin', 'main'], cwd=str(UPSTREAM_DIR))
    
    changed_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    # 筛选分类文件
    categories_to_update = []
    for f in changed_files:
        if f.startswith('categories/') and f.endswith('.md'):
            cat_name = f.split('/')[-1].replace('.md', '')
            if not cat_name.endswith('.zh'):
                categories_to_update.append(cat_name)
    
    if not categories_to_update:
        print("✅ 上游无更新")
        return
    
    print(f"📝 发现 {len(categories_to_update)} 个分类有更新:")
    for cat in categories_to_update:
        print(f"  - {cat}.md")
    
    # 重新翻译这些分类
    print(f"\n🔄 重新翻译这些分类...")
    
    state = load_state()
    for cat in categories_to_update:
        # 删除旧版本
        output_file = PROJECT_DIR / "categories" / f"{cat}.zh.md"
        if output_file.exists():
            output_file.unlink()
            print(f"  🗑️  删除旧版：{cat}.zh.md")
        
        # 从 completed 中移除
        if cat in state.get("completed", []):
            state["completed"].remove(cat)
        
        # 派发新任务
        dispatch_task(cat)
        save_state(state)
    
    print(f"\n✅ 同步完成，已派发重新翻译任务")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == '--status':
        show_status()
    elif arg == '--all':
        dispatch_all()
    elif arg == '--sync':
        sync_from_upstream()
        dispatch_all()
    elif arg.isdigit():
        dispatch_all(limit=int(arg))
    else:
        print(f"未知参数：{arg}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
