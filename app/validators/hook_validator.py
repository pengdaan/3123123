#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :code.py
@说明        :
@时间        :2020/08/17 10:16:01
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Optional
from app.models.project import Project
from app.validators.base_validator import BaseForm as Form


class HookForm(Form):
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])
    code = StringField()
    api_id = IntegerField(validators=[Optional()])
    desc = StringField()
    fun_name = StringField()

    def validators_pro_id(self, value):
        if not Project.query.filter_by(id=value.data).first():
            raise ValidationError(message="项目不存在")


class AddHookForm(HookForm):
    id = IntegerField(validators=[Optional()])


class UpdateHookForm(HookForm):
    id = IntegerField()


class AddApiHookForm(Form):
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])
    api_id = IntegerField(validators=[Optional()])
    code = StringField()
    fun_name = StringField()


class DelHookForm(Form):
    id = IntegerField()
    func_name = StringField(validators=[DataRequired(message="函数名不允许为空")])
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])
    api_id = IntegerField(validators=[Optional()])
