#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :PlanRun.py
@说明        :
@时间        :2020/12/04 10:40:53
@作者        :Leo
@版本        :1.0
"""
import requests
from app.libs import run
from app.models.case import Case
from app.models.case_detail import Case_Detail
from app.models.case_module import CaseModule
from app.models.config import Config
from app.models.parameter import Parameters
from app.models.plan import Plan
from app.models.plan_detail import PlanDetail
from app.models.plan_report_merge import planReportMerge
from app.models.task import ScheduledTask as Task


def run_plan_by_user(PlanId, user_id, task_id=None):
    PlanInfo = Plan.query.filter_by(id=PlanId).first_or_404("PlanId")
    if PlanInfo.case_list != "":
        caseList = PlanInfo.case_list.split(",")
        plan_run = Case.get_all_case_by_caseList(caseList)
        plan_data = {"plan_run_list": plan_run, "executor": int(user_id)}
        # print("plan_data", plan_data)
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
        planReport_merge_info = planReportMerge.add_planReportMerge(
            PlanId, tasks_detail, user_id
        )
        Plan.update_isStatus(PlanId, 3)
        if task_id:
            Task_info = Task.query.filter_by(id=task_id).first()
            if Task_info:
                plan_name = Task_info.name
                url = Task_info.robot
                headers = {"Content-Type": "text/plain"}
                plan_report_detail_list = (
                    planReport_merge_info.plan_report_detail.split(",")
                )
                report_ids = []
                if plan_report_detail_list:
                    for i in plan_report_detail_list:
                        plan_detail_info = PlanDetail.query.filter_by(id=i).first()
                        if plan_detail_info.case_status == 1:
                            report_ids.append(plan_detail_info.summary)
                        else:
                            data = {
                                "msgtype": "markdown",  # 消息类型，此时固定为markdown
                                "markdown": {
                                    "content": "#### **提醒！luna 实时反馈**\n"
                                    + "> "  # 标题 （支持1至6级标题，注意#与文字中间要有空格）
                                    + " **请相关同事注意，及时跟进！**\n"
                                    + "> "  # 加粗：**需要加粗的字**
                                    + '> 类型：<font color="info">定时任务</font> \n'
                                    + '> 计划名称：<font color="info">{0}</font> \n'.format(  # 引用：> 需要引用的文字
                                        plan_name
                                    )
                                    + '> 结果: <font color="warning">执行失败</font>\n'  # 引用：> 需要引用的文字
                                    + '> 错误信息：<font color="comment">{0}</font>\n'.format(
                                        plan_detail_info.summary
                                    )  # 字体颜色(只支持3种内置颜色)
                                },
                            }
                            requests.post(url, headers=headers, json=data)
                            break
                    if report_ids:
                        new_report_ids = [str(x) for x in report_ids]
                        report_data = ",".join(new_report_ids)
                        plan_report_url = "http://127.0.0.1:5000/api/1/report/suite?report_ids={0}".format(
                            report_data
                        )
                        send_data = {
                            "msgtype": "markdown",  # 消息类型，此时固定为markdown
                            "markdown": {
                                "content": "#### **提醒！luna 实时反馈**\n\n\n\n\n\n"
                                + "> "  # 标题 （支持1至6级标题，注意#与文字中间要有空格）
                                + " **请相关同事注意，及时跟进！**\n"
                                + "> "  # 加粗：**需要加粗的字**
                                + '> 类型：<font color="info">定时任务</font> \n'
                                + '> 计划名称：<font color="info">{0}</font> \n'.format(  # 引用：> 需要引用的文字
                                    plan_name
                                )
                                + '> 结果: <font color="info">执行成功</font>\n'  # 引用：> 需要引用的文字
                                + "> 测试报告：请点击：[查看报告详情]({0}) \n".format(
                                    plan_report_url
                                )  # 字体颜色(只支持3种内置颜色)
                            },
                        }
                        requests.post(url, headers=headers, json=send_data)
    else:
        return None
