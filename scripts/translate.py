#!/usr/bin/env python3
"""
分段翻译 Markdown 文件 - 使用 AI 翻译
保留代码块、链接、图片等结构，只翻译文本内容
"""

import sys
import re
import json
from pathlib import Path

def extract_code_blocks(content):
    """提取并替换代码块为占位符"""
    blocks = []
    def replace(match):
        idx = len(blocks)
        blocks.append(match.group())
        return f"___CODE_BLOCK_{idx}___"
    content = re.sub(r'```[\s\S]*?```', replace, content)
    return content, blocks

def restore_code_blocks(content, blocks):
    """恢复代码块"""
    for idx, block in enumerate(blocks):
        content = content.replace(f"___CODE_BLOCK_{idx}___", block)
    return content

def translate_batch(text_batch):
    """
    批量翻译文本段
    这里输出待翻译内容，由外部 AI 处理
    """
    print(json.dumps({"texts": text_batch}, ensure_ascii=False))
    return None  # 由外部处理

def process_file(input_path):
    content = Path(input_path).read_text(encoding='utf-8')
    
    # 提取代码块
    content, code_blocks = extract_code_blocks(content)
    
    # 按段落分割（保留 Markdown 结构）
    paragraphs = re.split(r'(\n\n+)', content)
    
    # 过滤出需要翻译的文本段落
    text_segments = []
    for i, para in enumerate(paragraphs):
        if para.strip() and not para.startswith('\n'):
            # 跳过纯格式行
            if not re.match(r'^[\s\|!\-\*\d\.#]+$', para):
                text_segments.append((i, para))
    
    print(f"文件：{input_path}")
    print(f"总段落数：{len(paragraphs)}")
    print(f"待翻译段落：{len(text_segments)}")
    print(f"代码块：{len(code_blocks)}")
    print("---")
    
    # 输出待翻译内容（每段）
    for idx, (pos, text) in enumerate(text_segments[:5]):  # 前 5 段示例
        print(f"\n[段落 {idx}]")
        print(text[:200])
    
    return text_segments, code_blocks

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法：python translate.py <input.md>")
        sys.exit(1)
    process_file(sys.argv[1])
