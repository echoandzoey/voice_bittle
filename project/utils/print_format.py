#!/usr/bin/env python
# -*- coding:utf-8 -*-
def colored_output(text, color_code):
    """
    打印彩色输出

    :param text: 要打印的文本
    :param color_code: ANSI转义颜色代码
    """
    # ANSI转义颜色代码前缀
    reset = '\033[0m'   # 重置颜色到默认

    # 根据颜色代码设置颜色前缀
    color_mapping = {
        "red": '\033[91m',
        "green": '\033[92m',
        "yellow": '\033[93m',
        "blue": '\033[94m',
        "purple": '\033[95m',
        "cyan": '\033[96m'
    }
    color_prefix = color_mapping.get(color_code.lower(), '')  # 如果颜色代码不在预定义中，则默认为空
    # 打印格式化的输出
    print(f"{color_prefix}{text}{reset}")

# 使用示例
# colored_output('🐕', '执行动作', 'green')
