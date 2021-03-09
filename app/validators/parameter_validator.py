#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :parameters.py
@说明        :
@时间        :2020/10/16 16:02:25
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired
from app.validators.base_validator import BaseForm as Form


class ParametersForm(Form):
    case_id = IntegerField(validators=[DataRequired(message="用例Id不允许为空")])
    parameters = StringField()
    key = StringField()


class updateParametersForm(ParametersForm):
    id = IntegerField(validators=[DataRequired(message="参数Id不允许为空")])
