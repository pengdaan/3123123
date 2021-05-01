#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :variable_validator.py
@说明        :
@时间        :2021/04/27 15:38:58
@作者        :Leo
@版本        :1.0
'''


from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, Optional
from app.models.project import Project
from app.models.variable import Variable
from app.validators.base_validator import BaseForm as Form


class VariableBaseForm(Form):
    variable_name = StringField(validators=[Length(min=1, max=255), DataRequired(message="name不允许为空")])
    status = IntegerField([DataRequired(message="状态不允许为空")])
    pro_id = IntegerField([DataRequired(message="项目id不允许为空")])
   
    def validate_pro_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="该项目不存在")

    def validate_variable_name(self, value):
        if Variable.query.filter_by(name=value.data, pro_id=self.pro_id.data, status=1).first():
            raise ValidationError(message="该变量已存在")


class AddVariableForm(VariableBaseForm):
    api_id = IntegerField(validators=[Optional()])
    case_id = IntegerField(validators=[Optional()])
    module_id = IntegerField(validators=[Optional()])
    case_module_id = IntegerField(validators=[Optional()])


class UpdateVariableForm(Form):
    id = IntegerField([DataRequired(message="id不允许为空")])
    variable_name = StringField(validators=[Length(min=1, max=255), DataRequired(message="name不允许为空")])
    status = IntegerField([DataRequired(message="状态不允许为空")])
    pro_id = IntegerField([DataRequired(message="项目id不允许为空")])
    api_id = IntegerField(validators=[Optional()])
    case_id = IntegerField(validators=[Optional()])

    def validate_pro_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="该项目不存在")


class VariableListForm(Form):
    api_id = IntegerField(validators=[Optional()])
    case_id = IntegerField(validators=[Optional()])


class DelVariableListForm(Form):
    variable_id = IntegerField([DataRequired(message="id不允许为空")])
    variable_name = StringField(validators=[Length(min=1, max=255), DataRequired(message="name不允许为空")])

    def validate_variable_id(self, value):
        if not Variable.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="该变量不存在")