#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录函数开始执行的时间
        result = func(*args, **kwargs)  # 执行函数
        end_time = time.time()  # 记录函数结束执行的时间
        print(f"{func.__name__} 运行时间: {end_time - start_time:.6f} 秒")
        return result

    return wrapper
