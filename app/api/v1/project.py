#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :project.py
@说明        :项目管理类api
@时间        :2020/08/11 09:13:30
@作者        :Leo
@版本        :1.0
"""

from app.libs.auth import auth_jwt
from app.libs.hook_code import (
    BASE_CODE_HOOK_SETUP,
    BASE_CODE_HOOK_SQL,
    BASE_CODE_HOOK_TEARDOWN,
)
from app.libs.code import Sucess
from app.libs.redprint import Redprint
from app.models.api import Api
from app.models.case import Case
from app.models.category import Category
from app.models.hook import Hook
from app.models.module import Module
from app.models.project import Project
from app.models.tag import Case_Tag
from app.models.config import Config
from app.constants import base_sql_config
from app.validators.project_validator import (
    addProjectForm,
    searchProjectForm,
    updateProjectForm,
)

api = Redprint("project")


@auth_jwt
@api.route("/add", methods=["POST"])
def add_project():
    """
    新增项目
    :return:
    """
    form = addProjectForm().validate_for_api()
    isProject = Project.query.filter_by(
        project_name=form.project_name.data, status=0
    ).first()
    if isProject:
        Project.update_project(isProject.id, form.project_name.data, form.desc.data)
        ProId = isProject.id
    else:
        projectInfo = Project.add_project(
            form.project_name.data, form.desc.data, form.user_id.data
        )
        categoryInfo = Category.add_category("公共分类", projectInfo.id)
        ApiInfo = Api.add_api(
            "数据库查询", "POST", "/api/1/sql/connect", projectInfo.id, categoryInfo.id, 2
        )
        Hook.add_hook(
            projectInfo.id, BASE_CODE_HOOK_SQL, "数据库函数demo", "create", ApiInfo.id
        )
        Hook.add_hook(
            projectInfo.id, BASE_CODE_HOOK_SETUP, "API 执行前，前置条件设置", "hook_setup"
        )
        Hook.add_hook(
            projectInfo.id, BASE_CODE_HOOK_TEARDOWN, "API 执行后，后置条件设置", "hook_teardown"
        )
        Config.add_config(
            "数据库访问配置",
            base_sql_config.CONFIG_BODY,
            base_sql_config.SQL_URL,
            projectInfo.id,
            2
            )
        Case_Tag.add_ca_tag("API用例", projectInfo.id)
        projectInfo.hide("user_detail")
        ProId = projectInfo.id
    data = {"pro_id": ProId}
    return Sucess(data=data)


@api.route("/update", methods=["POST"])
@auth_jwt
def update_project():
    """
    更新项目
    :return:
    """
    form = updateProjectForm().validate_for_api()
    Project.update_project(form.project_id.data, form.project_name.data, form.desc.data)
    return Sucess(msg="更新成功")


@api.route("/del/<int:id>", methods=["DELETE"])
@auth_jwt
def del_project(id):
    """
    删除项目
    :return:
    """
    Project.query.filter_by(id=id).first_or_404("project")
    Project.del_project(id)
    return Sucess(msg="项目删除成功")


@api.route("/detail/<int:id>", methods=["GET"])
@auth_jwt
def get_project_detail(id):
    """
    获取项目详情
    :return:
    """
    res = Project.query.filter_by(id=id).first_or_404("project_name")
    api_count = Api.query.filter_by(pro_id=id).count()
    result = {
        "id": res.id,
        "project_name": res.project_name,
        "desc": res.desc,
        "api_count": api_count,
    }
    return Sucess(data=result)


@api.route("/list", methods=["GET"])
@auth_jwt
def get_project_list():
    """
    获取项目列表
    :return:
    """
    result = Project.query.filter_by(status=1).order_by(Project.id.desc()).all()
    project_list = []
    for i in result:
        api_count = Api.query.filter_by(pro_id=i.id, status=1).count()
        case_count = Case.query.filter_by(pro_id=i.id, status=1).count()
        author = i.user_detail["username"]
        project = {
            "id": i.id,
            "project_name": i.project_name,
            "desc": i.desc,
            "api_count": api_count,
            "case_count": case_count,
            "author": author,
        }
        project_list.append(project)
    return Sucess(data=project_list)


@api.route("/<int:pro_id>/<int:page>", methods=["GET"])
@auth_jwt
def project_api_list_by_id(pro_id, page):
    """
    获取单个项目下的api列表
    :return:
    """
    result = {}
    api_lists = []
    if page == 1:
        res = (
            Api.query.filter_by(pro_id=pro_id, status=1)
            .order_by(Api.create_time.desc())
            .limit(10)
            .offset(0)
            .all()
        )
    else:
        page = int(page - 1) * 10
        res = (
            Api.query.filter_by(pro_id=pro_id, status=1)
            .order_by(Api.create_time.desc())
            .limit(10)
            .offset(page)
            .all()
        )
    count = Api.query.filter_by(pro_id=pro_id, status=1).count()
    if len(res) > 0:
        for i in res:
            category = Category.query.filter_by(id=i.cat_id, status=1).first()
            targetModule = Module.query.filter_by(api_id=i.id, status=1).all()
            modules = []
            if targetModule:
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


@api.route("/dashboard", methods=["GET"])
@auth_jwt
def tasks_dashboard_list():
    """[summary]
    首页仪表盘数据获取
    """
    project_count = Project.query.count()
    api_count = Api.query.count()
    case_count = Case.query.count()
    res = {
        "project_count": project_count,
        "api_count": api_count,
        "case_count": case_count,
    }
    return Sucess(data=res)


@api.route("/search", methods=["POST"])
@auth_jwt
def search_pro_detail():
    """
    查询项目
    :param pro_id:
    :return:
    """
    SearchProInfo = searchProjectForm().validate_for_api()
    result = Project.query.filter(
        Project.project_name.like("%{0}%".format(SearchProInfo.kw.data))
    ).all()
    project_list = []
    for i in result:
        api_count = Api.query.filter_by(pro_id=i.id, status=1).count()
        case_count = Case.query.filter_by(pro_id=i.id, status=1).count()
        author = i.user_detail["username"]
        project = {
            "id": i.id,
            "project_name": i.project_name,
            "desc": i.desc,
            "api_count": api_count,
            "case_count": case_count,
            "author": author,
        }
        project_list.append(project)
    return Sucess(data=project_list)
