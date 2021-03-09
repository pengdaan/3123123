#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :task.py
@说明        :
@时间        :2020/08/14 15:44:06
@作者        :Leo
@版本        :1.0
"""

from flask import request
from app.libs.code import Sucess

from app.libs.redprint import Redprint
from app.libs.tasks_run import task_caseList, task_project
from app.models.project import Project
from app.models.report import Report
from app.models.tasks import ScheduledTasks as Task
from app.register.executor import executor
from app.validators.task_validator import TasksForm

api = Redprint("task")


@api.route("/project/list/<int:page>", methods=["GET"])
def tasks_project_list(page):
    """
    放在task里面[project环境不符合]
    获取tasks项目列表
    :return:
    """
    res = Project.get_tasks_project(page)
    return Sucess(data=res)


@api.route("/list/<int:page>", methods=["GET"])
def get_project_task_list(page):
    """[summary]
    获取项目的task列表

    Args:
        page ([type]): [description]

    Returns:
        [type]: [description]
    """
    res = Task.get_project_tasks_list(page, kw=None)
    return Sucess(data=res)


@api.route("/search", methods=["POST"])
def search_project_task_list():
    """[summary]
    搜索查询task
    Returns:
        [type]: [description]
    """
    taskData = TasksForm().validate_for_api()
    res = Task.get_project_tasks_list(taskData.page.data, taskData.kw.data)
    return Sucess(data=res)


@api.route("/del/<int:task_id>", methods=["GET"])
def del_project_task(task_id):
    """[summary]
    删除task
    Args:
        task_id ([type]): [description]

    Returns:
        [type]: [description]
    """
    task_detail = Task.query.filter_by(id=task_id).first_or_404("taskId")
    task_detail_list = task_detail.tasks_detail.split(",")
    Task.del_tasks_detail(task_detail_list)
    Task.del_project_tasks(task_id)
    return Sucess()


@api.route("/detail/<int:task_id>", methods=["GET"])
def get_task_detail(task_id):
    """[summary]
    获取task的执行详情
    Args:
        task_id ([type]): [description]

    Returns:
        [type]: [description]
    """
    Task.query.filter_by(id=task_id).first_or_404("taskId")
    task_detail = Task.get_project_tasks_detail(task_id)
    return Sucess(data=task_detail)


@api.route("/project", methods=["GET"])
def tasks_project():
    """
    异步执行计划任务
    :return:
    """
    user_id = request.args.get("user_id")
    project_id = request.args.get("project_id")
    case_list = request.args.get("case_list")
    if project_id:
        executor.submit(task_project, project_id, user_id)
    if case_list:
        this_case_list = case_list.split(",")
        executor.submit(task_caseList, this_case_list, user_id)
    return Sucess(msg="Tasks joined successfully, please wait for the result")


@api.route("/count", methods=["GET"])
def tasks_count():
    """
    获取task的执行情况
    """
    TaskresultList = Report.get_report_count()
    return Sucess(data=TaskresultList)
