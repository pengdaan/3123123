#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :module.py
@说明        :
@时间        :2020/08/12 10:51:14
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, Optional

from app.models.module import Module
from app.models.sqlconfig import Sql_Config
from app.validators.base_validator import BaseForm as Form


class ModuleForm(Form):
    name = StringField(
        validators=[Length(min=1, max=255), DataRequired(message="模块名不可为空")]
    )
    body = StringField()
    api_id = IntegerField(validators=[DataRequired(message="apiId不可为空")])


class updateModuleForm(Form):
    id = IntegerField(validators=[DataRequired(message="moduleId不可为空")])
    body = StringField()
    sql_config_id = IntegerField(validators=[Optional()])

    def validate_id(self, value):
        if not Module.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="moduleId不存在")

    def validate_sql_config_id(self, value):
        if not Sql_Config.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="请绑定数据库")


class searchModuleForm(Form):
    api_id = IntegerField(validators=[DataRequired(message="apiId不可为空")])
    key = StringField()
    user_id = IntegerField()


class copyModuleForm(Form):
    copy_id = IntegerField(validators=[DataRequired(message="copyId不可为空")])
    id = IntegerField(validators=[DataRequired(message="moduleId不可为空")])

    def validate_id(self, value):
        if not Module.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="moduleId不存在")

    def validate_copy_id(self, value):
        if not Module.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="moduleId不存在")


class updateModuleNameForm(Form):
    name = StringField(
        validators=[Length(min=1, max=255), DataRequired(message="模块名不可为空")]
    )
    id = IntegerField(validators=[DataRequired(message="moduleId不可为空")])

    def validate_id(self, value):
        if not Module.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="moduleId不存在")
