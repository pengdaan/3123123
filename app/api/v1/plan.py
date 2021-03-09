#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :plan.py
@说明        :
@时间        :2020/12/03 15:32:11
@作者        :Leo
@版本        :1.0
"""

from flask import jsonify

from app.libs.plan_run import run_plan_by_user
from app.libs.redprint import Redprint
from app.models.plan import Plan
from app.models.plan_report_merge import planReportMerge
from app.models.user import User
from app.libs.code import Sucess
from app.register.executor import executor
from app.validators.plan_validator import (
    PlanBaseForm,
    UpdatePlanCaseForm,
    UpdatePlanisTasksForm,
)

api = Redprint("plan")


@api.route("/list/<int:proId>/<int:page>", methods=["GET"])
def plan_list(proId, page):
    # 获取计划列表
    res = {}
    count = Plan.query.filter_by(pro_id=proId, status=1).count()
    if page == 1:
        result = Plan.query.filter_by(pro_id=proId).limit(10).offset(0).all()
    else:
        page = int(page - 1) * 10
        result = Plan.query.filter_by(pro_id=proId).limit(10).offset(page).all()
    plan_list = []
    for i in result:
        data = {
            "id": i.id,
            "name": i.name,
            "desc": i.desc,
            "user": i.executor_detail.username,
            "case_list": i.case_list,
            "isTasks": i.isTasks,
            "status": i.status,
            "update_time": i.update_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        plan_list.append(data)
    res["planList"] = plan_list
    res["total"] = count
    return Sucess(data=res)


@api.route("/add", methods=["POST"])
def add_plan_list():
    # 添加计划
    PlanData = PlanBaseForm().validate_for_api()
    if PlanData.id.data:
        Plan.update_project_plan(
            PlanData.id.data, PlanData.name.data, PlanData.desc.data
        )
        return jsonify({"code": 0, "data": {"id": PlanData.id.data}, "msg": "success"})
    else:
        PlanInfo = Plan.add_project_plan(
            PlanData.pro_id.data,
            PlanData.name.data,
            PlanData.executor.data,
            PlanData.desc.data,
        )
        return Sucess(data={"id": PlanInfo.id})


@api.route("/addCase", methods=["POST"])
def add_plan_case():
    # 添加case
    planCaseData = UpdatePlanCaseForm().validate_for_api()
    caseList = ",".join("%s" % id for id in planCaseData.case_list.data)
    Plan.update_planCaseList(planCaseData.id.data, caseList)
    return Sucess()


@api.route("/updatePlan", methods=["POST"])
def update_plan_is_tasks():
    # 变更计划的执行状态
    planIsTasks = UpdatePlanisTasksForm().validate_for_api()
    Plan.update_isTasks(planIsTasks.id.data, planIsTasks.isTasks.data)
    return Sucess()


@api.route("/run/<int:planId>/<int:userId>", methods=["GET"])
def run_plan(planId, userId):
    """
    异步执行计划任务[plan]
    :return:
    """
    # run_plan(planId, userId)
    executor.submit(run_plan_by_user, planId, userId)
    return Sucess(msg="Tasks joined successfully, please wait for the result")


@api.route("/run/project/<int:proId>", methods=["GET"])
def run_project_plan(proId):
    """
    异步执行计划任务[project]
    :return:
    """
    userInfo = User.query.filter_by(username="admin").first_or_404("UserId 不存在")
    pro_plan_list = Plan.query.filter_by(pro_id=proId, isTasks=1).all()
    for i in pro_plan_list:
        executor.submit(run_plan_by_user, i.id, userInfo.id)
    return Sucess(msg="Tasks joined successfully, please wait for the result")


@api.route("/status/<int:proId>", methods=["GET"])
def get_project_status(proId):
    StatusList = []
    StatusInfo = Plan.query.filter_by(pro_id=proId).all()
    if StatusInfo:
        for i in StatusInfo:
            data = {"id": i.id, "status": i.status}
            StatusList.append(data)
    return Sucess(data=StatusList)


@api.route("/stop/<int:planId>", methods=["GET"])
def stop_plan(planId):
    Plan.update_isStatus(planId, 3)
    return Sucess()


@api.route("/report/list/<int:planId>/<int:Page>", methods=["GET"])
def report_plan_list(planId, Page):
    ReportInfo = planReportMerge.get_planReportMerge(planId, Page)
    return Sucess(data=ReportInfo)


@api.route("/del/<int:id>", methods=["get"])
def del_plan_case(id):
    # 删除计划
    Plan.del_plan(id)
    return Sucess()
