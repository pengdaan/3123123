#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :PlanRun.py
@说明        :
@时间        :2020/12/04 10:40:53
@作者        :Leo
@版本        :1.0
"""

from app.libs import run
from app.models.case import Case
from app.models.case_detail import Case_Detail
from app.models.case_module import CaseModule
from app.models.config import Config
from app.models.parameter import Parameters
from app.models.plan import Plan
from app.models.plan_detail import PlanDetail
from app.models.plan_report_merge import planReportMerge


def run_plan_by_user(PlanId, user_id):
    PlanInfo = Plan.query.filter_by(id=PlanId).first_or_404("PlanId")
    if PlanInfo.case_list != "":
        caseList = PlanInfo.case_list.split(",")
        plan_run = Case.get_all_case_by_caseList(caseList)
        plan_data = {"plan_run_list": plan_run, "executor": int(user_id)}
        print("plan_data", plan_data)
        # 进入执行中状态
        Plan.update_isStatus(PlanId, 2)

        tasks_list = []
        if len(plan_data["plan_run_list"]) > 0:
            for planCase in plan_data["plan_run_list"]:
                executor = planCase["user_id"] if planCase["user_id"] != "" else None
                caseDetail = Case_Detail.get_case_detail(planCase["case_id"])
                case = Case.query.filter_by(id=planCase["case_id"]).first()
                case_list = []
                if len(caseDetail) > 0:
                    for i in caseDetail:
                        baseData = CaseModule.query.filter_by(id=i.module_id).first()
                        if baseData.sql_config_id:
                            body_detail = eval(baseData.body)
                            body_detail["request"]["json"]["id"] = int(
                                baseData.sql_config_id
                            )
                            body_detail["request"]["json"]["other_config_id"] = int(
                                baseData.other_config_id
                            )
                        else:
                            body_detail = eval(baseData.body)
                        case_list.append(body_detail)
                    config = Config.query.filter_by(id=case["config_id"]).first()
                    if config:
                        host = None
                        config = eval(config.body)
                        parameters = Parameters.query.filter_by(
                            case_id=planCase["case_id"]
                        ).first()
                        if parameters:
                            this_parameters = eval(parameters.parameters)["parameters"]
                            config["parameters"] = this_parameters
                        apiList = []
                        cases = Case_Detail.query.filter_by(
                            case_id=planCase["case_id"]
                        ).all()
                        for i in cases:
                            apiList.append(i.api_id)
                        summary = run.debug_api(
                            apiList,
                            case_list,
                            planCase["pro_id"],
                            case_id=planCase["case_id"],
                            config=run.parse_host(host, config),
                            status=1,
                            run_type=None,
                            name=case.case_name,
                            executor=executor,
                        )
                        if isinstance(summary, int):
                            case_tasks_id = PlanDetail.add_plan_detail(
                                case_id=planCase["case_id"],
                                case_status=1,
                                summary=summary,
                            )
                            tasks_list.append(str(case_tasks_id))
                        else:
                            case_tasks_id = PlanDetail.add_plan_detail(
                                case_id=planCase["case_id"],
                                case_status=0,
                                summary=summary["msg"],
                            )
                            tasks_list.append(str(case_tasks_id))
                            Plan.update_isStatus(PlanId, 4)
                    else:
                        case_tasks_id = PlanDetail.add_plan_detail(
                            case_id=planCase["case_id"],
                            case_status=0,
                            summary="项目配置不存在，请检查",
                        )
                        tasks_list.append(str(case_tasks_id))
                        Plan.update_isStatus(PlanId, 4)
                else:
                    case_tasks_id = PlanDetail.add_plan_detail(
                        case_id=planCase["case_id"], case_status=0, summary="用例数量为空，请检查"
                    )
                    tasks_list.append(str(case_tasks_id))
                    Plan.update_isStatus(PlanId, 4)
        tasks_detail = ",".join(tasks_list)
        planReportMerge.add_planReportMerge(PlanId, tasks_detail, user_id)
        Plan.update_isStatus(PlanId, 3)
    else:
        return None
