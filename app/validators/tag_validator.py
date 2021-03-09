#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :tag.py
@说明        :
@时间        :2020/08/14 16:24:42
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired

from app.models.project import Project
from app.models.tag import Case_Tag
from app.validators.base_validator import BaseForm as Form


class TagBaseForm(Form):
    tag_name = StringField(validators=[DataRequired(message="标签名不允许为空")])
    desc = StringField()
    pro_id = IntegerField(validators=[DataRequired(message="项目Id不允许为空")])

    def validate_case_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="ProId不存在")


class addTagForm(TagBaseForm):
    def validate_tag_name(self, value):
        if Case_Tag.query.filter_by(
            pro_id=self.pro_id.data, tag_name=value.data, status=1
        ).first():
            raise ValidationError(message="该标签已存在")


class updateTagForm(TagBaseForm):
    id = IntegerField()

    def validate_id(self, value):
        if not Case_Tag.query.filter_by(id=value.data).first():
            raise ValidationError(message="该标签不存在")
