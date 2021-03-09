#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :variables.py
@说明        :
@时间        :2020/08/19 15:17:56
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, Optional

from app.models.case import Case
from app.models.project import Project
from app.models.variables import Variables
from app.validators.base_validator import BaseForm as Form


class variablesForm(Form):
    key = StringField(
        validators=[Length(min=1, max=255), DataRequired(message="key不允许为空")]
    )
    value = StringField(validators=[Length(min=1, max=255), Optional()])
    case_id = IntegerField(validators=[DataRequired(message="caseId不允许为空")])
    type = IntegerField(validators=[DataRequired(message="type不允许为空")])

    def validate_pro_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="project不存在")

    def validate_type(self, value):
        if int(value.data) > 7:
            raise ValidationError(message="类型无法解析")


class addVariablesForm(variablesForm):
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])

    def validate_case_id(self, value):
        if not Case.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="case 不存在 ")

    def validate_key(self, value):
        # 修改为项目纬度进行判断
        if Variables.query.filter_by(pro_id=self.pro_id.data, key=value.data).first():
            raise ValidationError(message="该变量在项目中已存在")


class updateVariablesForm(variablesForm):
    id = IntegerField(validators=[DataRequired(message="Id不允许为空")])

    def validate_case_id(self, value):
        if not Case.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="case 不存在 ")

    def validate_id(self, value):
        if not Variables.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="variables 不存在")
