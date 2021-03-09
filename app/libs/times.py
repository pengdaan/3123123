#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :times.py
@说明        :时间处理类
@时间        :2020/08/06 15:26:37
@作者        :Leo
@版本        :1.0
"""
from datetime import datetime


def get_time():
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dt
