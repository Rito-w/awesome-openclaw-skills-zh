#!/usr/bin/env python3
"""
翻译 awesome-openclaw-skills 的 categories 文件
"""
import os
import re
from pathlib import Path

# 标题翻译映射
TITLE_MAP = {
    "AI and LLMs": "AI 与大语言模型",
    "Apple Apps and Services": "Apple 应用与服务",
    "Browser and Automation": "浏览器与自动化",
    "Calendar and Scheduling": "日历与日程",
    "ClawDBot Tools": "ClawDBot 工具",
    "CLI Utilities": "命令行工具",
    "Coding Agents and IDEs": "编程代理与 IDE",
    "Communication": "通讯",
    "Data and Analytics": "数据与分析",
    "DevOps and Cloud": "DevOps 与云服务",
    "Gaming": "游戏",
    "Git and GitHub": "Git 与 GitHub",
    "Health and Fitness": "健康与健身",
    "Image and Video Generation": "图像与视频生成",
    "iOS and macOS Development": "iOS 与 macOS 开发",
    "Marketing and Sales": "营销与销售",
    "Media and Streaming": "媒体与流媒体",
    "Moltbook": "Moltbook",
    "Notes and PKM": "笔记与知识管理",
    "PDF and Documents": "PDF 与文档",
    "Personal Development": "个人发展",
    "Productivity and Tasks": "生产力与任务",
    "Search and Research": "搜索与研究",
    "Security and Passwords": "安全与密码",
    "Self-Hosted and Automation": "自托管与自动化",
    "Shopping and E-Commerce": "购物与电商",
    "Smart Home and IoT": "智能家居与物联网",
    "Speech and Transcription": "语音与转录",
    "Transportation": "交通出行",
    "Web and Frontend Development": "Web 与前端开发",
}

def translate_file(src_path: Path, dst_path: Path):
    """翻译单个文件"""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    translated_lines = []

    for line in lines:
        # 翻译标题
        if line.startswith('# '):
            title = line[2:]
            translated_title = TITLE_MAP.get(title, title)
            translated_lines.append(f'# {translated_title}')
        # 翻译返回链接
        elif '[← Back to main list]' in line:
            translated_lines.append('[← 返回主列表](../README.md#table-of-contents)')
        # 翻译技能数量
        elif line.startswith('**') and 'skills' in line:
            match = re.match(r'\*\*(\d+) skills?\*\*', line)
            if match:
                count = match.group(1)
                translated_lines.append(f'**{count} 个技能**')
            else:
                translated_lines.append(line)
        # 翻译技能描述
        elif line.startswith('- ['):
            # 保持链接不变，翻译描述
            match = re.match(r'- \[([^\]]+)\]\(([^)]+)\) - (.+)', line)
            if match:
                name, url, desc = match.groups()
                translated_desc = translate_description(desc)
                translated_lines.append(f'- [{name}]({url}) - {translated_desc}')
            else:
                translated_lines.append(line)
        else:
            translated_lines.append(line)

    # 添加翻译信息
    filename = src_path.name
    translated_lines.append('')
    translated_lines.append('---')
    translated_lines.append(f'*翻译自：https://github.com/VoltAgent/awesome-openclaw-skills/blob/main/categories/{filename}*')
    translated_lines.append('*翻译时间：2026-03-12*')

    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(translated_lines))

def translate_description(desc: str) -> str:
    """翻译技能描述（简化版，实际应使用翻译API）"""
    # 常用词翻译
    translations = {
        "Browse": "浏览",
        "boards": "板块",
        "and": "与",
        "extract": "提取",
        "thread": "帖子",
        "discussions": "讨论",
        "When": "当",
        "the": "这个",
        "user": "用户",
        "wants": "想要",
        "to": "去",
        "plan": "规划",
        "Generate": "生成",
        "professional": "专业",
        "advertising": "广告",
        "images": "图片",
        "from": "从",
        "product": "产品",
        "URLs": "URL",
        "Full-stack": "全栈",
        "affiliate": "联盟",
        "marketing": "营销",
        "automation": "自动化",
        "Integrate": "集成",
        "AI-powered": "AI 驱动",
        "Amazon": "亚马逊",
        "recommendations": "推荐",
        "Create": "创建",
        "signup": "注册",
        "lead": "潜在客户",
        "in": "在",
        "system": "系统",
        "using": "使用",
        "public": "公共",
        "HTTP": "HTTP",
        "endpoint": "端点",
        "Find": "查找",
        "suppliers": "供应商",
        "via": "通过",
        "contact": "联系",
        "them": "他们",
        "with": "使用",
        "optimized": "优化的",
        "outreach": "外联",
        "messages": "消息",
        "check": "检查",
        "their": "他们的",
        "replies": "回复",
        "Interact": "交互",
        "REST": "REST",
        "API": "API",
        "people": "人员",
        "org": "组织",
        "enrichment": "丰富",
        "search": "搜索",
        "lists": "列表",
        "Use": "使用",
        "CLI": "CLI",
        "for": "用于",
        "Manage": "管理",
        "projects": "项目",
        "monitor": "监控",
        "your": "你的",
        "brand": "品牌",
        "visibility": "可见性",
    }

    # 简单的词替换翻译
    result = desc
    for en, zh in translations.items():
        result = result.replace(en, zh)

    return result

def main():
    categories_dir = Path('/Volumes/myDisk/workplace/awesome-openclaw-skills-zh/categories')

    # 获取所有英文源文件
    for src_file in categories_dir.glob('*.md'):
        if src_file.name.endswith('.zh.md'):
            continue

        dst_file = categories_dir / f"{src_file.stem}.zh.md"
        print(f"翻译: {src_file.name} -> {dst_file.name}")
        translate_file(src_file, dst_file)

    print("\n翻译完成！")

if __name__ == '__main__':
    main()