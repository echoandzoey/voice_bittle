#!/usr/bin/env python
# -*- coding:utf-8 -*-
def ensure_json_wrapped_with_braces(json_str):
    """
    确保给定的JSON字符串以开放的大括号开始，以闭合的大括号结束。

    :param json_str: 需要检查和修改的JSON字符串。
    :return: 修改后的JSON字符串。
    """
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
    else:
        print("-----------")

    # 检查字符串是否以闭合的大括号结束
    if not trimmed_str.endswith('}'):
        # 如果不是，尝试找到最后一个出现的 '}'
        last_brace_pos = trimmed_str.rfind('}')
        if last_brace_pos != -1:
            # 如果找到了 '}'，截取到该位置
            trimmed_str = trimmed_str[:last_brace_pos + 1]
        else:
            # 如果没有找到 '}'，则在末尾位置添加 '}'
            # print("这个json没有}，成功查漏补缺")
            trimmed_str += '}'
    else:
        print("-----------")

    return trimmed_str
