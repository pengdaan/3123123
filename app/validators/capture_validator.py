#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :capture_validator.py
@说明        :
@时间        :2021/04/23 17:24:32
@作者        :Leo
@版本        :1.0
'''

from wtforms import IntegerField, StringField, ValidationError, FieldList
from app.models.project import Project
from app.validators.base_validator import BaseForm as Form
from wtforms.validators import DataRequired, Length


class captureForm(Form):
    cate_id = IntegerField(validators=[DataRequired(message="分类不允许为空")])
    pro_id = IntegerField(validators=[DataRequired(message="项目不允许为空")])
    user_id = IntegerField(validators=[DataRequired(message="用户不允许为空")])
    api_details = FieldList(
        StringField(), validators=[Length(min=1), DataRequired(message="请选择需要导入的api")]
    )

    def validate_pro_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="该项目不存在")