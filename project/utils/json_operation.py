#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import re

"""
    【json operation.py :json处理相关函数】
"""

"""
    ——————————提示词json构造函数————————————————
"""


def role_content_json(role, content):
    return {"role": role, "content": content}



"""
    ————————————————json格式化函数————————————————
"""


def format_json(json_str):
    """
    检查并补全json字符串格式（大括号，逗号问题）
    """
    # 尝试解析JSON字符串，如果成功则返回原字符串
    try:
        json.loads(json_str)
        return json_str
    except json.JSONDecodeError:
        # 如果解析失败，说明JSON字符串有误，尝试修复

        # 修复大括号问题
        json_with_braces = fix_braces(json_str)

        # # 修复逗号问题
        # fixed_json_str = fix_missing_comma(json_with_braces)

    return json_with_braces


def fix_braces(json_str):
    # 去除字符串首尾的空格以准确检查首尾字符
    trimmed_str = json_str.strip()

    # 检查字符串是否以开放的大括号开始
    if not trimmed_str.startswith('{'):
        # 如果不是，尝试找到第一个出现的 '{'
        first_brace_pos = trimmed_str.find('{')
        if first_brace_pos != -1:
            # 如果找到了 '{'，从该位置开始截取字符串
            print("这个字符串开头不是{，已经截取成功")
            trimmed_str = trimmed_str[first_brace_pos:]
        else:
            # 如果没有找到 '{'，则在开始位置添加 '{'
            print("这个json没有{，成功查漏补缺")
            trimmed_str = '{' + trimmed_str

    # 检查字符串是否以闭合的大括号结束
    if not trimmed_str.endswith('}'):
        # 如果不是，尝试找到最后一个出现的 '}'
        last_brace_pos = trimmed_str.rfind('}')
        if last_brace_pos != -1:
            # 如果找到了 '}'，截取到该位置
            trimmed_str = trimmed_str[:last_brace_pos + 1]
        else:
            # 如果没有找到 '}'，则在末尾位置添加 '}'
            print("这个json没有}，成功查漏补缺")
            trimmed_str += '}'

    return trimmed_str


def fix_missing_comma(json_str):
    # 定义一个正则表达式，用于查找在"thoughts"值和"action"键之间缺少逗号的情况
    pattern = r'"thoughts":[^{}]*"(?P<action>action)"'
    # 尝试查找匹配
    match = re.search(pattern, json_str)

    if match:
        # 如果找到匹配，说明"action"前缺少逗号

        action_start = match.start('action')

        # 计算"thoughts"键值对的结束位置（即"thoughts"值的结束位置）
        thoughts_end = json_str.rfind('"', 0, action_start)

        # 在"thoughts"值后插入逗号
        corrected_str = json_str[:thoughts_end] + ', ' + json_str[thoughts_end:]

        # 确保修正后的字符串是有效的JSON格式
        try:
            json.loads(corrected_str)
            print("已修复json逗号。")
            return corrected_str
        except json.JSONDecodeError:
            raise ValueError("修正后的JSON字符串仍无法解析。")
    else:
        # 如果没有找到匹配，说明JSON字符串格式正确
        return json_str


# # 示例使用
# json_str = ('{"thoughts": "哎呀，一下子变空白了，我可以自己想事情了！"\n'
#             '"action": "bre,scrh"}')
# fixed_json = format_json(json_str)
#
# print(fixed_json)

