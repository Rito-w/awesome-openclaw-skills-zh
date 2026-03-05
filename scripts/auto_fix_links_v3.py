#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动修复翻译文件中的链接错误 v3
修复所有剩余的链接问题
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path("/Volumes/myDisk/workplace/awesome-openclaw-skills-zh")
CATEGORIES_DIR = PROJECT_ROOT / "categories"

def fix_all_link_issues(file_path):
    """修复文件中的所有链接问题"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixed_count = 0
    fixes_applied = []
    
    # 模式 1: SKILL.mdmd -> SKILL.md
    pattern1 = r'SKILL\.mdmd'
    matches = re.findall(pattern1, content)
    for match in matches:
        correct = 'SKILL.md'
        content = content.replace(match, correct)
        fixed_count += 1
        fixes_applied.append(f"{match} → {correct}")
    
    # 模式 2: SKILL.mdtor-nick-skILL.md -> SKILL.md (通用模式：SKILL.mdXXXskILL.md)
    pattern2 = r'SKILL\.md[a-z]+skILL\.md'
    matches = re.findall(pattern2, content, re.IGNORECASE)
    for match in matches:
        correct = 'SKILL.md'
        content = content.replace(match, correct)
        fixed_count += 1
        fixes_applied.append(f"{match} → {correct}")
    
    # 模式 3: SKILL.mdXXX/SKILL.md -> SKILL.md
    pattern3 = r'SKILL\.md[a-z0-9_-]+/SKILL\.md'
    matches = re.findall(pattern3, content)
    for match in matches:
        correct = 'SKILL.md'
        content = content.replace(match, correct)
        fixed_count += 1
        fixes_applied.append(f"{match} → {correct}")
    
    # 模式 4: SKILL.mdSKILL.md -> SKILL.md
    pattern4 = r'SKILL\.mdSKILL\.md'
    matches = re.findall(pattern4, content)
    for match in matches:
        correct = 'SKILL.md'
        content = content.replace(match, correct)
        fixed_count += 1
        fixes_applied.append(f"{match} → {correct}")
    
    # 模式 5: SKILL.md/SKILL.md -> SKILL.md
    pattern5 = r'SKILL\.md/SKILL\.md'
    matches = re.findall(pattern5, content)
    for match in matches:
        correct = 'SKILL.md'
        content = content.replace(match, correct)
        fixed_count += 1
        fixes_applied.append(f"{match} → {correct}")
    
    # 模式 6: /tree/tree/main -> /tree/main
    pattern6 = r'/tree/tree/main'
    matches = re.findall(pattern6, content)
    for match in matches:
        correct = '/tree/main'
        content = content.replace(match, correct)
        fixed_count += 1
        fixes_applied.append(f"{match} → {correct}")
    
    # 模式 7: /sskills/ -> /skills/
    pattern7 = r'/sskills/'
    matches = re.findall(pattern7, content)
    for match in matches:
        correct = '/skills/'
        content = content.replace(match, correct)
        fixed_count += 1
        fixes_applied.append(f"{match} → {correct}")
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return fixed_count, fixes_applied

def main():
    print("开始自动修复所有链接错误 v3...\n")
    
    # 检查所有 .zh.md 文件
    zh_files = sorted(CATEGORIES_DIR.glob("*.zh.md"))
    
    total_fixed = 0
    all_fixes = []
    
    for zh_file in zh_files:
        fixed, fixes = fix_all_link_issues(zh_file)
        if fixed > 0:
            total_fixed += fixed
            all_fixes.append((zh_file.name, fixes))
            print(f"✓ {zh_file.name}: 修复 {fixed} 个链接")
            for fix in fixes:
                print(f"    {fix}")
    
    if total_fixed == 0:
        print("无需修复")
    
    print(f"\n✅ 完成！共修复 {total_fixed} 个链接")

if __name__ == "__main__":
    main()
