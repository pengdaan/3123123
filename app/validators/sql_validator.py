#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :sql.py
@说明        :
@时间        :2020/08/19 09:44:01
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, Optional
from app.models.project import Project
from app.models.sqlconfig import Sql_Config
from app.validators.base_validator import BaseForm as Form


class SQLBaseForm(Form):
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])
    name = StringField(
        validators=[Length(min=1, max=255), DataRequired(message="name不允许为空")]
    )
    host = StringField(
        validators=[Length(min=1, max=255), DataRequired(message="host不允许为空")]
    )
    username = StringField(
        validators=[Length(min=1, max=50), DataRequired(message="username不允许为空")]
    )
    password = StringField(
        validators=[Length(min=1, max=50), DataRequired(message="password不允许为空")]
    )
    database = StringField(validators=[Optional()])
    port = IntegerField(validators=[DataRequired(message="port不允许为空")])

    def validate_pro_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="项目不存在")


class addSQLForm(SQLBaseForm):
    def validate_host(self, value):
        if Sql_Config.query.filter_by(
            pro_id=self.pro_id.data,
            host=value.data,
            database=self.database.data,
            status=1,
        ).first():
            raise ValidationError(message="该数据库配置已存在")


class updateSQLForm(SQLBaseForm):
    id = IntegerField(validators=[DataRequired(message="sqlId不允许为空")])

    def validate_id(self, value):
        if not Sql_Config.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="sqlId不存在")


class connectSQLForm(Form):
    id = IntegerField(validators=[DataRequired(message="sqlId不允许为空")])
    data = StringField(validators=[Optional()])

    # other_config_id = IntegerField(
    #     validators=[DataRequired(message='sql配置不允许为空')])

    def validate_id(self, value):
        if not Sql_Config.query.filter_by(id=value.data).first():
            raise ValidationError(message="sqlId不存在")

    # def validate_other_config_id(self, value):
    #     if not Config.query.filter_by(id=value.data).first():
    #         raise ValidationError(message='配置不存在')


class searchSQLForm(Form):
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])
    kw = StringField(validators=[Optional()])

    def validate_pro_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="项目不存在")
