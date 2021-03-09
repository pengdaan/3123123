#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :base.py
@说明        :基础检验器
@时间        :2020/08/06 22:06:39
@作者        :Leo
@版本        :1.0
"""
from flask import request
from wtforms import Form

from app.libs.code import parameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise parameterException(data=self.errors)
        return self
