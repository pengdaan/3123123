#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :blueprints.py
@说明        :蓝图注册器
@时间        :2020/08/05 21:41:27
@作者        :Leo
@版本        :1.0
"""
from app.api.v1 import create_blueprint_v1


def register_blueprints(app):
    app.register_blueprint(create_blueprint_v1(), url_prefix="/api/1")
