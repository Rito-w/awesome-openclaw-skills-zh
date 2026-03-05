#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译质量检查脚本 v2
更智能地检查 categories/ 目录下所有 .zh.md 文件的翻译质量
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

def parse_skill_line(line):
    """解析技能行，返回 (技能名，链接，描述)"""
    # 格式：- [skill-name](url) - description
    match = re.match(r'^- \[([^\]]+)\]\(([^)]+)\) - (.*)$', line.strip())
    if match:
        return match.group(1), match.group(2), match.group(3)
    return None, None, line.strip()

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
        zh_line = zh_lines[i].rstrip('\n')
        original_line = original_lines[i].rstrip('\n') if i < len(original_lines) else ""
        
        line_num = i + 1
        
        # 跳过空行
        if not zh_line.strip() and not original_line.strip():
            continue
        
        # 检查技能行格式：- [name](url) - description
        if original_line.strip().startswith('- [') and '](http' in original_line:
            orig_name, orig_url, orig_desc = parse_skill_line(original_line)
            zh_name, zh_url, zh_desc = parse_skill_line(zh_line)
            
            # 检查点 d: 技能名称是否正确保留英文
            if orig_name and zh_name and orig_name != zh_name:
                issues.append({
                    'file': f"categories/{zh_filename}",
                    'line': line_num,
                    'original': f"技能名：{orig_name}",
                    'translation': f"技能名：{zh_name}",
                    'issue': '技能名被错误翻译',
                    'suggestion': f'技能名应保持英文：{orig_name}',
                    'severity': 'high'
                })
            
            # 检查点 e: 链接是否正确保留
            if orig_url and zh_url and orig_url != zh_url:
                issues.append({
                    'file': f"categories/{zh_filename}",
                    'line': line_num,
                    'original': f"链接：{orig_url}",
                    'translation': f"链接：{zh_url}",
                    'issue': '链接被修改',
                    'suggestion': f'链接应保持原样：{orig_url}',
                    'severity': 'high'
                })
            
            # 检查点 a: 描述部分是否有未翻译的英文
            if orig_desc and zh_desc:
                # 如果原文描述是英文，检查译文描述
                if is_english_text(orig_desc) and is_english_text(zh_desc):
                    # 检查是否整句未翻译（排除技能名重复的情况）
                    if is_likely_untranslated(orig_desc, zh_desc):
                        issues.append({
                            'file': f"categories/{zh_filename}",
                            'line': line_num,
                            'original': f"描述：{orig_desc}",
                            'translation': f"描述：{zh_desc}",
                            'issue': '未翻译的英文描述',
                            'suggestion': '需要将描述翻译为中文',
                            'severity': 'high'
                        })
                
                # 检查点 b: 机翻痕迹 - 检查多语言混杂
                # 如果原文是英文，但译文包含其他语言（法语、西班牙语等）
                if is_english_text(orig_desc):
                    if detect_foreign_language(zh_desc):
                        lang = detect_foreign_language(zh_desc)
                        issues.append({
                            'file': f"categories/{zh_filename}",
                            'line': line_num,
                            'original': f"描述：{orig_desc}",
                            'translation': f"描述：{zh_desc}",
                            'issue': f'描述包含非中文内容 ({lang})',
                            'suggestion': '应该翻译为中文，而不是保留其他语言',
                            'severity': 'medium'
                        })
            
            # 检查点 c: 格式错乱
            if not zh_line.strip().startswith('- ['):
                issues.append({
                    'file': f"categories/{zh_filename}",
                    'line': line_num,
                    'original': original_line[:80],
                    'translation': zh_line[:80],
                    'issue': '格式错乱 - 列表项格式不正确',
                    'suggestion': '保持 - [name](link) - description 格式',
                    'severity': 'medium'
                })
        
        # 检查非技能行的未翻译内容
        elif original_line.strip() and not original_line.strip().startswith('#') and not original_line.strip().startswith('['):
            if is_english_text(original_line) and is_english_text(zh_line):
                if is_likely_untranslated(original_line, zh_line):
                    issues.append({
                        'file': f"categories/{zh_filename}",
                        'line': line_num,
                        'original': original_line[:80],
                        'translation': zh_line[:80],
                        'issue': '未翻译的英文内容',
                        'suggestion': '需要翻译为中文',
                        'severity': 'medium'
                    })
        
        # 检查点 f: 特殊符号（希腊字母等）是否正确保留
        special_chars_pattern = r'[α-ωΑ-Ω∑∏∫∂∇∈∉∋∌⊂⊃⊄⊅∩∪∅∞≈≠≡≤≥⊕⊗√∧∨¬⇒⇔∀∃]'
        if re.search(special_chars_pattern, original_line):
            if not re.search(special_chars_pattern, zh_line):
                issues.append({
                    'file': f"categories/{zh_filename}",
                    'line': line_num,
                    'original': original_line[:80],
                    'translation': zh_line[:80],
                    'issue': '特殊符号丢失',
                    'suggestion': '保留原文中的特殊符号',
                    'severity': 'low'
                })
    
    return issues

def contains_chinese(text):
    """检查是否包含中文"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def is_english_text(text):
    """检查是否主要是英文文本"""
    # 移除链接和 markdown 格式
    clean_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', '', text)
    clean_text = re.sub(r'[`\*\-_#]', '', clean_text)
    # 检查是否包含连续的英文字母
    english_words = re.findall(r'\b[a-zA-Z]{3,}\b', clean_text)
    return len(english_words) >= 2

def is_likely_untranslated(original, translation):
    """判断是否可能是未翻译的文本"""
    # 如果原文和译文非常相似，可能是未翻译
    original_clean = re.sub(r'[^\w\s]', '', original.lower())
    translation_clean = re.sub(r'[^\w\s]', '', translation.lower())
    
    # 如果英文单词大部分相同，可能是未翻译
    original_words = set(original_clean.split())
    translation_words = set(translation_clean.split())
    
    if len(original_words) > 2:
        overlap = len(original_words & translation_words)
        if overlap / len(original_words) > 0.5:
            return True
    
    return False

def detect_foreign_language(text):
    """检测文本中是否包含非中文/英文的外语"""
    # 检测法语特征
    if re.search(r'\b(le|la|les|de|du|des|et|est|une|un|pour|dans|avec|sur|à|être|avoir)\b', text, re.IGNORECASE):
        if re.search(r'[àâçéèêëîïôùûü]', text):
            return '法语'
    
    # 检测西班牙语特征
    if re.search(r'\b(el|la|los|las|de|del|y|es|una|uno|para|en|con|ser|estar)\b', text, re.IGNORECASE):
        if re.search(r'[áéíóúñ¿¡]', text):
            return '西班牙语'
    
    # 检测葡萄牙语特征
    if re.search(r'\b(o|a|os|as|de|do|da|dos|das|e|é|uma|um|para|em|com|ser|estar)\b', text, re.IGNORECASE):
        if re.search(r'[áàâãéêíóôõúç]', text):
            return '葡萄牙语'
    
    # 检测德语特征
    if re.search(r'\b(der|die|das|und|ist|ein|eine|für|mit|von|zu|das|ist)\b', text, re.IGNORECASE):
        if re.search(r'[äöüß]', text):
            return '德语'
    
    return None

def generate_report(all_issues):
    """生成报告"""
    report = "# 翻译质量检查报告\n\n"
    report += f"共发现 **{len(all_issues)}** 个问题\n\n"
    
    # 按严重程度统计
    high_count = sum(1 for i in all_issues if i.get('severity') == 'high')
    medium_count = sum(1 for i in all_issues if i.get('severity') == 'medium')
    low_count = sum(1 for i in all_issues if i.get('severity') == 'low')
    
    report += f"- 🔴 高优先级：{high_count}\n"
    report += f"- 🟡 中优先级：{medium_count}\n"
    report += f"- 🟢 低优先级：{low_count}\n\n"
    
    # 按文件分组
    issues_by_file = {}
    for issue in all_issues:
        file_key = issue['file']
        if file_key not in issues_by_file:
            issues_by_file[file_key] = []
        issues_by_file[file_key].append(issue)
    
    for file_path, file_issues in sorted(issues_by_file.items()):
        high_in_file = sum(1 for i in file_issues if i.get('severity') == 'high')
        report += f"\n## {file_path} ({len(file_issues)} 个问题，{high_in_file} 个高优先级)\n\n"
        
        # 先显示高优先级问题
        high_issues = [i for i in file_issues if i.get('severity') == 'high']
        if high_issues:
            report += "### 🔴 高优先级问题\n\n"
            for issue in high_issues[:20]:  # 限制显示数量
                report += format_issue(issue)
            if len(high_issues) > 20:
                report += f"\n_...还有 {len(high_issues) - 20} 个高优先级问题_\n\n"
        
        # 显示中优先级问题
        medium_issues = [i for i in file_issues if i.get('severity') == 'medium']
        if medium_issues:
            report += "### 🟡 中优先级问题\n\n"
            for issue in medium_issues[:10]:
                report += format_issue(issue)
            if len(medium_issues) > 10:
                report += f"\n_...还有 {len(medium_issues) - 10} 个中优先级问题_\n\n"
        
        # 显示低优先级问题
        low_issues = [i for i in file_issues if i.get('severity') == 'low']
        if low_issues:
            report += "### 🟢 低优先级问题\n\n"
            for issue in low_issues[:5]:
                report += format_issue(issue)
            if len(low_issues) > 5:
                report += f"\n_...还有 {len(low_issues) - 5} 个低优先级问题_\n\n"
    
    return report

def format_issue(issue):
    """格式化单个问题"""
    output = f"**第 {issue['line']} 行**\n\n"
    output += f"- 原文：`{issue['original']}`\n"
    output += f"- 译文：`{issue['translation']}`\n"
    output += f"- 问题：{issue['issue']}\n"
    output += f"- 建议：{issue['suggestion']}\n\n"
    return output

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
    
    # 统计
    high_count = sum(1 for i in all_issues if i.get('severity') == 'high')
    medium_count = sum(1 for i in all_issues if i.get('severity') == 'medium')
    low_count = sum(1 for i in all_issues if i.get('severity') == 'low')
    
    print(f"\n✅ 检查完成")
    print(f"- 检查了 {checked_files} 个文件")
    print(f"- 发现了 {len(all_issues)} 个问题")
    print(f"  - 高优先级：{high_count}")
    print(f"  - 中优先级：{medium_count}")
    print(f"  - 低优先级：{low_count}")
    print(f"- 详细报告在：docs/translation-issues.md")

if __name__ == "__main__":
    main()
