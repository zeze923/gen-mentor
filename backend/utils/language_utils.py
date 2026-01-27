# -*- coding: utf-8 -*-
"""语言检测和适配工具"""

import re


def detect_language(text: str) -> str:
    """
    检测文本的主要语言
    
    Args:
        text: 要检测的文本
        
    Returns:
        'zh' 表示中文，'en' 表示英文
    """
    if not text:
        return 'en'
    
    # 统计中文字符数量
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 统计英文字符数量
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    
    # 如果中文字符占比超过 30%，认为是中文
    total_chars = chinese_chars + english_chars
    if total_chars == 0:
        return 'en'
    
    chinese_ratio = chinese_chars / total_chars
    return 'zh' if chinese_ratio > 0.3 else 'en'


def get_language_instruction(language: str = 'en') -> str:
    """
    获取语言指令文本
    
    Args:
        language: 'zh' 或 'en'
        
    Returns:
        语言指令文本
    """
    if language == 'zh':
        return """
**重要：语言要求**
- 请使用**中文**生成所有内容
- 所有标题、描述、解释都必须使用中文
- 保持专业和清晰的中文表达
"""
    else:
        return """
**Important: Language Requirement**
- Please generate all content in **English**
- All titles, descriptions, and explanations must be in English
- Maintain professional and clear English expression
"""


def get_language_from_goal(learning_goal: str) -> str:
    """
    从学习目标中检测语言
    
    Args:
        learning_goal: 学习目标文本
        
    Returns:
        'zh' 或 'en'
    """
    return detect_language(learning_goal)


def add_language_instruction_to_prompt(prompt: str, learning_goal: str) -> str:
    """
    在 prompt 中添加语言指令
    
    Args:
        prompt: 原始 prompt
        learning_goal: 学习目标（用于检测语言）
        
    Returns:
        添加了语言指令的 prompt
    """
    language = get_language_from_goal(learning_goal)
    language_instruction = get_language_instruction(language)
    
    # 在 prompt 开头添加语言指令
    return f"{language_instruction}\n\n{prompt}"
