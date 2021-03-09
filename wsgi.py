#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :wsgi.py
@说明        :
@时间        :2020/09/17 13:55:26
@作者        :Leo
@版本        :1.0
'''

from dotenv import load_dotenv
import os
from app import create_app

from gevent import monkey
monkey.patch_all()

# 配置测试环境和开发环境的控制器
dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    env = os.getenv("FLASK_ENV")
else:
    env = 'production'

app = create_app(env)
# 关键点，往celery推入flask信息，使得celery能使用flask上下文
app.app_context().push()
