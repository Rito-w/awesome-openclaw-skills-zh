#!/usr/bin/env python3
"""
auto-translate.py - 使用 Claude Code 批量翻译 Markdown 文件

用法:
    python auto-translate.py categories/           # 翻译整个目录
    python auto-translate.py README.md             # 翻译单个文件
    python auto-translate.py --all                 # 翻译所有需要翻译的文件
    python auto-translate.py --status              # 查看翻译状态
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(__file__).parent.parent
UPSTREAM_DIR = Path("/Volumes/myDisk/workplace/awesome-openclaw-skills")
SCRIPT_DIR = Path(__file__).parent
STATE_FILE = SCRIPT_DIR / "translate-state.json"

# 翻译提示词模板
TRANSLATE_PROMPT = """请翻译以下 Markdown 内容为中文。

【翻译规则】
1. 保留所有链接、代码块、图片和 HTML 标签不变
2. 只翻译可见文本（标题、描述、元数据）
3. 保持技能名称和 URL 为英文
4. 保持 Markdown 结构完全不变
5. 只输出翻译后的内容，不要任何解释

【输入】{input_file}
【输出】{output_file}

请读取输入文件，翻译后直接写入输出文件。"""


def load_state():
    """加载翻译状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"translations": [], "last_update": None}


def save_state(state):
    """保存翻译状态"""
    state["last_update"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_files_to_translate(target):
    """获取需要翻译的文件列表"""
    files = []
    target_path = PROJECT_DIR / target
    
    if target_path.is_dir():
        # 目录：获取所有 .md 文件
        for md_file in target_path.glob("*.md"):
            if not md_file.name.endswith('.zh.md'):
                output_name = md_file.stem + '.zh.md'
                output_path = md_file.parent / output_name
                files.append({
                    'input': str(md_file.relative_to(PROJECT_DIR)),
                    'output': str(output_path.relative_to(PROJECT_DIR)),
                    'exists': output_path.exists()
                })
    elif target_path.exists():
        # 单文件
        output_name = target_path.stem + '.zh.md'
        output_path = target_path.parent / output_name
        files.append({
            'input': str(target_path.relative_to(PROJECT_DIR)),
            'output': str(output_path.relative_to(PROJECT_DIR)),
            'exists': output_path.exists()
        })
    else:
        print(f"❌ 文件/目录不存在：{target}")
        sys.exit(1)
    
    return files


def translate_with_claude(input_file, output_file):
    """使用 Claude Code 翻译单个文件"""
    input_path = PROJECT_DIR / input_file
    output_path = PROJECT_DIR / output_file
    
    # 如果输入文件不存在，尝试从上游复制
    if not input_path.exists():
        upstream_file = UPSTREAM_DIR / input_file
        if upstream_file.exists():
            print(f"  📥 从上游复制：{input_file}")
            input_path.parent.mkdir(parents=True, exist_ok=True)
            with open(upstream_file, 'r', encoding='utf-8') as src:
                content = src.read()
            with open(input_path, 'w', encoding='utf-8') as dst:
                dst.write(content)
        else:
            print(f"  ⚠️  文件不存在：{input_file}")
            return False
    
    print(f"  🤖 调用 Claude Code 翻译...")
    
    # 构建提示词
    prompt = TRANSLATE_PROMPT.format(
        input_file=str(input_path),
        output_file=str(output_path)
    )
    
    # 使用 claude 命令执行
    try:
        result = subprocess.run(
            ['claude', prompt],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
            timeout=300  # 5 分钟超时
        )
        
        if result.returncode == 0:
            print(f"  ✅ 翻译完成：{output_file}")
            return True
        else:
            print(f"  ❌ 翻译失败：{result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  ⏱️  超时（>5 分钟）")
        return False
    except Exception as e:
        print(f"  ❌ 错误：{e}")
        return False


def show_status(target=None):
    """显示翻译状态"""
    state = load_state()
    
    if target:
        files = get_files_to_translate(target)
    else:
        # 默认检查 categories 目录
        files = get_files_to_translate('categories')
    
    print("\n=== 翻译状态 ===\n")
    print(f"{'输入文件':<50} {'输出文件':<50} {'状态'}")
    print("-" * 110)
    
    translated = 0
    pending = 0
    
    for file_info in files:
        output_exists = Path(PROJECT_DIR / file_info['output']).exists()
        status = "✅ 已翻译" if output_exists else "⏳ 待翻译"
        if output_exists:
            translated += 1
        else:
            pending += 1
        print(f"{file_info['input']:<50} {file_info['output']:<50} {status}")
    
    print("-" * 110)
    print(f"总计：{len(files)} 文件 | 已翻译：{translated} | 待翻译：{pending}")
    print(f"最后更新：{state.get('last_update', '无')}")
    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    target = sys.argv[1]
    
    # 特殊命令
    if target == '--status':
        show_status()
        return
    elif target == '--all':
        target = 'categories'
    
    # 获取文件列表
    files = get_files_to_translate(target)
    
    if not files:
        print("没有找到需要翻译的文件")
        return
    
    print(f"\n=== 批量翻译 ===")
    print(f"目标：{target}")
    print(f"文件数：{len(files)}\n")
    
    state = load_state()
    success = 0
    failed = 0
    
    for file_info in files:
        # 跳过已翻译的文件
        if Path(PROJECT_DIR / file_info['output']).exists():
            print(f"⏭️  跳过（已存在）：{file_info['output']}")
            success += 1
            continue
        
        print(f"\n[{success + failed + 1}/{len(files)}] {file_info['input']}")
        
        if translate_with_claude(file_info['input'], file_info['output']):
            success += 1
            state["translations"].append({
                'input': file_info['input'],
                'output': file_info['output'],
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            })
        else:
            failed += 1
            state["translations"].append({
                'input': file_info['input'],
                'output': file_info['output'],
                'status': 'failed',
                'timestamp': datetime.now().isoformat()
            })
        
        save_state(state)
    
    print(f"\n=== 翻译完成 ===")
    print(f"成功：{success}/{len(files)}")
    print(f"失败：{failed}/{len(files)}")
    print(f"\n状态已保存到：{STATE_FILE}")


if __name__ == '__main__':
    main()
