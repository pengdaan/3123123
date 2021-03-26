#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :hook.py
@说明        :
@时间        :2020/08/14 15:43:28
@作者        :Leo
@版本        :1.0
"""

from app.libs.auth import auth_jwt
from app.libs.code import Sucess, Fail
from app.libs.redprint import Redprint
from app.libs.code_run import DebugCode
from app.models.api import Api
from app.models.hook import Hook
from app.validators.hook_validator import (
    AddHookForm,
    DelHookForm,
    UpdateHookForm,
)

api = Redprint("hook")


@api.route("/tree/<int:pro_id>", methods=["GET"])
@auth_jwt
def hook_tree(pro_id):
    """
    获取项目下的hook Tree
    :return:
    """
    hook_list = []
    Hook_Api_Info = (
        Hook.query.with_entities(Hook.api_id).filter_by(pro_id=pro_id).distinct().all()
    )
    if Hook_Api_Info:
        for i in Hook_Api_Info:
            if i.api_id:
                Api_info = Api.query.filter_by(id=i.api_id).first()
                label = Api_info.name
            else:
                label = "公共函数"
            Hook_Info = Hook.query.filter_by(pro_id=pro_id, api_id=i.api_id).all()
            children = []
            if Hook_Info:
                for i in Hook_Info:
                    children.append({"label": i.fun_name, "id": i.id, "desc": i.desc})
            hook_detail = {"api_id": i.api_id, "label": label, "children": children}
            hook_list.append(hook_detail)
    return Sucess(data=hook_list)


@api.route("/getProList/<int:pro_id>/<int:page>", methods=["GET"])
@auth_jwt
def hook_list(pro_id, page):
    """
    获取项目下的hook 列表
    :return:
    """
    if page == 1:
        offset_id = 0
    else:
        offset_id = int(page - 1) * 10
    hook_list = []
    Hook_Info = (
        Hook.query.filter_by(pro_id=pro_id)
        .order_by(Hook.create_time.desc())
        .limit(10)
        .offset(offset_id)
        .all()
    )
    count = Hook.query.filter_by(pro_id=pro_id).count()
    if Hook_Info:
        for i in Hook_Info:
            if i.api_id:
                Api_info = Api.query.filter_by(id=i.api_id).first()
                api_name = Api_info.name
            else:
                api_name = "公共函数"
            data = {
                "id": i.id,
                "func_name": i.fun_name,
                "api_id": i.api_id,
                "api_name": api_name,
                "desc": i.desc,
                "pro_id": i.pro_id,
            }
            hook_list.append(data)
    res = {"hook_list": hook_list, "count": count}
    return Sucess(data=res)


@api.route("/getApiList/<int:api_id>/<int:page>", methods=["GET"])
@auth_jwt
def api_hook_list(api_id, page):
    """
    获取项目下的hook 列表
    :return:
    """
    if page == 1:
        offset_id = 0
    else:
        offset_id = int(page - 1) * 10
    hook_list = []
    Apis_Info = (
        Hook.query.filter_by(api_id=api_id)
        .order_by(Hook.create_time.desc())
        .limit(10)
        .offset(offset_id)
        .all()
    )
    count = Hook.query.filter_by(api_id=api_id).count()
    if Apis_Info:
        for i in Apis_Info:
            if i.api_id:
                Api_info = Api.query.filter_by(id=i.api_id).first()
                api_name = Api_info.name
            else:
                api_name = "公共函数"
            data = {
                "id": i.id,
                "func_name": i.fun_name,
                "api_id": i.api_id,
                "api_name": api_name,
                "desc": i.desc,
                "pro_id": i.pro_id,
            }
            hook_list.append(data)
    res = {"hook_list": hook_list, "count": count}
    return Sucess(data=res)


@api.route("/<int:pro_id>/apilist", methods=["GET"])
@auth_jwt
def hook_api_list(pro_id):
    """
    获取项目下的hook 的api列表
    :return:
    """
    api_list = []
    BASE_API = {"id": "", "name": "公共函数"}
    apis = Api.query.filter_by(pro_id=pro_id).all()
    if apis:
        for i in apis:
            data = {"id": i.id, "name": i.name}
            api_list.append(data)
    api_list.append(BASE_API)
    return Sucess(data={"api_list": api_list})


@api.route("/add", methods=["POST"])
@auth_jwt
def add_hook():
    hookData = AddHookForm().validate_for_api()
    is_exist = Hook.query.filter_by(
        pro_id=hookData.pro_id.data, fun_name=hookData.fun_name.data
    ).all()
    if is_exist:
        return Sucess(code=40001, msg="函数已存在,请重命名！")
    else:
        hook_info = Hook.add_hook(
            hookData.pro_id.data,
            hookData.code.data,
            hookData.desc.data,
            hookData.fun_name.data,
            hookData.api_id.data,
        )
        return Sucess(data=hook_info.id)


@api.route("/update", methods=["POST"])
@auth_jwt
def update_hook():
    hookData = UpdateHookForm().validate_for_api()
    is_exist = (
        Hook.query.filter_by(
            pro_id=hookData.pro_id.data, fun_name=hookData.fun_name.data
        )
        .filter(Hook.id != hookData.id.data)
        .all()
    )
    if len(is_exist) > 0:
        return Sucess(code=40001, msg="函数已存在,请重命名！")
    else:
        Hook.update_Hook(
            hookData.id.data,
            hookData.code.data,
            hookData.desc.data,
            hookData.fun_name.data,
            hookData.api_id.data,
        )
        return Sucess(data=hookData.id.data)


@api.route("/detail/<int:id>", methods=["GET"])
@auth_jwt
def get_hook_detail(id):
    """
    获取项目的hook代码详情
    :param pro_id:
    :return:
    """
    data = Hook.query.filter_by(id=id).first_or_404("hook")
    if data.api_id:
        api_info = Api.query.filter_by(id=data.api_id).first()
        api_name = api_info.name
    else:
        api_name = "公共函数"
    res = {
        "project_id": data.pro_id,
        "api_id": data.api_id,
        "api_name": api_name,
        "code": data.code,
        "desc": data.desc,
        "id": data.id,
    }
    return Sucess(data=res)


@api.route("/detail/api/<int:api_id>", methods=["GET"])
@auth_jwt
def get_hook_api_detail(api_id):
    """
    获取api的hook代码详情
    :param pro_id:
    :return:
    """
    CodeInfo = Hook.query.filter_by(api_id=api_id).first()
    if CodeInfo:
        code = CodeInfo.code
    else:
        code = ""
    res = {"code": code}
    return Sucess(data={"hook_list": res})


@api.route("/update", methods=["POST"])
@auth_jwt
def update_hook_detail():
    """
    更新项目的hook代码详情
    :param pro_id:
    :return:
    """
    hookData = AddHookForm().validate_for_api()
    Hook.update_Hook(hookData.pro_id.data, hookData.code.data, hookData.fun_name.data)
    return Sucess()


@api.route("/debug", methods=["POST"])
@auth_jwt
def debug_hook_coode():
    """
    在线调试hook代码
    :return:
    """
    debug_code = ""
    hookData = AddHookForm().validate_for_api()
    if hookData.id.data is None:
        is_exist = Hook.query.filter_by(
            pro_id=hookData.pro_id.data, fun_name=hookData.fun_name.data
        ).all()
    else:
        is_exist = Hook.order_by_hook_id(
            pro_id=hookData.pro_id.data,
            fun_name=hookData.fun_name.data,
            id=hookData.id.data,
        )
    if is_exist:
        return Sucess(code=40001, msg="函数已存在,请重命名！")
    else:
        public_code = (
            Hook.query.filter_by(pro_id=hookData.pro_id.data, api_id=None)
            .filter(Hook.id != hookData.id.data)
            .all()
        )
        if public_code:
            for i in public_code:
                debug_code = debug_code + i.code
        if hookData.api_id.data is not None:
            api_code = (
                Hook.query.filter_by(
                    pro_id=hookData.pro_id.data, api_id=hookData.api_id.data
                )
                .filter(Hook.id != hookData.id.data)
                .all()
            )
            if api_code:
                for i in api_code:
                    debug_code = debug_code + i.code
        debug_code = debug_code + hookData.code.data
        debug = DebugCode(debug_code)
        # print(debug_code)
        debug.run()
        return Sucess(data=debug.resp)


@api.route("/del", methods=["POST"])
# @auth_jwt
def del_hook():
    """
    删除hook
    :return:
    """
    delData = DelHookForm().validate_for_api()
    case_is_activite = Hook._hook_is_activite_by_case(
        delData.func_name.data, delData.pro_id.data
    )
    if delData.api_id.data is not None:
        api_is_activite = Hook._hook_is_activite_by_api(
            delData.func_name.data, api_id=delData.api_id.data, pro_id=None
        )
    else:
        api_is_activite = Hook._hook_is_activite_by_api(
            delData.func_name.data, api_id=None, pro_id=delData.pro_id.data
        )
    if len(case_is_activite) > 0 or len(api_is_activite) > 0:
        print('api_is_activite',api_is_activite)
        all_is_activite = api_is_activite + case_is_activite
        return Fail(data=all_is_activite, msg="删除失败,该函数在api或case中正在使用") 
    else:

        Hook.del_hook(delData.id.data)
        return Sucess()
