#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :variable.py
@说明        :
@时间        :2021/04/20 17:23:35
@作者        :Leo
@版本        :1.0
'''

from app.libs.auth import auth_jwt
from flask import request
from app.libs.code import Sucess, Fail
from app.libs.redprint import Redprint
from app.models.variable import Variable
from app.validators.variable_validator import AddVariableForm, UpdateVariableForm, VariableListForm, DelVariableListForm

api = Redprint("variable")


@api.route('/add', methods=["POST"])
# @auth_jwt
def add_variable():
    res = AddVariableForm().validate_for_api()
    target_variable = Variable.query.filter_by(name=res.variable_name.data, pro_id=res.pro_id.data).first()
    if target_variable:
        Variable.update_variable_status(target_variable.id, 1, "", res.variable_name.data)
        return Sucess(data={"id": target_variable.id, "status": 1})
    else:
        variableInfo = Variable.add_variable(res.variable_name.data, res.case_id.data, res.pro_id.data, res.api_id.data, res.module_id.data, res.case_module_id.data)
        return Sucess(data={"id": variableInfo.id, "status": variableInfo.status})


@api.route('/update', methods=["POST"])
# @auth_jwt
def update_variable():
    res = UpdateVariableForm().validate_for_api()
    Variable.update_variable_status(res.id.data, res.status.data, "", res.variable_name.data)
    return Sucess(data={"id": res.id.data, "status": res.status.data})


@api.route('/<int:pro_id>/list', methods=["POST"])
# @auth_jwt
def variable_list(pro_id):
    res = VariableListForm().validate_for_api()
    if res.api_id.data:
        res = Variable.get_variable_list(pro_id=pro_id, api_id=res.api_id.data)
    elif res.case_id.data:
        res = Variable.get_variable_list(pro_id=pro_id, case_id=res.case_id.data)
    else:
        res = Variable.get_variable_list(pro_id)
    return Sucess(data={"variable_list": res})


@api.route('/del', methods=["POST"])
# @auth_jwt
def del_variable():
    res = DelVariableListForm().validate_for_api()
    isVariable = Variable.get_variable(res.variable_name.data)
    if len(isVariable["apis_detail"]) > 0 and len(isVariable['cases_detail']) > 0:
        return Fail(data=isVariable, msg="该变量正在用例/api场景中使用")
    else:
        Variable.del_variable(res.variable_id.data)
        return Sucess()
