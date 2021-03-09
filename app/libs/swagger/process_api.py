#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :processApi.py
@说明        :swagger转httprunner API录入
@时间        :2020/11/13 10:30:07
@作者        :Leo
@版本        :1.0
"""
from app.models.api import Api
from app.models.module import Module


def get_swagger_api_name(data):
    if isinstance(data, dict):
        return data["name"]
    else:
        return None


def get_swagger_api_url(data):
    if isinstance(data, dict):
        return data["request"]["url"]
    else:
        return None


def get_swagger_api_body(data):
    if isinstance(data, dict):
        data["times"] = 1
        data["skipUnless"] = True
        desc = {"variables": {}, "extract": {}, "params": {}, "data": {}}
        desc["header"] = data["request"]["headers"]
        if data["request"].get("params"):
            for p in data["request"]["params"].keys():
                desc["params"].update({p: ""})
        if data["request"].get("data"):
            for d in data["request"]["data"].keys():
                desc["data"].update({d: ""})
        if data["request"].get("json"):
            for j in data["request"]["json"].keys():
                desc["data"].update({j: ""})

        data["desc"] = desc
        data.pop("validate")
        return data
    else:
        return None


def get_swagger_Api(path, name, pro_id, method, cat_id):
    """[summary]
    获取项目下的ApiId

    Args:
        path ([type]): [description]
        name ([type]): [description]
        pro_id ([type]): [description]
        method ([type]): [description]
        cat_id ([type]): [description]

    Returns:
        [type]: [description]
    """
    ApiInfo = Api.query.filter_by(path=path, cat_id=cat_id, status=1).first()
    if not ApiInfo:
        ApiInfo = Api.add_api(name, method, path, pro_id, cat_id, 1)
    return ApiInfo.id


def add_swagger_Api_by_module(api_id, body, user_id, name="基础模版", api_type=1):
    """[summary]
    添加api模版
    api_type:1 全量更新
    api_type:2 智能更新

    Args:
        api_id ([type]): [description]
        body ([type]): [description]
        user_id ([type]): [description]
        name (str, optional): [description]. Defaults to "基础模版".
    """
    ModuleInfo = Module.query.filter_by(
        name=name, api_id=api_id, user_id=user_id
    ).first()
    if api_type == 1:
        if ModuleInfo:
            Module.update_module(ModuleInfo.id, name, body, sql_config_id=None)
        else:
            Module.add_api_module(name, body, api_id, user_id, sql_config_id=None)
    else:
        if not ModuleInfo:
            Module.add_api_module(name, body, api_id, user_id, sql_config_id=None)
