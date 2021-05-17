#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :case.py
@说明        :
@时间        :2020/08/13 14:09:11
@作者        :Leo
@版本        :1.0
"""

from flask import g

from app.libs import run
from app.libs.auth import auth_jwt
from app.libs.code import Sucess
from app.libs.parser import Format, Parse
from app.libs.redprint import Redprint
from app.models.case import Case
from app.models.case_detail import Case_Detail
from app.models.case_module import CaseModule
from app.models.config import Config
from app.models.parameter import Parameters
from app.models.sqlconfig import Sql_Config
from app.models.user import User
from app.register.wsIO import socketio
from app.libs.func_name import get_func_name

from app.validators.case_validator import (
    CaseForm,
    CaseRunForm,
    DebugCaseForm,
    SetupForm,
    UpdateCaseForm,
    CopyCaseForm
)
from app.validators.case_detail_validator import (
    UpdateCaseSetup,
    addCaseDetail,
    delCaseDetail,
)

api = Redprint("case")


@api.route("/add", methods=["POST"])
@auth_jwt
def add_case():
    """
    添加case
    :return:
    """
    caseData = CaseForm().validate_for_api()
    caseInfo = Case.add_Case(
        caseData.pro_id.data,
        caseData.case_name.data,
        caseData.user_id.data,
        caseData.config_id.data,
        caseData.desc.data,
        caseData.tag_id.data,
    )
    return Sucess(data=caseInfo.id)


@api.route("/update", methods=["POST"])
@auth_jwt
def update_case():
    """
    更新case
    :return:
    """
    caseData = UpdateCaseForm().validate_for_api()
    Case.update_Case(
        caseData.id.data,
        caseData.pro_id.data,
        caseData.case_name.data,
        caseData.config_id.data,
        caseData.tag_id.data,
        caseData.desc.data,
    )
    return Sucess(data={"case_id": caseData.id.data})


@api.route("/<int:pro_id>/<int:page>", methods=["GET"])
@auth_jwt
def get_all_case(pro_id, page):
    """
    获取case_list
    :param pro_id:
    :return:
    """
    res = {}
    count = Case.query.filter_by(pro_id=pro_id, status=1).count()
    if page == 1:
        result = Case.query.filter_by(pro_id=pro_id, status=1).limit(10).offset(0).all()
    else:
        page = int(page - 1) * 10
        result = Case.query.filter_by(pro_id=pro_id).limit(10).offset(page).all()
    case_list = []
    for i in result:
        case_detail = []
        for n in i.case_details:
            data = {"case_detail_id": n.id, "path": n.path, "setup": n.setup}
            case_detail.append(data)
        userDetail = User.query.filter_by(id=i.user_id).first_or_404("user")
        config_detail = Config.query.filter_by(id=i.config_id).first_or_404("ConfigId")
        case = {
            "id": i.id,
            "case_name": i.case_name,
            "desc": i.desc if i.desc is not None else "暂无描述",
            "config_detail": {"id": i.config_id, "name": config_detail.name},
            "tag_detail": {"id": i.tag_detail.id, "name": i.tag_detail.tag_name}
            if i.tag_detail
            else {"id": "", "name": ""},
            "pro_id": i.pro_id,
            "case_detail": case_detail,
            "apiCount": len(case_detail),
            "user_detail": {"id": i.user_id, "user_name": userDetail.username},
            "update_time": i.update_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        case_list.append(case)
    res["caseList"] = case_list
    res["total"] = count
    return Sucess(data=res)


@api.route("/del/<int:case_id>", methods=["DELETE"])
@auth_jwt
def del_case(case_id):
    """
    删除case
    :param pro_id:
    :return:
    """
    Case.query.filter_by(id=case_id, status=1).first_or_404("Case")
    Case.del_case(case_id)
    return Sucess()


@api.route("/detail/<int:case_id>", methods=["GET"])
@auth_jwt
def get_case_detail(case_id):
    """
    获取单个case详情
    :param pro_id:
    :return:
    """
    Case.query.filter_by(id=case_id, status=1).first_or_404("Case")
    res = Case.get_Case_detail(case_id)
    if res["case_detail"]:
        for i in res["case_detail"]:
            modules = CaseModule.query.filter_by(
                id=i["module_id"], status=1
            ).first_or_404("caseModule")
            parse = Parse(eval(modules.body))
            parse.parse_http()
            if modules.sql_config_id:
                sqlConfigDetail = Sql_Config.query.filter_by(
                    id=modules.sql_config_id, status=1
                ).first_or_404("caseModule")
                api_type = 2
                sql_name = sqlConfigDetail.name
            else:
                api_type = 1
                sql_name = None
            if modules.other_config_id:
                configDetail = Config.query.filter_by(
                    id=modules.other_config_id, status=1
                ).first_or_404("caseModule")
                config_id = modules.other_config_id
                config_name = configDetail.name
            else:
                config_id = None
                config_name = None
            i["type"] = api_type
            i["sql_config_detail"] = {
                "sql_config_id": modules.sql_config_id,
                "sql_config_name": sql_name,
            }
            i["config_detail"] = {"config_id": config_id, "config_name": config_name}
            result = {
                "id": i["api_id"],
                "case_detail_id": case_id,
                "body": parse.testcase,
                "module_id": modules.id,
            }
            module_detail = {
                "current_module": {
                    "name": modules.name,
                    "user_id": modules.user_id,
                    "detail": result,
                },
                "other_module": [],
            }
            i["module_detail"] = module_detail
    return Sucess(data=res)


@api.route("/find/<int:tag_id>/<int:page>", methods=["GET"])
@auth_jwt
def find_case_by_tag(tag_id, page):
    """
    获取case_list
    :param pro_id:
    :return:
    """
    res = {}
    count = Case.query.filter_by(tag_id=tag_id, status=1).count()
    if page == 1:
        result = Case.query.filter_by(tag_id=tag_id, status=1).limit(10).offset(0).all()
    else:
        page = int(page - 1) * 10
        result = Case.query.filter_by(tag_id=tag_id).limit(10).offset(page).all()
    case_list = []
    for i in result:
        case_detail = []
        for n in i.case_details:
            data = {"case_detail_id": n.id, "path": n.path, "setup": n.setup}
            case_detail.append(data)
        userDetail = User.query.filter_by(id=i.user_id).first_or_404("user")
        config_detail = Config.query.filter_by(id=i.config_id).first_or_404("ConfigId")
        case = {
            "id": i.id,
            "case_name": i.case_name,
            "desc": i.desc if i.desc is not None else "暂无描述",
            "config_detail": {"id": i.config_id, "name": config_detail.name},
            "tag_detail": {"id": i.tag_detail.id, "name": i.tag_detail.tag_name}
            if i.tag_detail
            else {"id": "", "name": ""},
            "pro_id": i.pro_id,
            "case_detail": case_detail,
            "apiCount": len(case_detail),
            "user_detail": {"id": i.user_id, "user_name": userDetail.username},
            "update_time": i.update_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        case_list.append(case)
    res["caseList"] = case_list
    res["total"] = count
    return Sucess(data=res)


@api.route("/detail/del", methods=["POST"])
@auth_jwt
def del_case_detail():
    """
    删除case中的api
    :return:
    """
    caseData = delCaseDetail().validate_for_api()
    Case_Detail.del_case_detail(caseData.id.data, caseData.case_id.data)
    CaseModule.del_case_module(caseData.module_id.data)
    return Sucess()


@api.route("/detail/add", methods=["POST"])
@auth_jwt
def add_case_detail():
    """
    case添加module
    :return:
    """
    addData = addCaseDetail().validate_for_api()
    api = Format(addData.case_api.data)
    api.parse()
    func_name = get_func_name(api.testcase)
    if addData.id.data:
        CaseModule.update_module(
            addData.id.data,
            api.testcase["name"],
            str(api.testcase),
            addData.other_config_id.data,
            func_name,
            addData.sql_config_id.data,
        )
        CaseDetailInfo = Case_Detail.query.filter_by(
            case_id=addData.case_id.data,
            module_id=addData.id.data,
            api_id=addData.api_id.data,
        ).first()
        res = {
            "case_detail_id": CaseDetailInfo.id,
            "module_id": addData.id.data,
        }
        return Sucess(data=res)
    else:
        modules = CaseModule.add_api_module(
            addData.name.data,
            str(api.testcase),
            addData.case_id.data,
            addData.user_id.data,
            addData.other_config_id.data,
            func_name,
            addData.sql_config_id.data,
        )
        CaseDetailInfo = Case_Detail.add_case_detail(
            addData.name.data,
            modules.id,
            addData.path.data,
            addData.setup.data,
            addData.case_id.data,
            addData.api_id.data,
        )
        return Sucess(
            data={
                "case_detail_id": CaseDetailInfo.id,
                "module_id": modules.id,
            }
        )


@api.route("/module/detail/<int:id>", methods=["GET"])
@auth_jwt
def get_case_module_detail_by_id(id):
    """
    获取单个case_model的详情
    :return:
    """
    api = CaseModule.query.filter_by(id=id).first_or_404("CaseModule")
    parse = Parse(eval(api.body))
    parse.parse_http()
    res = {
        "id": api.id,
        "body": parse.testcase,
    }
    return Sucess(data=res)


@api.route("/module/detail/setup", methods=["POST"])
@auth_jwt
def update_case_setup():
    """
    [旧]更新case中api的执行顺序,现主要用于更新name
    :return:
    """
    caseData = UpdateCaseSetup().validate_for_api()
    CaseDetails = Case_Detail.query.filter_by(id=caseData.id.data).first_or_404(
        "CaseDetailId"
    )
    Case_Detail.case_detail_update_setup(
        caseData.id.name, caseData.setup.data, caseData.name.data
    )
    module_id = CaseDetails.id
    module_detail = CaseModule.query.filter_by(id=module_id).first_or_404(
        "CaseModuleId"
    )
    if module_detail.name != caseData.name.data:
        module_body = eval(module_detail.body)
        module_body["name"] = caseData.name.data
        CaseModule.update_module_name(module_id, caseData.name.data, str(module_body))
    return Sucess()


@api.route("/run", methods=["POST"])
@auth_jwt
def run_case():
    """
    运行case
    :return:
    """
    uid = g.user
    caseData = CaseRunForm().validate_for_api()
    caseDetail = Case_Detail.get_case_detail(caseData.case_id.data)
    case = Case.query.filter_by(id=caseData.case_id.data).first_or_404("caseId")
    case_list = []
    if caseDetail:
        for i in caseDetail:
            baseData = CaseModule.query.filter_by(
                id=i.module_id, status=1
            ).first_or_404("CaseModuleId")
            if baseData.sql_config_id:
                body_detail = eval(baseData.body)
                body_detail["request"]["json"]["id"] = int(baseData.sql_config_id)
                body_detail["request"]["json"]["other_config_id"] = int(
                    baseData.other_config_id
                )
            else:
                body_detail = eval(baseData.body)
            case_list.append(body_detail)
        config = Config.query.filter_by(
            id=caseData.config_id.data, status=1
        ).first_or_404("ConfigId")
        host = None
        config = eval(config.body)
        summary = run.debug_api(
            case_list,
            caseData.pro_id.data,
            case_id=caseData.case_id.data,
            config=run.parse_host(host, config),
            status=1,
            run_type=None,
            name=case.case_name,
            executor=uid,
        )
        if isinstance(summary, int):
            return Sucess(data=summary)
        else:
            return Sucess(data=summary)
    else:
        return Sucess(data={"status": True, "msg": "Case不存在用例"})


@api.route("/debug", methods=["POST"])
@auth_jwt
def debug_case():
    """
    debug_case
    传入：
        case_id : 用于获取到case下的公参
        module_id: 获取项目的body
        config_id: 获取项目的配置
    :return:
    """
    caseData = DebugCaseForm().validate_for_api()
    apiList = []
    for i in caseData.module_list.data:
        api_id = (Case_Detail.query.filter_by(module_id=i).first()).api_id
        apiList.append(api_id)
    case_list = []
    for i in caseData.module_list.data:
        baseData = CaseModule.query.filter_by(id=int(i)).first_or_404("CaseModuleId")
        if baseData.sql_config_id:
            body_detail = eval(baseData.body)
            body_detail["request"]["json"]["id"] = int(baseData.sql_config_id)
            body_detail["request"]["json"]["other_config_id"] = int(
                baseData.other_config_id
            )
        else:
            body_detail = eval(baseData.body)
        case_list.append(body_detail)
    config = Config.query.filter_by(id=caseData.config_id.data).first_or_404("ConfigId")
    host = None
    config = eval(config.body)
    parameters = Parameters.query.filter_by(case_id=caseData.case_id.data).first()
    if parameters:
        this_parameters = eval(parameters.parameters)["parameters"]
        config["parameters"] = this_parameters
    summary = run.debug_api(
        apiList,
        case_list,
        caseData.pro_id.data,
        case_id=caseData.case_id.data,
        config=run.parse_host(host, config),
        status=1,
        run_type=1,
    )
    return Sucess(data=summary)


@api.route("/module/detail/setups", methods=["POST"])
@auth_jwt
def update_setups():
    """
    更新case的执行顺序
    :return:
    """
    caseData = SetupForm().validate_for_api()
    Case_Detail.case_detail_update_setups(caseData.setups.data)
    return Sucess()


@socketio.on("connect", namespace="/ws")
def test_connect():
    # sid = request.sid
    socketio.emit("server_response", {"data": "socket连接成功."}, namespace="/ws")


@socketio.on_error_default
# 监听某个事件，以及事件的参数
def default_error_handler(e):
    pass
    # Luna.logger.info(request.event["message"],request.event["args"])
    # print(request.event["message"])  # "my error event"
    # print(request.event["args"])  # (data,)


@socketio.on("run", namespace="/ws")
def case_run_by_socket(req):
    executor = req["user_id"] if req["user_id"] != "" else None
    caseDetail = Case_Detail.get_case_detail(req["case_id"])
    case = Case.query.filter_by(id=req["case_id"]).first_or_404("caseId")
    case_list = []
    if caseDetail:
        for i in caseDetail:
            baseData = CaseModule.query.filter_by(id=i.module_id).first()
            if baseData.sql_config_id:
                body_detail = eval(baseData.body)
                body_detail["request"]["json"]["id"] = int(baseData.sql_config_id)
                body_detail["request"]["json"]["other_config_id"] = int(
                    baseData.other_config_id
                )
            else:
                body_detail = eval(baseData.body)
            case_list.append(body_detail)
        config = Config.query.filter_by(id=req["config_id"]).first()
        if config:
            host = None
            config = eval(config.body)
            # parameters = Parameters.query.filter_by(case_id=req["case_id"]).first()
            apiList = []
            cases = Case_Detail.query.filter_by(case_id=req["case_id"]).all()
            for i in cases:
                apiList.append(i.api_id)
            # if parameters:
            #     this_parameters = eval(parameters.parameters)["parameters"]
            #     config["parameters"] = this_parameters
            summary = run.debug_api(
                apiList,
                case_list,
                req["pro_id"],
                case_id=req["case_id"],
                config=run.parse_host(host, config),
                status=1,
                run_type=None,
                name=case.case_name,
                executor=executor,
            )
            socketio.sleep(3)
            if isinstance(summary, int):
                result_data = {"summary": summary, "case_id": req["case_id"]}
                socketio.emit(
                    "server_response",
                    {"code": 0, "data": result_data, "msg": "Report添加成功"},
                    namespace="/ws",
                )
            else:
                socketio.emit(
                    "server_response",
                    {
                        "code": 3002,
                        "data": {"summary": summary["msg"], "case_id": req["case_id"]},
                        "msg": "Case运行错误: " + summary["msg"],
                    },
                    namespace="/ws",
                )
                exit()
        else:
            socketio.emit(
                "server_response",
                {
                    "code": 3003,
                    "data": {"summary": "", "case_id": req["case_id"]},
                    "msg": "该配置不存在",
                },
                namespace="/ws",
            )
    else:
        socketio.emit(
            "server_response",
            {
                "code": 3004,
                "data": {"summary": "", "case_id": req["case_id"]},
                "msg": "Case不存在用例",
            },
            namespace="/ws",
        )


@api.route('/copy', methods=["POST"])
@auth_jwt
def copy_case():
    req = CopyCaseForm().validate_for_api()
    case_module = CaseModule.query.filter_by(case_id=req.id.data).all()
    new_case = Case.copy_case(req.id.data, req.user_id.data, req.case_name.data)
    for i in case_module:
        case_detail = Case_Detail.query.filter_by(module_id=i.id).first()
        new_case_module = CaseModule.add_api_module(i.name, i.body, new_case.id, req.user_id.data, i.other_config_id, i.func_name, i.sql_config_id)
        Case_Detail.add_case_detail(case_detail.name, new_case_module.id, case_detail.path, case_detail.setup, new_case.id, case_detail.api_id)
    return Sucess()