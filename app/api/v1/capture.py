#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :capture.py
@说明        :
@时间        :2021/03/29 15:09:03
@作者        :Leo
@版本        :1.0
'''

from app.libs.redprint import Redprint
from app.libs.code import Sucess
from app.models.user import User
from app.models.capture import get_pro_list, get_conf_list, get_category_list

api = Redprint("capture")


@api.route("/user_list", methods=["GET"])
def user_list():
    """
    用户列表
    """
    user_list = User.get_login_user_list()
    return Sucess(data=user_list)


@api.route("/pro_list", methods=["GET"])
def pro_list():
    """
    项目列表
    """
    pro_list_info = get_pro_list()
    return Sucess(data=pro_list_info)


@api.route("/<int:pro_id>/conf_list", methods=["GET"])
def conf_list(pro_id):
    """
    配置列表
    """
    pro_list_info = get_conf_list(pro_id)
    return Sucess(data=pro_list_info)


@api.route("/<int:pro_id>/category", methods=["GET"])
def category_list(pro_id):
    """
    分类列表
    """
    category_list_info = get_category_list(pro_id)
    return Sucess(data=category_list_info)


@api.route("/upload", methods=["POST"])
def upload_api():
    """
    配置列表
    """
    return Sucess()
