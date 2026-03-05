#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译质量检查脚本 v4
智能检查：按技能名匹配而不是按行号匹配
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
    """解析技能行，返回 (技能名，链接，描述) 或 None"""
    line = line.strip()
    if not line.startswith('- ['):
        return None
    
    match = re.match(r'^- \[([^\]]+)\]\(([^)]+)\) - (.*)$', line)
    if match:
        return {
            'name': match.group(1),
            'url': match.group(2),
            'description': match.group(3)
        }
    return None

def extract_skills_from_file(file_path):
    """从文件中提取所有技能，返回字典 {skill_name: {url, description, line_num}}"""
    lines = read_file_lines(file_path)
    skills = {}
    
    for i, line in enumerate(lines):
        skill = parse_skill_line(line)
        if skill:
            skill['line_num'] = i + 1
            skill['raw_line'] = line.rstrip('\n')
            skills[skill['name']] = skill
    
    return skills

def check_translation_quality(zh_file, original_file):
    """检查翻译质量 - 按技能名匹配"""
    issues = []
    
    zh_filename = zh_file.name
    
    # 提取两个文件的技能
    zh_skills = extract_skills_from_file(zh_file)
    original_skills = extract_skills_from_file(original_file)
    
    # 检查点 1: 翻译文件中是否有原文件中没有的技能（多余的技能）
    for skill_name, zh_skill in zh_skills.items():
        if skill_name not in original_skills:
            issues.append({
                'file': f"categories/{zh_filename}",
                'line': zh_skill['line_num'],
                'original': f'技能不存在于原文件',
                'translation': f"技能名：{skill_name}",
                'issue': '翻译文件中有多余的技能（原文件中不存在）',
                'suggestion': '检查是否需要从翻译文件中移除',
                'severity': 'medium',
                'type': 'extra_skill'
            })
    
    # 检查点 2: 原文件中是否有翻译文件中没有的技能（缺失的技能）
    for skill_name, orig_skill in original_skills.items():
        if skill_name not in zh_skills:
            issues.append({
                'file': f"categories/{zh_filename}",
                'line': orig_skill['line_num'],
                'original': f"技能名：{skill_name}",
                'translation': f'技能缺失',
                'issue': '原文件中有此技能，但翻译文件中缺失',
                'suggestion': '需要添加此技能的翻译',
                'severity': 'high',
                'type': 'missing_skill'
            })
    
    # 检查点 3: 对匹配的技能进行详细检查
    for skill_name, orig_skill in original_skills.items():
        if skill_name not in zh_skills:
            continue  # 已在上一步报告
        
        zh_skill = zh_skills[skill_name]
        
        # 检查链接是否正确
        if orig_skill['url'] != zh_skill['url']:
            issues.append({
                'file': f"categories/{zh_filename}",
                'line': zh_skill['line_num'],
                'original': f"链接：{orig_skill['url']}",
                'translation': f"链接：{zh_skill['url']}",
                'issue': '链接被修改',
                'suggestion': f'链接应保持原样：{orig_skill["url"]}',
                'severity': 'high',
                'type': 'url_changed',
                'auto_fixable': True,
                'fix_value': orig_skill['url']
            })
        
        # 检查描述
        orig_desc = orig_skill['description']
        zh_desc = zh_skill['description']
        
        # 检查点 a: 完全未翻译的英文描述
        if is_pure_english(orig_desc) and is_pure_english(zh_desc):
            if is_likely_untranslated(orig_desc, zh_desc):
                issues.append({
                    'file': f"categories/{zh_filename}",
                    'line': zh_skill['line_num'],
                    'original': f"描述：{orig_desc}",
                    'translation': f"描述：{zh_desc}",
                    'issue': '完全未翻译的英文描述',
                    'suggestion': '需要将描述翻译为中文',
                    'severity': 'high',
                    'type': 'untranslated',
                    'auto_fixable': False
                })
        
        # 检查点 b: 检测多语言混杂（原文是英文，但译文包含法语/西班牙语/葡萄牙语等）
        if is_pure_english(orig_desc):
            foreign_lang = detect_foreign_language(zh_desc)
            if foreign_lang:
                issues.append({
                    'file': f"categories/{zh_filename}",
                    'line': zh_skill['line_num'],
                    'original': f"描述：{orig_desc}",
                    'translation': f"描述：{zh_desc}",
                    'issue': f'描述包含非中文内容 ({foreign_lang})',
                    'suggestion': '应该翻译为中文，而不是保留其他语言',
                    'severity': 'high',
                    'type': 'foreign_language',
                    'auto_fixable': False
                })
        
        # 检查点 c: 描述中是否包含明显的机翻痕迹
        # 例如：描述以英文句号结尾但前面是中文
        if contains_chinese(zh_desc) and zh_desc.rstrip().endswith('.'):
            # 中文描述不应该以英文句号结尾
            if not zh_desc.rstrip().endswith('。'):
                issues.append({
                    'file': f"categories/{zh_filename}",
                    'line': zh_skill['line_num'],
                    'original': f"描述：{orig_desc}",
                    'translation': f"描述：{zh_desc}",
                    'issue': '标点符号使用不当（中文描述使用英文句号）',
                    'suggestion': '中文描述应使用中文标点符号',
                    'severity': 'low',
                    'type': 'punctuation',
                    'auto_fixable': False
                })
    
    # 检查非技能内容（标题、统计等）
    zh_lines = read_file_lines(zh_file)
    original_lines = read_file_lines(original_file)
    
    # 检查标题行
    if len(zh_lines) > 0 and len(original_lines) > 0:
        zh_title = zh_lines[0].strip()
        orig_title = original_lines[0].strip()
        
        # 标题应该保持一致（或正确翻译）
        if zh_title.startswith('#') and orig_title.startswith('#'):
            if is_pure_english(orig_title) and is_pure_english(zh_title):
                if orig_title == zh_title:
                    # 标题未翻译
                    issues.append({
                        'file': f"categories/{zh_filename}",
                        'line': 1,
                        'original': orig_title,
                        'translation': zh_title,
                        'issue': '标题未翻译',
                        'suggestion': '标题应该翻译为中文',
                        'severity': 'medium',
                        'type': 'title_untranslated',
                        'auto_fixable': False
                    })
    
    return issues

def contains_chinese(text):
    """检查是否包含中文"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def is_pure_english(text):
    """检查是否主要是纯英文（不包含中文）"""
    if contains_chinese(text):
        return False
    return bool(re.search(r'[a-zA-Z]{3,}', text))

def is_likely_untranslated(original, translation):
    """判断是否可能是未翻译的文本"""
    original_clean = re.sub(r'[^\w\s]', '', original.lower())
    translation_clean = re.sub(r'[^\w\s]', '', translation.lower())
    
    if original_clean == translation_clean:
        return True
    
    original_words = set(original_clean.split())
    translation_words = set(translation_clean.split())
    
    if len(original_words) > 2:
        overlap = len(original_words & translation_words)
        if overlap / len(original_words) > 0.8:
            return True
    
    return False

def detect_foreign_language(text):
    """检测文本中是否包含非中文/英文的外语"""
    # 检测法语
    if re.search(r'[àâçéèêëîïôùûü]', text):
        if re.search(r'\b(le|la|les|de|du|des|et|est|une|un)\b', text, re.IGNORECASE):
            return '法语'
    
    # 检测西班牙语
    if re.search(r'[áéíóúñ¿¡]', text):
        if re.search(r'\b(el|la|los|las|de|del|y|es)\b', text, re.IGNORECASE):
            return '西班牙语'
    
    # 检测葡萄牙语
    if re.search(r'[áàâãéêíóôõúç]', text):
        if re.search(r'\b(o|a|os|as|de|do|da|e|é)\b', text, re.IGNORECASE):
            return '葡萄牙语'
    
    # 检测德语
    if re.search(r'[äöüß]', text):
        if re.search(r'\b(der|die|das|und|ist|ein)\b', text, re.IGNORECASE):
            return '德语'
    
    return None

def generate_report(all_issues):
    """生成报告"""
    report = "# 翻译质量检查报告\n\n"
    report += f"共发现 **{len(all_issues)}** 个问题\n\n"
    
    # 按类型统计
    type_counts = {}
    for issue in all_issues:
        t = issue.get('type', 'unknown')
        type_counts[t] = type_counts.get(t, 0) + 1
    
    report += "## 问题类型统计\n\n"
    type_names = {
        'missing_skill': '缺失的技能',
        'extra_skill': '多余的技能',
        'url_changed': '链接被修改',
        'untranslated': '未翻译的描述',
        'foreign_language': '包含外语',
        'punctuation': '标点符号问题',
        'title_untranslated': '标题未翻译'
    }
    for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        name = type_names.get(t, t)
        report += f"- {name}: {count}\n"
    report += "\n"
    
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
        
        # 按类型分组显示
        issues_by_type = {}
        for issue in file_issues:
            t = issue.get('type', 'unknown')
            if t not in issues_by_type:
                issues_by_type[t] = []
            issues_by_type[t].append(issue)
        
        for issue_type, type_issues in sorted(issues_by_type.items(), key=lambda x: -len(x[1])):
            type_name = type_names.get(issue_type, issue_type)
            report += f"### {type_name} ({len(type_issues)} 个)\n\n"
            
            for issue in type_issues[:20]:  # 限制显示数量
                report += format_issue(issue)
            
            if len(type_issues) > 20:
                report += f"\n_...还有 {len(type_issues) - 20} 个问题_\n\n"
    
    return report

def format_issue(issue):
    """格式化单个问题"""
    output = f"**第 {issue['line']} 行**\n\n"
    output += f"- 原文：`{issue['original'][:80]}`{'...' if len(issue['original']) > 80 else ''}\n"
    output += f"- 译文：`{issue['translation'][:80]}`{'...' if len(issue['translation']) > 80 else ''}\n"
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
    
    # 按类型统计
    type_counts = {}
    for issue in all_issues:
        t = issue.get('type', 'unknown')
        type_counts[t] = type_counts.get(t, 0) + 1
    
    print(f"\n✅ 检查完成")
    print(f"- 检查了 {checked_files} 个文件")
    print(f"- 发现了 {len(all_issues)} 个问题")
    print(f"  - 高优先级：{high_count}")
    print(f"  - 中优先级：{medium_count}")
    print(f"  - 低优先级：{low_count}")
    print(f"- 问题类型:")
    for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  - {t}: {count}")
    print(f"- 详细报告在：docs/translation-issues.md")

if __name__ == "__main__":
    main()
