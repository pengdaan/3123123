#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :helper.py
@说明        :
@时间        :2020/08/18 21:12:12
@作者        :Leo
@版本        :1.0
"""

import datetime
import json
import time
import uuid

from flask import g, render_template


class Helper:
    def __init__(self):
        pass

    """
    统一渲染方法
    """

    @staticmethod
    def custom_render(template, context={}):
        if "current_user" in g:
            context["current_user"] = g.current_user
        return render_template(template, **context)

    """
    获取当前时间
    """

    @staticmethod
    def getCurrentDate(format="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.now()

    """
    uuid格式化
    """

    @staticmethod
    def getUUid():
        return str(uuid.uuid1()).replace("-", "")

    """
    jinja中调用的时间转换过滤器
    """

    @staticmethod
    def convert_timestamp(value):
        try:
            return time.strftime(
                "%Y--%m--%d %H:%M:%S", time.localtime(int(float(value)))
            )
        except Exception as e:
            return value

    """
      jinja中格式化json的过滤器
    """

    @staticmethod
    def convert_json(value):
        try:
            value = json.dumps(
                value,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
                separators=(",", ":"),
            )
            return value

        except Exception as e:
            return value
