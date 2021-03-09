#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :executor.py
@说明        :flask 异步设置
@时间        :2020/08/19 14:38:22
@作者        :Leo
@版本        :1.0
"""

from flask_executor import Executor

executor = Executor()


def register_Executor(app):
    executor.init_app(app)
