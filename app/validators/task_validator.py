#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :task.py
@说明        :
@时间        :2020/08/19 13:58:38
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField
from wtforms.validators import Optional

from app.validators.base_validator import BaseForm as Form


class TasksForm(Form):
    kw = StringField(validators=[Optional()])
    page = IntegerField()
