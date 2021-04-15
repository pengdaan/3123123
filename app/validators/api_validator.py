#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :api.py
@说明        :
@时间        :2020/08/12 09:17:54
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Length

from app.models.api import Api
from app.models.project import Project
from app.validators.base_validator import BaseForm as Form
from sqlalchemy import text
from app.models.base import db


class ApiForm(Form):
    name = StringField(
        validators=[Length(min=1, max=255), DataRequired(message="name不允许为空")]
    )
    path = StringField(
        validators=[Length(min=1, max=500), DataRequired(message="path不允许为空")]
    )
    method = StringField(validators=[DataRequired(message="method不允许为空")])
    type = IntegerField(validators=[DataRequired(message="接口类型不允许为空")])
    cat_id = IntegerField(validators=[DataRequired(message="catId不允许为空")])


class addApiForm(ApiForm):
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])

    def validate_path(self, value):
        if Api.query.filter_by(
            path=value.data, cat_id=self.cat_id.data, status=1
        ).first():
            raise ValidationError(message="此接口已存在该分类下")

    def validate_pro_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="该项目不存在")


class updateApiForm(ApiForm):
    id = IntegerField()
    body = StringField()

    def validate_id(self, value):
        if not Api.query.filter_by(id=value.data).first():
            raise ValidationError(message="Api不存在")

    def validate_path(self, value):
        api_info = Api.query.filter_by(id=self.id.data).first()
        taget_sql = "select * from api where pro_id =:pro_id and path=:path and id !=:id"
        res = db.session.execute(text(taget_sql), {"id": api_info.id, "pro_id": api_info.pro_id, "path": value.data}).fetchall()
        if res:
            raise ValidationError(message="接口路径已存在，请勿重复添加")


class FindApiForm(Form):
    proId = IntegerField(validators=[DataRequired(message="proId不允许为空")])
    cateId = StringField()
    name = StringField()
    page = IntegerField()
