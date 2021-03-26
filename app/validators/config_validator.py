#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :config.py
@说明        :
@时间        :2020/08/17 11:22:45
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired

from app.models.config import Config
from app.validators.base_validator import BaseForm as Form


class ConfigForm(Form):
    type = IntegerField(validators=[DataRequired(message="配置类型不允许为空")])
    name = StringField(validators=[DataRequired(message="配置名不允许为空")])
    base_url = StringField()


class addConfigForm(ConfigForm):
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])
    header = StringField()
    request = StringField()
    variables = StringField()
    hooks = StringField()
    parameters = StringField()
    validate = StringField()


class updateConfigForm(Form):
    id = IntegerField()
    data = StringField(validators=[DataRequired(message="configData不允许为空")])
    type = IntegerField()

    def validate_id(self, value):
        if not Config.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="ConfigId不存在")


class searchConfigForm(Form):
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])
    kw = StringField()
