#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :run.py
@说明        :
@时间        :2020/08/13 10:24:52
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired

from app.models.config import Config
from app.models.project import Project
from app.models.sqlconfig import Sql_Config
from app.validators.base_validator import BaseForm as Form


class RunForm(Form):

    id = IntegerField([DataRequired(message="apiId不允许为空")])
    config_id = IntegerField([DataRequired(message="configId不允许为空")])
    module_id = IntegerField([DataRequired(message="moduleId不允许为空")])


class DebugForm(Form):
    api_id = StringField()
    body = StringField()
    config_id = IntegerField([DataRequired(message="configId不允许为空")])
    pro_id = IntegerField([DataRequired(message="proId不允许为空")])
    sql_config_id = IntegerField([DataRequired(message="sqlConfigId不允许为空")])

    def validate_pro_id(self, value):
        Project.query.filter_by(id=value.data, status=1).first_or_404("projectId")

    def validate_config_id(self, value):
        Config.query.filter_by(id=value.data, status=1).first_or_404("ConfigId")

    def validate_sql_config_id(self, value):
        if value.data is not None:
            Sql_Config.query.filter_by(id=value.data, status=1).first()
        else:
            raise ValidationError(message="请选择数据库")
