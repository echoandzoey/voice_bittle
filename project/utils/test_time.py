#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from project.utils.print_format import colored_output


def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time

        # Unicode小时钟图标
        colored_output(f"🕐 [{func.__name__}] {duration:.2f} s", "blue")
        return result

    return wrapper
