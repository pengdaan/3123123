#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :_add_api.py
@说明        :
@时间        :2021/04/01 11:24:16
@作者        :Leo
@版本        :1.0
'''

from sqlalchemy import text

from app.libs.tools_func import serialize_sqlalchemy_obj
from app.models.base import db
from app.models.api import Api


def add_api(name, path, method, pro_id, cat_id):
    is_api = Api.query.filter_by(path=path).first()
    if not is_api:
        api_info = Api.add_api(name, method, path, pro_id, cat_id, 1)
        api_id = api_info.id
    else:
        api_id = is_api.id
    return api_id



