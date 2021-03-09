#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :DecimalEncoder.py
@说明        :flask 序列化拓展
@时间        :2020/08/10 14:19:08
@作者        :Leo
@版本        :1.0
"""
import decimal
from datetime import date
from flask._compat import text_type
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.code import ServerError
from app.libs.httprunner.parser import LazyString


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        # 判断o是否含有keys属性和get__item__ 方法
        if hasattr(o, "keys") and hasattr(o, "__getitem__"):
            # return {"code": 0, "data": dict(o), "msg": "SUCESS"}
            return dict(o)
        if isinstance(o, date):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, LazyString):
            return text_type(o)
        raise ServerError()


# class Flask(_Flask):
#     # 替换Flask中原有的json_encoder方法。
#     json_encoder = JSONEncoder
