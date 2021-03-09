#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :forms.py
@说明        :校验
@时间        :2020/08/06 11:54:04
@作者        :Leo
@版本        :1.0
"""
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Email, Length

from app.models.user import User
from app.validators.base_validator import BaseForm as Form


class UserForm(Form):
    username = StringField(
        validators=[Length(min=4, max=255), DataRequired(message="用户名不允许为空")]
    )
    password = StringField(validators=[DataRequired(message="密码不允许为空")])
    email = StringField(
        validators=[
            Email(message="邮箱格式不正确"),
            Length(min=1, max=255),
            DataRequired(message="邮箱不允许为空"),
        ]
    )
    token = StringField()

    def validate_email(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError(message="邮箱已存在")

    def validate_username(self, value):
        if User.query.filter_by(username=value.data).first():
            raise ValidationError(message="用户名已存在")


class LoginForm(Form):
    username = StringField(
        validators=[Length(min=4, max=25), DataRequired(message="用户名不允许为空")]
    )
    password = StringField(validators=[DataRequired(message="密码不允许为空")])
