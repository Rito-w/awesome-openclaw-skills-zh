#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译质量检查脚本
检查 categories/ 目录下所有 .zh.md 文件的翻译质量
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path("/Volumes/myDisk/workplace/awesome-openclaw-skills-zh")
CATEGORIES_DIR = PROJECT_ROOT / "categories"
OUTPUT_FILE = PROJECT_ROOT / "docs" / "translation-issues.md"

def find_zh_files():
    """找到所有 .zh.md 文件"""
    zh_files = sorted(CATEGORIES_DIR.glob("*.zh.md"))
    return zh_files

def get_original_file(zh_file):
    """获取对应的英文原文件"""
    original_name = zh_file.name.replace(".zh.md", ".md")
    original_file = CATEGORIES_DIR / original_name
    return original_file if original_file.exists() else None

def read_file_lines(file_path):
    """读取文件的所有行"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def check_translation_quality(zh_file, original_file):
    """检查翻译质量"""
    issues = []
    
    zh_lines = read_file_lines(zh_file)
    original_lines = read_file_lines(original_file)
    
    zh_filename = zh_file.name
    original_filename = original_file.name
    
    # 逐行对比
    max_lines = max(len(zh_lines), len(original_lines))
    
    for i in range(max_lines):
        zh_line = zh_lines[i].strip() if i < len(zh_lines) else ""
        original_line = original_lines[i].strip() if i < len(original_lines) else ""
        
        line_num = i + 1
        
        # 跳过空行和纯标题行
        if not zh_line or not original_line:
            continue
        
        # 跳过完全相同的行（如链接、标题等）
        if zh_line == original_line:
            continue
        
        # 检查点 a: 未翻译的英文描述
        # 如果原文是英文，译文也包含大量英文（排除技能名、链接等）
        if contains_english_text(original_line) and contains_english_text(zh_line):
            # 检查是否整句未翻译
            if is_likely_untranslated(original_line, zh_line):
                issues.append({
                    'file': f"categories/{zh_filename}",
                    'line': line_num,
                    'original': original_line,
                    'translation': zh_line,
                    'issue': '未翻译的英文描述',
                    'suggestion': '需要翻译为中文'
                })
        
        # 检查点 b: 机翻痕迹
        # 检查常见的机翻问题
        machine_translation_patterns = [
            (r'的 API', 'API'),  # 过度使用"的"
            (r'进行', ''),  # 过度使用"进行"
            (r'一个', ''),  # 过度使用"一个"
        ]
        
        # 检查点 c: 格式错乱
        # 检查 markdown 格式是否正确
        if original_line.startswith('- [') and not zh_line.startswith('- ['):
            issues.append({
                'file': f"categories/{zh_filename}",
                'line': line_num,
                'original': original_line,
                'translation': zh_line,
                'issue': '格式错乱 - 列表项格式不正确',
                'suggestion': '保持 - [name](link) 格式'
            })
        
        # 检查点 d: 技能名称是否正确保留英文
        # 提取技能名称（方括号内的内容）
        zh_skill_match = re.search(r'\[([^\]]+)\]', zh_line)
        original_skill_match = re.search(r'\[([^\]]+)\]', original_line)
        
        if original_skill_match and zh_skill_match:
            original_skill = original_skill_match.group(1)
            zh_skill = zh_skill_match.group(1)
            
            # 技能名应该保持一致
            if original_skill != zh_skill:
                # 检查是否是翻译了技能名（不应该）
                if contains_chinese(zh_skill) and not contains_chinese(original_skill):
                    issues.append({
                        'file': f"categories/{zh_filename}",
                        'line': line_num,
                        'original': f"技能名：{original_skill}",
                        'translation': f"技能名：{zh_skill}",
                        'issue': '技能名被错误翻译',
                        'suggestion': f'技能名应保持英文：{original_skill}'
                    })
        
        # 检查点 e: 链接是否正确保留
        zh_link_match = re.search(r'\]\(([^)]+)\)', zh_line)
        original_link_match = re.search(r'\]\(([^)]+)\)', original_line)
        
        if original_link_match and zh_link_match:
            original_link = original_link_match.group(1)
            zh_link = zh_link_match.group(1)
            
            if original_link != zh_link:
                issues.append({
                    'file': f"categories/{zh_filename}",
                    'line': line_num,
                    'original': f"链接：{original_link}",
                    'translation': f"链接：{zh_link}",
                    'issue': '链接被修改',
                    'suggestion': f'链接应保持原样：{original_link}'
                })
        
        # 检查点 f: 特殊符号（希腊字母等）是否正确保留
        # 检查数学符号、希腊字母等
        special_chars_pattern = r'[α-ωΑ-Ω∑∏∫∂∇∈∉∋∌⊂⊃⊄⊅∩∪∅∞≈≠≡≤≥⊕⊗√∧∨¬⇒⇔∀∃]'
        if re.search(special_chars_pattern, original_line):
            if not re.search(special_chars_pattern, zh_line):
                issues.append({
                    'file': f"categories/{zh_filename}",
                    'line': line_num,
                    'original': original_line,
                    'translation': zh_line,
                    'issue': '特殊符号丢失',
                    'suggestion': '保留原文中的特殊符号'
                })
    
    return issues

def contains_chinese(text):
    """检查是否包含中文"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def contains_english_text(text):
    """检查是否包含英文文本（排除纯链接、技能名等）"""
    # 移除链接和 markdown 格式
    clean_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', '', text)
    clean_text = re.sub(r'[`\*\-_#]', '', clean_text)
    # 检查是否包含连续的英文字母
    return bool(re.search(r'[a-zA-Z]{3,}', clean_text))

def is_likely_untranslated(original, translation):
    """判断是否可能是未翻译的文本"""
    # 如果原文和译文非常相似，可能是未翻译
    original_words = set(re.findall(r'[a-zA-Z]+', original.lower()))
    translation_words = set(re.findall(r'[a-zA-Z]+', translation.lower()))
    
    # 如果英文单词大部分相同，可能是未翻译
    if len(original_words) > 3:
        overlap = len(original_words & translation_words)
        if overlap / len(original_words) > 0.7:
            return True
    
    return False

def generate_report(all_issues):
    """生成报告"""
    report = "# 翻译质量检查报告\n\n"
    report += f"生成时间：{Path(PROJECT_ROOT).stat().st_mtime}\n\n"
    report += f"共发现 **{len(all_issues)}** 个问题\n\n"
    
    # 按文件分组
    issues_by_file = {}
    for issue in all_issues:
        file_key = issue['file']
        if file_key not in issues_by_file:
            issues_by_file[file_key] = []
        issues_by_file[file_key].append(issue)
    
    for file_path, file_issues in sorted(issues_by_file.items()):
        report += f"\n## {file_path}\n\n"
        report += f"共 {len(file_issues)} 个问题\n\n"
        
        for issue in file_issues:
            report += f"### 问题行号：第 {issue['line']} 行\n\n"
            report += f"**原文：** `{issue['original'][:100]}`{'...' if len(issue['original']) > 100 else ''}\n\n"
            report += f"**译文：** `{issue['translation'][:100]}`{'...' if len(issue['translation']) > 100 else ''}\n\n"
            report += f"**问题描述：** {issue['issue']}\n\n"
            report += f"**建议修复：** {issue['suggestion']}\n\n"
            report += "---\n\n"
    
    return report

def main():
    print("开始检查翻译质量...")
    
    zh_files = find_zh_files()
    print(f"找到 {len(zh_files)} 个翻译文件")
    
    all_issues = []
    checked_files = 0
    
    for zh_file in zh_files:
        original_file = get_original_file(zh_file)
        if original_file is None:
            print(f"⚠️  未找到原文件：{zh_file.name}")
            continue
        
        print(f"检查：{zh_file.name}")
        issues = check_translation_quality(zh_file, original_file)
        all_issues.extend(issues)
        checked_files += 1
    
    # 生成报告
    report = generate_report(all_issues)
    
    # 确保 docs 目录存在
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入报告
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 检查完成")
    print(f"- 检查了 {checked_files} 个文件")
    print(f"- 发现了 {len(all_issues)} 个问题")
    print(f"- 详细报告在：docs/translation-issues.md")

if __name__ == "__main__":
    main()
