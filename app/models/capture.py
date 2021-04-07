#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :capture.py
@说明        :
@时间        :2021/03/29 15:23:06
@作者        :Leo
@版本        :1.0
'''

from sqlalchemy import text

from app.libs.tools_func import serialize_sqlalchemy_obj
from app.models.base import db


def get_pro_list():
    projects = "select id,project_name from project;"
    pro_list = db.session.execute(text(projects)).fetchall()
    pro_list_info = serialize_sqlalchemy_obj(pro_list)
    return pro_list_info


def get_conf_list(pro_id):
    configs = "select id,name from config where pro_id=:pro_id and type =1;"
    fonf_list = db.session.execute(text(configs), {"pro_id": pro_id}).fetchall()
    fonf_list_info = serialize_sqlalchemy_obj(fonf_list)
    return fonf_list_info


def get_category_list(pro_id):
    category = "select id,category_name from category where pro_id=:pro_id;"
    category_list = db.session.execute(text(category), {"pro_id": pro_id}).fetchall()
    category_list_info = serialize_sqlalchemy_obj(category_list)
    return category_list_info



