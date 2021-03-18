#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :task.py
@说明        :
@时间        :2020/08/14 15:44:06
@作者        :Leo
@版本        :1.0
"""
import requests
from app.libs.code import Sucess, Fail
import json
from app.libs.redprint import Redprint
from app.models.task import ScheduledTask as Task
from app.register.scheduler import scheduler
from app.models.report import Report
from datetime import datetime
from app.validators.task_validator import TaskForm, addTaskForm, updateTaskForm
from app.libs.auth import auth_jwt

api = Redprint("task")


@api.route("/add", methods=["POST"])
@auth_jwt
def add_task():
    """[summary]
        添加计划任务:
        # 一次性任务
        {
            "plan_id":13,
            "run_time": "2021-3-10 17:41:00",
            "type": "date",
            "robort":"",
            "desc":"",
            "name":"test_1"
        }

        # 周期性任务
        {
            "plan_id":13,
            "run_time": {
                    "day_of_week": "2",
                    "hour": "16",
                    "minute": "19",
                    "second": "00"
            },
            "type": "cron",
            "robort":"",
            "desc":"",
            "name":"test_3"
        }
        # 添加cron类型定时任务
        {
            "plan_id":13,
            "run_time": {
                    "day_of_week": "2",
                    "hour": "16",
                    "minute": "19",
                    "second": "00"
            },
            "type": "cron",
            "robort":"",
            "desc":"",
            "name":"test_3"
    }

        Returns:
            [type]: [description]
    """
    task_info = addTaskForm().validate_for_api()
    plan_id = task_info.plan_id.data
    name = task_info.name.data
    desc = task_info.desc.data
    trigger_type = task_info.type.data
    robort = task_info.robort.data
    if trigger_type == "date":
        run_time = task_info.run_time.data
        Task_info = Task.add_task(name, desc, plan_id, run_time, 1, robort)
        print("添加一次性任务成功---[ %s ] " % Task_info.id)
    elif trigger_type == "interval":
        interval_time = task_info.interval_time.data
        Task_info = Task.add_task(name, desc, plan_id, interval_time, 2, robort)
        seconds = int(interval_time)
        if seconds <= 0:
            return Fail(code=40001, msg="请输入大于0的时间间隔！")
    elif trigger_type == "cron":
        day_of_week = task_info.run_time.data["day_of_week"]
        hour = task_info.run_time.data["hour"]
        minute = task_info.run_time.data["minute"]
        second = task_info.run_time.data["second"]
        cron_data = json.dumps(
            {
                "day_of_week": day_of_week,
                "hour": hour,
                "minute": minute,
                "second": second,
            }
        )
        Task_info = Task.add_task(name, desc, plan_id, cron_data, 3, robort)
        print("添加周期执行任务成功任务成功---[ %s ] " % id)
    return Sucess()


@api.route("/update", methods=["POST"])
@auth_jwt
def update_task():
    """[summary]
    更新计划任务,更新前要先停止任务
    Returns:
        [type]: [description]
    """
    task_info = updateTaskForm().validate_for_api()
    id = task_info.task_id.data
    Task_status = Task.query.filter_by(id=id).first_or_404("task")
    if Task_status.status == 1:
        return Sucess(msg="更新失败,请先停止任务")
    else:
        name = task_info.name.data
        desc = task_info.desc.data
        trigger_type = task_info.type.data
        robort = task_info.robort.data
        if trigger_type == "date":
            schedule = task_info.run_time.data
            task_type = 1
        elif trigger_type == "interval":
            schedule = task_info.interval_time.data
            task_type = 2
        elif trigger_type == "cron":
            day_of_week = task_info.run_time.data["day_of_week"]
            hour = task_info.run_time.data["hour"]
            minute = task_info.run_time.data["minute"]
            second = task_info.run_time.data["second"]
            schedule = json.dumps(
                {
                    "day_of_week": day_of_week,
                    "hour": hour,
                    "minute": minute,
                    "second": second,
                }
            )
            task_type = 3
        Task.update_task(
            id=id,
            name=name,
            desc=desc,
            schedule=schedule,
            type=task_type,
            robot=robort,
            status=0,
        )
        return Sucess()


@api.route("/del/<int:id>", methods=["GET"])
@auth_jwt
def delete_task(id):
    """[summary]
    删除任务，删除前需要先停止任务
    Returns:
        [type]: [description]
    """
    Task_info = Task.query.filter_by(id=id).first_or_404("task")
    if Task_info.status == 1:
        return Sucess(msg="停止失败,请先停止任务")
    else:
        Task.del_task(id)
        return Sucess()


@api.route("/start/<int:id>", methods=["GET"])
@auth_jwt
def start_resume_job(id):
    """[summary]
    启动任务
    Args:
        id ([type]): [description]

    Returns:
        [type]: [description]
    """
    task_info = Task.query.filter_by(id=id).first_or_404("task")
    if task_info.status == 1:
        return Sucess()
    else:
        if task_info.type == 1:
            y = datetime.strptime(task_info.schedule, "%Y-%m-%d %H:%M:%S")
            z = datetime.now()
            diff = z - y
            if diff.days < 0:
                scheduler.add_job(
                    func="app.libs.task_config:run_plan_by_task",
                    trigger="date",
                    run_date=task_info.schedule,
                    replace_existing=True,
                    coalesce=True,
                    id=str(task_info.id),
                    kwargs={"plan_id": task_info.plan_id, "task_id": id},
                )
            else:
                return Fail(msg="执行时间必须大于当前时间")
        elif task_info.type == 2:
            scheduler.add_job(
                func="app.libs.task_config:run_plan_by_task",
                trigger="interval",
                seconds=int(task_info.schedule),
                replace_existing=True,
                coalesce=True,
                id=str(task_info.id),
                kwargs={"plan_id": task_info.plan_id, "task_id": id},
            )
        elif task_info.type == 3:
            cron_time = json.loads(task_info.schedule)
            scheduler.add_job(
                func="app.libs.task_config:run_plan_by_task",
                id=str(task_info.id),
                trigger="cron",
                day_of_week=cron_time["day_of_week"],
                hour=int(cron_time["hour"]),
                minute=int(cron_time["minute"]),
                second=int(cron_time["second"]),
                replace_existing=True,
                kwargs={"plan_id": task_info.plan_id, "task_id": id},
            )
        Task.update_task(
            id=id,
            name=task_info.name,
            desc=task_info.desc,
            schedule=task_info.schedule,
            type=task_info.type,
            robot=task_info.robot,
            status=1,
        )
        return Sucess()


@api.route("/remove/<int:id>", methods=["GET"])
@auth_jwt
def stop_resume_job(id):
    """[summary]
    停止任务[直接删除]
    Args:
        id ([type]): [description]

    Returns:
        [type]: [description]
    """
    task_info = Task.query.filter_by(id=id).first_or_404("任务不存在")
    scheduler.remove_job(id)
    Task.update_task(
        id=id,
        name=task_info.name,
        desc=task_info.desc,
        schedule=task_info.schedule,
        type=task_info.type,
        robot=task_info.robot,
        status=0,
    )
    return Sucess()


@api.route("/list/<int:plan_id>", methods=["GET"])
@auth_jwt
def get_plan_stask_list(plan_id):
    """[summary]
    获取计划定时任务列表
    Args:
        plan_id ([type]): [description]

    Returns:
        [type]: [description]
    """
    plan_task_list = []
    task_list = Task.query.filter_by(plan_id=plan_id).all()
    if task_list:
        for i in task_list:
            data = {
                "id": i.id,
                "name": i.name,
                "desc": i.desc,
                "schedule": i.schedule,
                "type": i.type,
                "robot": i.robot,
                "status": i.status,
            }
            plan_task_list.append(data)
    return Sucess(data=plan_task_list)


@api.route("/robort/test", methods=["POST"])
@auth_jwt
def test_wechat_robort():
    robort_info = TaskForm().validate_for_api()
    print('robort_info.robort.data',robort_info.robort.data)
    if robort_info.robort.data and "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?" in robort_info.robort.data:
        headers = {"Content-Type": "text/plain"}
        data = {"msgtype": "text", "text": {"content": "hello world"}}
        requests.post(robort_info.robort.data, headers=headers, json=data)
        return Sucess()
    else:
        return Fail(msg="发送失败，请检查链接是否正确")


@api.route('/count', methods=["GET"])
@auth_jwt
def tasks_count():
    """
    首页燃尽图展示
    """
    TaskresultList = Report.get_report_count()
    return Sucess(data=TaskresultList)