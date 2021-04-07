#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :api.py
@说明        :
@时间        :2020/08/12 09:43:54
@作者        :Leo
@版本        :1.0
"""

from app.libs import run
from app.libs.auth import auth_jwt
from app.libs.code import Sucess
from app.libs.parser import Format
from app.libs.redprint import Redprint
from app.models.api import Api
from app.models.category import Category
from app.models.config import Config
from app.models.module import Module
from app.models.sqlconfig import Sql_Config
from app.validators.api_validator import FindApiForm, addApiForm, updateApiForm
from app.validators.run_validator import DebugForm, RunForm

api = Redprint("interface")


@api.route("/add", methods=["POST"])
@auth_jwt
def add_api():
    """
    添加api
    {
        "pro_id":"82",
        "name":"测试",
        "path":"/baidu.com",
        "method":"GET",
        "cat_id":250,
        "type":"1"
    }
    """
    form = addApiForm().validate_for_api()
    apiInfo = Api.add_api(
        form.name.data,
        form.method.data,
        form.path.data,
        form.pro_id.data,
        form.cat_id.data,
        form.type.data,
    )
    return Sucess(data={"id": apiInfo.id})


@api.route("/del/<int:id>", methods=["DELETE"])
@auth_jwt
def del_api(id):
    """
    删除api
    :param id:
    :return:
    """
    Api.query.filter_by(id=id, status=1).first_or_404("apiId")
    Api.del_api(id)
    return Sucess()


@api.route("/detail/<int:id>", methods=["GET"])
@auth_jwt
def get_api_detail(id):
    """
    获取api 详情
    :param id:
    :return:
    """
    result = Api.query.filter_by(id=id, status=1).first()
    if result:
        modules = []
        apiOfModules = Module.query.filter_by(api_id=id).all()
        if apiOfModules:
            for i in apiOfModules:
                if i.sql_config_id:
                    sqlConfigDetail = Sql_Config.query.filter_by(
                        id=i.sql_config_id, status=1
                    ).first_or_404("sqlConfigId")
                    sql_config_id = i.sql_config_id
                    sql_name = sqlConfigDetail.name
                else:
                    sql_config_id = 0
                    sql_name = None
                data = {
                    "module_id": i.id,
                    "name": i.name,
                    "body": i.body,
                    "api_id": i.api_id,
                    "user_id": i.user_id,
                    "sql_config_detail": {
                        "sql_config_id": sql_config_id,
                        "sql_config_name": sql_name,
                    },
                }
                modules.append(data)
        category_name = Category.query.filter_by(
            id=result.cat_id, status=1
        ).first_or_404("apiId")
        res = {
            "id": result.id,
            "name": result.name,
            "path": result.path,
            "method": result.method,
            "pro_id": result.pro_id,
            "cat_id": result.cat_id,
            "type": str(result.type),
            "cat_name": category_name,
            "modules_detail": modules,
        }
        return Sucess(data=res)
    else:
        return Sucess(msg="Api 不存在")


@api.route("/update", methods=["POST"])
@auth_jwt
def update_api():
    """
    更新api内容
    :return:
    """
    modlueList = []
    apiData = updateApiForm().validate_for_api()
    modlueDetails = Module.query.filter_by(api_id=apiData.id.data).all()
    if modlueDetails:
        for i in modlueDetails:
            modlueList.append(i.id)
    Api.update_api(
        apiData.id.data,
        apiData.name.data,
        apiData.method.data,
        apiData.path.data,
        apiData.cat_id.data,
        apiData.type.data,
    )
    return Sucess()


@api.route("/run", methods=["POST"])
@auth_jwt
def api_run():
    """
    单个api运行
    :return:
    """
    runData = RunForm().validate_for_api()
    apiOfrun = Api.query.filter_by(id=runData.id.data).first_or_404("apiId")
    module = Module.query.filter_by(id=runData.module_id.data).first_or_404("moduleId")
    type = apiOfrun.type
    if type == 2:
        sql_config = module.sql_config_id
        apiOfbody = eval(module.body)
        apiOfbody["request"]["json"]["id"] = int(sql_config)
    else:
        apiOfbody = eval(module.body)
    config = Config.query.filter_by(id=runData.config_id.data).first_or_404("configId")
    # 不做host的配置处理，暂时冗余host字段
    host = None
    apis = [runData.id.data]
    summary = run.debug_api(
        apis,
        apiOfbody,
        apiOfrun.pro_id,
        case_id=None,
        config=run.parse_host(host, eval(config.body)),
    )
    return Sucess(data=summary)


@api.route("/debug", methods=["POST"])
@auth_jwt
def debug_api():
    """
    调试模式
    :return:
    """
    debugData = DebugForm().validate_for_api()
    api = Format(debugData.body.data)
    api.parse()
    config = Config.query.filter_by(id=debugData.config_id.data).first_or_404(
        "configId"
    )
    if debugData.sql_config_id.data != 0:
        api.testcase["request"]["json"]["id"] = int(debugData.sql_config_id.data)
        test_case = eval(str(api.testcase))
    else:
        test_case = eval(str(api.testcase))
    # 不做host的配置处理，暂时冗余host字段
    host = None
    summary = run.debug_api(
        apiIds=debugData.api_id.data,
        api=test_case,
        project=debugData.pro_id.data,
        case_id=None,
        config=run.parse_host(host, eval(config.body)),
    )
    return Sucess(data=summary)


@api.route("/find", methods=["POST"])
@auth_jwt
def FindApi():
    """
    查询
    :return:
    """
    # 通过api名称模糊查询，
    # 通过分类查询
    result = {}
    api_lists = []
    apiData = FindApiForm().validate_for_api()
    if apiData.page.data == 1:
        if apiData.cateId.data:
            count = (
                Api.query.filter_by(
                    pro_id=apiData.proId.data, cat_id=apiData.cateId.data, status=1
                )
                .filter(
                    Api.name.like("%" + str(apiData.name.data) + "%")
                    if apiData.name.data is not None
                    else ""
                )
                .count()
            )
            res = (
                Api.query.filter_by(
                    pro_id=apiData.proId.data, cat_id=apiData.cateId.data, status=1
                )
                .filter(
                    Api.name.like("%" + str(apiData.name.data) + "%")
                    if apiData.name.data is not None
                    else ""
                )
                .order_by(Api.create_time.desc())
                .limit(10)
                .offset(0)
                .all()
            )
        else:
            count = (
                Api.query.filter_by(pro_id=apiData.proId.data, status=1)
                .filter(
                    Api.name.like("%" + apiData.name.data + "%")
                    if apiData.name.data is not None
                    else ""
                )
                .count()
            )
            res = (
                Api.query.filter_by(pro_id=apiData.proId.data, status=1)
                .filter(
                    Api.name.like("%" + apiData.name.data + "%")
                    if apiData.name.data is not None
                    else ""
                )
                .order_by(Api.create_time.desc())
                .limit(10)
                .offset(0)
                .all()
            )
    else:
        page = int(apiData.page.data - 1) * 10
        if apiData.cateId.data != "":
            count = (
                Api.query.filter_by(
                    pro_id=apiData.proId.data, cat_id=apiData.cateId.data, status=1
                )
                .filter(
                    Api.name.like("%" + str(apiData.name.data) + "%")
                    if apiData.name.data is not None
                    else ""
                )
                .count()
            )
            res = (
                Api.query.filter_by(
                    pro_id=apiData.proId.data, cat_id=apiData.cateId.data, status=1
                )
                .filter(
                    Api.name.like("%" + str(apiData.name.data) + "%")
                    if apiData.name.data is not None
                    else ""
                )
                .order_by(Api.create_time.desc())
                .limit(10)
                .offset(page)
                .all()
            )
        else:
            count = (
                Api.query.filter_by(pro_id=apiData.proId.data, status=1)
                .filter(
                    Api.name.like("%" + apiData.name.data + "%")
                    if apiData.name.data is not None
                    else ""
                )
                .count()
            )
            res = (
                Api.query.filter_by(pro_id=apiData.proId.data, status=1)
                .filter(
                    Api.name.like("%" + apiData.name.data + "%")
                    if apiData.name.data is not None
                    else ""
                )
                .order_by(Api.create_time.desc())
                .limit(10)
                .offset(page)
                .all()
            )
    if res:
        for i in res:
            category = Category.query.filter_by(id=i.cat_id, status=1).first()
            targetModule = Module.query.filter_by(api_id=i.id, status=1).all()
            modules = []
            if len(targetModule) > 0:
                for m in targetModule:
                    module_detail = {"id": m.id, "name": m.name}
                    modules.append(module_detail)
            category_detail = {"id": i.cat_id, "name": category.category_name}

            data = {
                "id": i.id,
                "name": i.name,
                "path": i.path,
                "type": i.type,
                "method": i.method,
                "category_detail": category_detail,
                "module_detail": modules,
                "create_time": i.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            api_lists.append(data)
    result["api_list"] = api_lists
    result["total"] = count
    return Sucess(data=result)
