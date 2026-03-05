#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译 awesome-openclaw-skills 技能描述
使用简单的翻译映射 + 规则处理
"""

import os
import re

PROJECT_DIR = "/Volumes/myDisk/workplace/awesome-openclaw-skills-zh"
RAW_BASE_URL = "https://raw.githubusercontent.com/VoltAgent/awesome-openclaw-skills/main"

# 常见英文短语翻译映射
TRANSLATION_MAP = {
    # 通用动词
    "Get": "获取",
    "Create": "创建",
    "Generate": "生成",
    "Manage": "管理",
    "Track": "追踪",
    "Monitor": "监控",
    "Analyze": "分析",
    "Build": "构建",
    "Deploy": "部署",
    "Search": "搜索",
    "Query": "查询",
    "Send": "发送",
    "Receive": "接收",
    "Enable": "启用",
    "Automate": "自动化",
    "Transform": "转换",
    "Convert": "转换",
    "Process": "处理",
    "Extract": "提取",
    "Import": "导入",
    "Export": "导出",
    "Update": "更新",
    "Delete": "删除",
    "Check": "检查",
    "Verify": "验证",
    "Test": "测试",
    "Debug": "调试",
    "Optimize": "优化",
    "Configure": "配置",
    "Install": "安装",
    "Setup": "设置",
    "Connect": "连接",
    "Integrate": "集成",
    "Sync": "同步",
    "Backup": "备份",
    "Restore": "恢复",
    
    # 名词
    "agent": "代理",
    "agents": "代理",
    "skill": "技能",
    "skills": "技能",
    "tool": "工具",
    "tools": "工具",
    "API": "API",
    "data": "数据",
    "file": "文件",
    "files": "文件",
    "user": "用户",
    "users": "用户",
    "task": "任务",
    "tasks": "任务",
    "project": "项目",
    "projects": "项目",
    "code": "代码",
    "security": "安全",
    "privacy": "隐私",
    "performance": "性能",
    "cost": "成本",
    "token": "代币",
    "wallet": "钱包",
    "blockchain": "区块链",
    "crypto": "加密",
    "model": "模型",
    "models": "模型",
    "LLM": "大语言模型",
    "AI": "人工智能",
    "chat": "聊天",
    "message": "消息",
    "email": "邮件",
    "calendar": "日历",
    "schedule": "日程",
    "note": "笔记",
    "notes": "笔记",
    "document": "文档",
    "documents": "文档",
    "image": "图片",
    "images": "图片",
    "video": "视频",
    "audio": "音频",
    "music": "音乐",
    "voice": "语音",
    "speech": "语音",
    "text": "文本",
    "search": "搜索",
    "research": "研究",
    "web": "网页",
    "browser": "浏览器",
    "automation": "自动化",
    "workflow": "工作流",
    "pipeline": "管道",
    "integration": "集成",
    "platform": "平台",
    "service": "服务",
    "services": "服务",
    "app": "应用",
    "application": "应用",
    "dashboard": "仪表板",
    "interface": "界面",
    "command": "命令",
    "CLI": "命令行",
    "terminal": "终端",
    "server": "服务器",
    "cloud": "云",
    "database": "数据库",
    "storage": "存储",
    "network": "网络",
    "devops": "开发运维",
    "CI/CD": "持续集成/部署",
    "git": "Git",
    "github": "GitHub",
    "repository": "仓库",
    "commit": "提交",
    "branch": "分支",
    "merge": "合并",
    "pull request": "拉取请求",
    "issue": "问题",
    "bug": "错误",
    "feature": "功能",
    "release": "发布",
    "version": "版本",
    "package": "包",
    "dependency": "依赖",
    "library": "库",
    "framework": "框架",
    "template": "模板",
    "component": "组件",
    "module": "模块",
    "plugin": "插件",
    "extension": "扩展",
    "theme": "主题",
    "style": "样式",
    "design": "设计",
    "UI": "用户界面",
    "UX": "用户体验",
    "responsive": "响应式",
    "mobile": "移动",
    "desktop": "桌面",
    "iOS": "iOS",
    "Android": "Android",
    "macOS": "macOS",
    "Windows": "Windows",
    "Linux": "Linux",
    
    # 形容词
    "smart": "智能",
    "automatic": "自动",
    "automated": "自动化的",
    "real-time": "实时",
    "fast": "快速",
    "secure": "安全",
    "private": "私密",
    "simple": "简单",
    "easy": "容易",
    "powerful": "强大",
    "efficient": "高效",
    "reliable": "可靠",
    "scalable": "可扩展",
    "flexible": "灵活",
    "custom": "自定义",
    "personal": "个人",
    "professional": "专业",
    "advanced": "高级",
    "basic": "基础",
    "local": "本地",
    "remote": "远程",
    "online": "在线",
    "offline": "离线",
    "free": "免费",
    "open source": "开源",
    
    # 短语
    "for AI agents": "为 AI 代理设计",
    "for Clawdbot": "为 Clawdbot 设计",
    "using": "使用",
    "with": "带有",
    "via": "通过",
    "based on": "基于",
    "powered by": "驱动",
    "designed for": "专为...设计",
    "optimized for": "为...优化",
    "support for": "支持",
    "integration with": "与...集成",
    "seamless": "无缝",
    "one-click": "一键",
    "end-to-end": "端到端",
    "full-featured": "功能齐全",
    "lightweight": "轻量级",
    "minimal": "极简",
    "comprehensive": "全面",
    "complete": "完整",
    "unified": "统一",
    "centralized": "集中",
    "decentralized": "去中心化",
    "distributed": "分布式",
    "peer-to-peer": "点对点",
    "client-server": "客户端 - 服务器",
    
    # 技术术语（保持英文或音译）
    "Python": "Python",
    "JavaScript": "JavaScript",
    "TypeScript": "TypeScript",
    "React": "React",
    "Vue": "Vue",
    "Next.js": "Next.js",
    "Node.js": "Node.js",
    "Docker": "Docker",
    "Kubernetes": "Kubernetes",
    "AWS": "AWS",
    "Azure": "Azure",
    "GCP": "GCP",
    "Solana": "Solana",
    "Ethereum": "以太坊",
    "Bitcoin": "比特币",
    "Base": "Base",
    "TON": "TON",
    "REST API": "REST API",
    "GraphQL": "GraphQL",
    "WebSocket": "WebSocket",
    "OAuth": "OAuth",
    "JWT": "JWT",
    "SSH": "SSH",
    "SSL": "SSL",
    "TLS": "TLS",
    "HTTP": "HTTP",
    "HTTPS": "HTTPS",
    "JSON": "JSON",
    "XML": "XML",
    "CSV": "CSV",
    "Markdown": "Markdown",
    "HTML": "HTML",
    "CSS": "CSS",
}

def translate_description(desc):
    """翻译描述文本"""
    result = desc
    
    # 按长度降序替换，避免部分匹配问题
    sorted_keys = sorted(TRANSLATION_MAP.keys(), key=len, reverse=True)
    
    for key in sorted_keys:
        value = TRANSLATION_MAP[key]
        # 使用正则进行单词边界匹配（不区分大小写）
        pattern = r'\b' + re.escape(key) + r'\b'
        result = re.sub(pattern, value, result, flags=re.IGNORECASE)
    
    return result

def process_file_zh(filepath, content):
    """处理文件：翻译描述部分"""
    lines = content.split('\n')
    translated_lines = []
    
    for line in lines:
        # 跳过空行、标题、链接行
        if not line.strip():
            translated_lines.append(line)
            continue
        if line.startswith('#'):
            translated_lines.append(line)
            continue
        if line.strip().startswith('[') and '](' in line:
            translated_lines.append(line)
            continue
        
        # 处理列表项：- [skill-name](url) - 描述
        match = re.match(r'^(- \[[^\]]+\]\([^)]+\) - )(.+)$', line)
        if match:
            prefix = match.group(1)
            desc = match.group(2)
            translated_desc = translate_description(desc)
            translated_lines.append(f"{prefix}{translated_desc}")
            continue
        
        # 其他行：尝试翻译
        if 'Gold Sponsor' in line or 'Silver Sponsor' in line or 'Bronze Sponsor' in line:
            continue  # 跳过赞助行
        if 'Sponsor' in line and any(x in line for x in ['Gold', 'Silver', 'Bronze']):
            continue
        
        translated_lines.append(line)
    
    # 检查是否已有来源标注
    has_source = any('*翻译自：' in line for line in translated_lines)
    if not has_source:
        base_name = os.path.basename(filepath).replace('.md', '')
        source_url = f"{RAW_BASE_URL}/{filepath}"
        translated_lines.append("")
        translated_lines.append(f"*翻译自：{source_url}*")
    
    return '\n'.join(translated_lines)

def main():
    import subprocess
    
    print("🔄 开始翻译 awesome-openclaw-skills 技能描述...")
    print()
    
    # 获取所有 .zh.md 文件
    categories_dir = os.path.join(PROJECT_DIR, "categories")
    zh_files = [f for f in os.listdir(categories_dir) if f.endswith('.zh.md')]
    
    print(f"发现 {len(zh_files)} 个待翻译文件")
    print()
    
    stats = []
    for filename in zh_files:
        filepath = os.path.join(categories_dir, filename)
        print(f"处理：{filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取对应的英文文件名
        en_filename = filename.replace('.zh.md', '.md')
        en_filepath = os.path.join("categories", en_filename)
        
        translated = process_file_zh(en_filepath, content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(translated)
        
        line_count = len(translated.split('\n'))
        stats.append((filename, line_count))
        print(f"  → 完成：{line_count} 行")
    
    print()
    print("📊 翻译统计:")
    print(f"  翻译文件数：{len(stats)}")
    total_lines = sum(lines for _, lines in stats)
    print(f"  总行数：{total_lines}")
    
    # Git 提交
    print()
    print("提交更改...")
    subprocess.run('git add -A', shell=True, cwd=PROJECT_DIR)
    subprocess.run('git commit -m "feat: 翻译技能描述 2026-03-05"', shell=True, cwd=PROJECT_DIR)
    
    print("推送到 GitHub...")
    result = subprocess.run('git push origin main', shell=True, cwd=PROJECT_DIR, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ 推送成功")
    else:
        print(f"推送输出：{result.stdout}")
        if result.stderr:
            print(f"推送错误：{result.stderr}")
    
    print()
    print("=" * 50)
    print("✅ 翻译任务完成")
    print(f"  翻译了 {len(stats)} 个文件，共 {total_lines} 行")

if __name__ == "__main__":
    main()
