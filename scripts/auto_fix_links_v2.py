#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动修复翻译文件中的链接错误 v2
修复更复杂的链接重复问题
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path("/Volumes/myDisk/workplace/awesome-openclaw-skills-zh")
CATEGORIES_DIR = PROJECT_ROOT / "categories"

def fix_duplicate_links(file_path):
    """修复文件中的重复链接问题"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixed_count = 0
    
    # 模式 1: SKILL.mdXXX/SKILL.md -> SKILL.md (如 SKILL.mdfashion-design/SKILL.md)
    pattern1 = r'SKILL\.md[a-z0-9_-]+/SKILL\.md'
    matches = re.findall(pattern1, content)
    for match in matches:
        correct = 'SKILL.md'
        content = content.replace(match, correct)
        fixed_count += 1
        print(f"  ✓ 修复：{match} → {correct}")
    
    # 模式 2: SKILL.mdSKILL.md -> SKILL.md
    pattern2 = r'SKILL\.mdSKILL\.md'
    matches = re.findall(pattern2, content)
    for match in matches:
        correct = 'SKILL.md'
        content = content.replace(match, correct)
        fixed_count += 1
        print(f"  ✓ 修复：{match} → {correct}")
    
    # 模式 3: SKILL.md/SKILL.md -> SKILL.md
    pattern3 = r'SKILL\.md/SKILL\.md'
    matches = re.findall(pattern3, content)
    for match in matches:
        correct = 'SKILL.md'
        content = content.replace(match, correct)
        fixed_count += 1
        print(f"  ✓ 修复：{match} → {correct}")
    
    # 模式 4: /tree/tree/main -> /tree/main
    pattern4 = r'/tree/tree/main'
    matches = re.findall(pattern4, content)
    for match in matches:
        correct = '/tree/main'
        content = content.replace(match, correct)
        fixed_count += 1
        print(f"  ✓ 修复：{match} → {correct}")
    
    # 模式 5: /sskills/ -> /skills/
    pattern5 = r'/sskills/'
    matches = re.findall(pattern5, content)
    for match in matches:
        correct = '/skills/'
        content = content.replace(match, correct)
        fixed_count += 1
        print(f"  ✓ 修复：{match} → {correct}")
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return fixed_count

def main():
    print("开始自动修复链接错误 v2...\n")
    
    # 需要检查的文件
    files_to_check = [
        "categories/coding-agents-and-ides.zh.md",
        "categories/productivity-and-tasks.zh.md",
        "categories/browser-and-automation.zh.md",
        "categories/transportation.zh.md"
    ]
    
    total_fixed = 0
    
    for file_rel_path in files_to_check:
        file_path = PROJECT_ROOT / file_rel_path
        if not file_path.exists():
            print(f"⚠️  文件不存在：{file_rel_path}")
            continue
        
        print(f"检查：{file_rel_path}")
        fixed = fix_duplicate_links(file_path)
        if fixed > 0:
            total_fixed += fixed
            print(f"  已修复 {fixed} 个链接\n")
        else:
            print(f"  无需修复\n")
    
    print(f"✅ 完成！共修复 {total_fixed} 个链接")

if __name__ == "__main__":
    main()
