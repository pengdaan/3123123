#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :parameters.py
@说明        :
@时间        :2020/10/16 15:53:44
@作者        :Leo
@版本        :1.0
"""

import json
from app.libs.auth import auth_jwt
from app.libs.code import Sucess
from app.libs.redprint import Redprint
from app.models.parameter import Parameters
from app.validators.parameter_validator import ParametersForm, updateParametersForm

api = Redprint("parameters")


@api.route("/add", methods=["POST"])
@auth_jwt
def add_parameters():
    """[summary]
    添加数据驱动
    """
    parameters_info = ParametersForm().validate_for_api()
    key_is_exist = Parameters.key_is_exist(
        parameters_info.case_id.data, parameters_info.key.data
    )
    if key_is_exist:
        return Sucess(data="key: " + parameters_info.key.data + "已存在")
    else:
        Parameters.add_parameters(
            parameters_info.case_id.data,
            parameters_info.key.data,
            parameters_info.parameters.data,
        )
    return Sucess()


@api.route("/update", methods=["POST"])
@auth_jwt
def update_parameters():
    """[summary]
    更新数据驱动
    """
    parameters_info = updateParametersForm().validate_for_api()
    key_is_exist = Parameters.key_is_exist(
        parameters_info.case_id.data, parameters_info.key.data, parameters_info.id.data
    )
    if key_is_exist:
        return Sucess(data="key: " + parameters_info.key.data + "已存在")
    else:
        Parameters.update_parameters(
            parameters_info.id.data,
            parameters_info.key.data,
            parameters_info.parameters.data,
        )
        return Sucess()


@api.route("/detail", methods=["POST"])
@auth_jwt
def parameters_detail():
    """[summary]
    获取Case数据驱动详情
    """
    parameter_lists = []
    caseId = ParametersForm().validate_for_api()
    parameters = Parameters.query.filter_by(case_id=caseId.case_id.data).all()
    if parameters:
        for i in parameters:
            parameters_info = json.loads(i.parameters)
            parameter_data = parameters_info["parameters"][0]
            descs = parameters_info["desc"]
            (desc,) = descs.values()
            (key,) = parameter_data
            (value,) = parameter_data.values()
            parameter = {
                "id": i.id,
                "key": key,
                "value": value,
                "desc": desc,
                "status": i.status,
            }
            parameter_lists.append(parameter)
    return Sucess(data=parameter_lists)


@api.route("/<int:id>/status", methods=["GET"])
@auth_jwt
def update_parameters_status(id):
    """[summary]
    更新parameters状态
    """
    parameter_info = Parameters.query.filter_by(id=id).first()
    if parameter_info.status == 1:
        Parameters.update_parameters_status(id, 0)
    else:
        Parameters.update_parameters_status(id, 1)
    return Sucess()


@api.route("/<int:id>/del", methods=["GET"])
@auth_jwt
def del_parameters(id):
    """[summary]
    删除parameters
    """
    Parameters.del_parameters(id)
    return Sucess()
