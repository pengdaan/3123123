#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :swagger.py
@说明        :
@时间        :2020/11/16 17:06:17
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired

from app.models.project import Project
from app.validators.base_validator import BaseForm as Form


class SwaggerBaseForm(Form):
    url = StringField(validators=[DataRequired(message="swaggerUI链接不允许为空")])
    add_type = IntegerField(validators=[DataRequired(message="导入类型不能为空")])
    pro_id = IntegerField(validators=[DataRequired(message="项目Id不允许为空")])
    user_id = IntegerField(validators=[DataRequired(message="UserId is not None")])

    def validate_case_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="ProId不存在")
