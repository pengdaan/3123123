#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :client.py
@说明        :客户端注册
@时间        :2020/08/05 21:55:20
@作者        :Leo
@版本        :1.0
"""

from flask import g, jsonify, request

from app.libs.auth import auth_jwt, luna_auth_token
from app.libs.code import Sucess
from app.libs.redprint import Redprint
from app.models.project import Project
from app.models.user import User
from app.validators.user_validator import LoginForm, UserForm

api = Redprint("user")


@api.route("/register", methods=["POST"])
def register():
    """
    [summary]
    用户注册
    """
    form = UserForm().validate_for_api()
    uid = User.add_user(form.username.data, form.password.data, form.email.data)
    res = {
        "id": uid,
        "username": form.username.data,
        "email": form.email.data,
    }
    return Sucess(data=res)


@api.route("/login", methods=["POST"])
def login():
    """[summary]
    用户登录
    Returns:
        [type]: 用户信息
    """
    form = LoginForm().validate_for_api()
    users = User.verify(form.username.data, form.password.data)
    token = luna_auth_token(users["uid"], form.username.data)
    this_token = token.decode("ascii")
    User.add_token(users["uid"], this_token)
    res = {
        "id": users["uid"],
        "token": this_token,
        "username": users["username"],
    }
    return Sucess(data=res)


@api.route("/info", methods=["GET"])
def user_info():
    """
    获取用户信息
    :return:
    """
    token = request.args.get("token")
    users = User.query.filter_by(token=token).first_or_404("username")
    users.hide("token")
    ProInfo = (
        Project.query.filter_by(status=1).order_by(Project.update_time.desc()).first()
    )
    return jsonify(
        {
            "responseCode": 2000,
            "data": users,
            "pro_info": {"id": ProInfo.id, "pro_name": ProInfo.project_name},
        }
    )


@api.route("/logout", methods=["GET"])
@auth_jwt
def logout():
    """
    退出登录
    """
    uid = g.user
    User.update_user_status(uid, 0, 2)
    return Sucess()
