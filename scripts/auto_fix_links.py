#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动修复翻译文件中的链接错误
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path("/Volumes/myDisk/workplace/awesome-openclaw-skills-zh")
CATEGORIES_DIR = PROJECT_ROOT / "categories"

# 从报告中提取的链接修复映射
LINK_FIXES = {
    # browser-and-automation.zh.md
    "categories/browser-and-automation.zh.md": {
        "https://github.com/openclaw/skills/tree/main/skills/fabriziogianni7/pond3r-skll/SKILL.md": 
        "https://github.com/openclaw/skills/tree/main/skills/fabriziogianni7/pond3r-skill/SKILL.md"
    },
    # coding-agents-and-ides.zh.md
    "categories/coding-agents-and-ides.zh.md": {
        "https://github.com/openclaw/sskills/tree/main/skills/pauldelavallaz/morpheus-": 
        "https://github.com/openclaw/skills/tree/main/skills/pauldelavallaz/morpheus-fashion-design/SKILL.md",
        "https://github.com/openclaw/skills/tree/main/skills/holl4landtv/tiktok-video-": 
        "https://github.com/openclaw/skills/tree/main/skills/holl4ndtv/tiktok-video-analyzer/SKILL.md"
    },
    # productivity-and-tasks.zh.md
    "categories/productivity-and-tasks.zh.md": {
        "https://github.com/openclaw/skills/tree/main/skills/clarazoe/close-loop/SKILL.md": 
        "https://github.com/openclaw/skills/tree/main/skills/clarezoe/close-loop/SKILL.md",
        "https://github.com/openclaw/skills/tree/main/skills/cluelessboy/ds160-autofil": 
        "https://github.com/openclaw/skills/tree/main/skills/clulessboy/ds160-autofill/SKILL.md",
        "https://github.com/openclaw/skills/tree/main/skills/quarantine/effortlist-ai/": 
        "https://github.com/openclaw/skills/tree/main/skills/quarantiine/effortlist-ai/SKILL.md",
        "https://github.com/openclaw/skills/tree/main/skills/jovansapioneer/network-ai": 
        "https://github.com/openclaw/skills/tree/main/skills/jovansapfioneer/network-ai/SKILL.md",
        "https://github.com/openclaw/skills/tree/main/skills/sarthakb7/sokosumi/SKILL.": 
        "https://github.com/openclaw/skills/tree/main/skills/sarthib7/sokosumi/SKILL.md",
        "https://github.com/openclaw/skills/tree/tree/main/skills/suky57/zulip/SKILL.md": 
        "https://github.com/openclaw/skills/tree/main/skills/suky57/zulip/SKILL.md"
    },
    # transportation.zh.md
    "categories/transportation.zh.md": {
        "https://github.com/openclaw/skills/tree/main/skills/yoavfael/dropshipping-men": 
        "https://github.com/openclaw/skills/tree/main/skills/yoavfael/dropshipping-mentor-nick-skill/SKILL.md"
    }
}

def fix_links_in_file(file_path, fixes):
    """修复文件中的链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixed_count = 0
    for old_link, new_link in fixes.items():
        if old_link in content:
            content = content.replace(old_link, new_link)
            fixed_count += 1
            print(f"  ✓ 修复链接：{old_link[:60]}... → {new_link[:60]}...")
    
    if fixed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return fixed_count

def main():
    print("开始自动修复链接错误...\n")
    
    total_fixed = 0
    
    for file_rel_path, fixes in LINK_FIXES.items():
        file_path = PROJECT_ROOT / file_rel_path
        if not file_path.exists():
            print(f"⚠️  文件不存在：{file_rel_path}")
            continue
        
        print(f"修复：{file_rel_path}")
        fixed = fix_links_in_file(file_path, fixes)
        total_fixed += fixed
        print(f"  已修复 {fixed} 个链接\n")
    
    print(f"✅ 完成！共修复 {total_fixed} 个链接")

if __name__ == "__main__":
    main()
