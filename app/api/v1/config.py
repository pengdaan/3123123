#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :config.py
@说明        :
@时间        :2020/08/14 15:43:18
@作者        :Leo
@版本        :1.0
"""

from flask import request
from app.libs.code import Sucess

from app.libs.auth import auth_jwt
from app.libs.parser import Format, Parse
from app.libs.redprint import Redprint
from app.models.case import Case
from app.models.config import Config
from app.models.project import Project
from app.validators.config_validator import (
    addConfigForm,
    searchConfigForm,
    updateConfigForm,
)

api = Redprint("config")


@api.route("/add", methods=["POST"])
@auth_jwt
def add_config():
    """
    新增config。[暂时不做拆分，body存储格式和原来一致]
    :return:
    """
    configData = addConfigForm().validate_for_api()
    config = Format(configData.data, level="config")
    config.parse()
    Config.add_config(
        config.name,
        str(config.testcase),
        config.base_url,
        configData.pro_id.data,
        configData.type.data,
    )
    return Sucess()


@api.route("/get_case/<int:id>", methods=["GET"])
@auth_jwt
def get_case_config_list(id):
    """
    根据id查询配置下是否有case
    :param id:
    :return:
    """
    case_list = Case.query.filter_by(config_id=id).all()
    if case_list:
        data = case_list
    else:
        data = []
    return Sucess(data=data)


@api.route("/del/<int:id>", methods=["GET"])
@auth_jwt
def del_config(id):
    """
    根据id删除配置
    :param id:
    :return:
    """
    Config.query.filter_by(id=id).first_or_404("configId")
    Config.del_config(id)
    return Sucess()


@api.route("/detail/<int:id>", methods=["GET"])
@auth_jwt
def config_detail(id):
    """
    根据id获取配置详情
    :param id:
    :return:
    """
    configInfo = Config.query.filter_by(id=id).first_or_404("configId")
    parse = Parse(eval(configInfo.body), level="config")
    parse.parse_http()
    result = {
        "name": configInfo.name,
        "body": parse.testcase,
        "base_url": configInfo.base_url,
        "type": configInfo.type,
    }
    return Sucess(data=result)


@api.route("/update", methods=["POST"])
@auth_jwt
def update_config():
    """
    更新config
    :return:
    """
    configData = updateConfigForm().validate_for_api()
    config = Format(configData.data.data, level="config")
    config.parse()
    Config.update_config(
        configData.id.data,
        config.name,
        str(config.testcase),
        config.base_url,
        configData.type.data,
    )
    return Sucess()


@api.route("/list/<int:pro_id>", methods=["GET"])
@auth_jwt
def get_pro_config_list(pro_id):
    """
    根据项目id 获取配置列表
    :param pro_id:
    :return:
    """
    Project.query.filter_by(id=pro_id).first_or_404("proId")
    if "type" in request.args:
        type = request.args.get("type")
    else:
        type = None
    result = Config.config_list(pro_id, type)
    return Sucess(data=result)


@api.route("/search", methods=["POST"])
@auth_jwt
def search_pro_config_detail():
    """
    查询配置
    :param pro_id:
    :return:
    """
    configInfo = searchConfigForm().validate_for_api()
    Project.query.filter_by(id=configInfo.pro_id.data).first_or_404("proId")
    if not configInfo.kw.data:
        result = Config.search_config_list(configInfo.pro_id.data, None)
    else:
        result = Config.search_config_list(configInfo.pro_id.data, configInfo.kw.data)
    return Sucess(data=result)
