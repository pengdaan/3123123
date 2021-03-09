#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :tasksRun.py
@说明        :task 执行方法
@时间        :2020/08/19 14:47:27
@作者        :Leo
@版本        :1.0
"""
from app.libs import run
from app.models.case import Case
from app.models.case_detail import Case_Detail
from app.models.case_module import CaseModule
from app.models.config import Config
from app.models.tasks import ScheduledTasks as Task


def task_caseList(caseList, user_id):
    case_lists = Case.get_all_case_by_caseList(caseList)
    data = {"data": case_lists, "executor": int(user_id)}
    tasks_list = []
    if len(data["data"]) > 0:
        for req in data["data"]:
            executor = req["user_id"] if req["user_id"] != "" else None
            caseDetail = Case_Detail.get_case_detail(req["case_id"])
            case = Case.query.filter_by(id=req["case_id"]).first()
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
                config = Config.query.filter_by(id=req["config_id"]).first()
                if config:
                    host = None
                    config = eval(config.body)
                    summary = run.debug_api(
                        case_list,
                        req["pro_id"],
                        case_id=req["case_id"],
                        config=run.parse_host(host, config),
                        status=1,
                        run_type=None,
                        name=case.case_name,
                        executor=executor,
                    )
                    if isinstance(summary, int):
                        case_tasks_id = Task.add_case_tasks(
                            case_id=req["case_id"], case_status=1, summary=summary
                        )
                        tasks_list.append(str(case_tasks_id))
                    else:
                        case_tasks_id = Task.add_case_tasks(
                            case_id=req["case_id"],
                            case_status=0,
                            summary=summary["msg"],
                        )
                        tasks_list.append(str(case_tasks_id))
                else:
                    case_tasks_id = Task.add_case_tasks(
                        case_id=req["case_id"], case_status=0, summary="项目配置不存在，请检查"
                    )
                    tasks_list.append(str(case_tasks_id))
            else:
                case_tasks_id = Task.add_case_tasks(
                    case_id=req["case_id"], case_status=0, summary="用例数量为空，请检查"
                )
                tasks_list.append(str(case_tasks_id))
        tasks_detail = ",".join(tasks_list)
        projet_taskId = Task.add_project_tasks(
            pro_id=req["pro_id"],
            executor=data["executor"],
            count=len(data["data"]),
            tasks_detail=tasks_detail,
        )
        Task.get_project_tasks_detail(projet_taskId.id)
        return projet_taskId.id


def task_project(project_id, user_id):
    case_lists = Case.get_all_case_by_project(project_id)
    data = {"data": case_lists, "executor": int(user_id)}
    tasks_list = []
    if len(data["data"]) > 0:
        for req in data["data"]:
            executor = req["user_id"] if req["user_id"] != "" else None
            caseDetail = Case_Detail.get_case_detail(req["case_id"])
            case = Case.query.filter_by(id=req["case_id"]).first()
            case_list = []
            if len(caseDetail) > 0:
                for i in caseDetail:
                    print(i)
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
                config = Config.query.filter_by(id=req["config_id"]).first()
                if config:
                    host = None
                    config = eval(config.body)
                    summary = run.debug_api(
                        case_list,
                        req["pro_id"],
                        case_id=req["case_id"],
                        config=run.parse_host(host, config),
                        status=1,
                        run_type=None,
                        name=case.case_name,
                        executor=executor,
                    )
                    if isinstance(summary, int):
                        case_tasks_id = Task.add_case_tasks(
                            case_id=req["case_id"], case_status=1, summary=summary
                        )
                        tasks_list.append(str(case_tasks_id))
                    else:
                        case_tasks_id = Task.add_case_tasks(
                            case_id=req["case_id"],
                            case_status=0,
                            summary=summary["msg"],
                        )
                        tasks_list.append(str(case_tasks_id))
                else:
                    case_tasks_id = Task.add_case_tasks(
                        case_id=req["case_id"], case_status=0, summary="项目配置不存在，请检查"
                    )
                    tasks_list.append(str(case_tasks_id))
            else:
                case_tasks_id = Task.add_case_tasks(
                    case_id=req["case_id"], case_status=0, summary="用例数量为空，请检查"
                )
                tasks_list.append(str(case_tasks_id))
        tasks_detail = ",".join(tasks_list)
        projet_taskId = Task.add_project_tasks(
            pro_id=req["pro_id"],
            executor=data["executor"],
            count=len(data["data"]),
            tasks_detail=tasks_detail,
        )
        return projet_taskId.id
