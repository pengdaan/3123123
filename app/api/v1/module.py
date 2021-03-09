#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :module.py
@说明        :
@时间        :2020/08/14 15:43:38
@作者        :Leo
@版本        :1.0
"""

from flask import g
from app.libs.code import Sucess

from app.libs.auth import auth_jwt
from app.libs.func_name import get_func_name
from app.libs.parser import Format, Parse
from app.libs.redprint import Redprint
from app.models.module import Module
from app.models.sqlconfig import Sql_Config
from app.validators.module_validator import (
    ModuleForm,
    copyModuleForm,
    searchModuleForm,
    updateModuleForm,
    updateModuleNameForm,
)

api = Redprint("module")


@api.route("/add", methods=["POST"])
@auth_jwt
def add_module():
    """
    新增module
    :return:
    """
    uid = g.user
    moduleData = ModuleForm().validate_for_api()
    api = Format(moduleData.body.data)
    api.parse()
    ModuleInfo = Module.query.filter_by(
        name=moduleData.name.data, api_id=moduleData.api_id.data, user_id=uid, status=1
    ).first()
    if not ModuleInfo:
        addModule = Module.add_api_module(
            moduleData.name.data,
            str(api.testcase),
            moduleData.api_id.data,
            uid,
        )
        return Sucess(data=addModule.id)
    else:
        return Sucess(data=addModule.id, msg="该模块已存在")


@api.route("/del/<int:id>", methods=["GET"])
@auth_jwt
def del_module(id):
    Module.query.filter_by(id=id, status=1).first_or_404("ModuleId")
    Module.del_module(id)
    return Sucess()


@api.route("/search", methods=["POST"])
@auth_jwt
def search_module():
    """
    [暂时还没用到]根据关键字/用户id 查询
    {"key":"zzz","api_id":1,"user_id":1}
    :key 选填
    :user_id 选填
    :return:
    """
    moduleData = searchModuleForm().validate_for_api()
    if moduleData.key.data:
        res = Module.get_api_modules_by_key(moduleData.api_id.data, moduleData.key.id)
    if moduleData.user_id.data:
        res = Module.get_api_modules_by_user_id(
            moduleData.api_id.data, moduleData.user_id.data
        )
    else:
        res = Module.get_api_modules(moduleData.api_id.data, status=1)
    return Sucess(data=res)


@api.route("/detail/<int:id>")
@auth_jwt
def get_api_module_detail(id):
    """
    获取单个model的详情
    :return:
    """
    apiInfo = Module.query.filter_by(id=id, status=1).first_or_404("ModuleId")
    parse = Parse(eval(apiInfo.body))
    parse.parse_http()
    if apiInfo.sql_config_id:
        sqlConfigDetail = Sql_Config.get_sql_config_by_id(apiInfo.sql_config_id)
        sql_config_id = apiInfo.sql_config_id
        sql_name = sqlConfigDetail.name
    else:
        sql_config_id = 0
        sql_name = None
    res = {
        "id": apiInfo.id,
        "body": parse.testcase,
        "sql_config_detail": {
            "sql_config_id": sql_config_id,
            "sql_config_name": sql_name,
        },
    }
    return Sucess(data=res)


@api.route("/update", methods=["POST"])
@auth_jwt
def update_module():
    """
    修改用户模版
    :return:
    """
    moduleData = updateModuleForm().validate_for_api()
    api = Format(moduleData.body.data)
    api.parse()
    func_name = get_func_name(api.testcase)
    api_body = {
        "name": api.name,
        "body": api.testcase,
        "url": api.url,
        "method": api.method,
    }
    if isinstance(moduleData.sql_config_id.data, int):
        Module.update_module(
            moduleData.id.data,
            api_body["name"],
            str(api_body["body"]),
            func_name,
            moduleData.sql_config_id.data,
        )
    else:
        Module.update_module(
            moduleData.id.data,
            api_body["name"],
            str(api_body["body"]),
            func_name,
            sql_config_id=None,
        )
    return Sucess()


@api.route("/copy", methods=["POST"])
@auth_jwt
def copy_api_module():
    """[summary]
    复制api内的module，生成新的module

    Returns:
        [type] -- [description]
    """
    moduleData = copyModuleForm().validate_for_api()
    copy_module_detail = Module.query.filter_by(
        id=moduleData.copy_id.data, status=1
    ).first_or_404("ModuleId")
    module_detail = Module.query.filter_by(
        id=moduleData.id.data, status=1
    ).first_or_404("ModuleDetailId")
    Module.update_module(
        moduleData.id.data,
        module_detail.name,
        copy_module_detail.body,
        copy_module_detail.sql_config_id,
    )
    return Sucess()


@api.route("/update/name", methods=["POST"])
@auth_jwt
def update_module_name():
    """[summary]
    修改api内的moduleName

    Returns:
        [type] -- [description]
    """
    uid = g.user
    moduleData = updateModuleNameForm().validate_for_api()

    module_detail = Module.query.filter_by(
        id=moduleData.id.data, user_id=uid, name=moduleData.name.data
    ).first()
    if not module_detail:
        Module.update_module_name(moduleData.id.data, moduleData.name.data)
        return Sucess()
    else:
        return Sucess(msg="场景不存在")
