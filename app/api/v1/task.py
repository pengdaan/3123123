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
from app.models.project import Project
from app.models.report import Report
from app.models.task import ScheduledTask as Task
from app.register.executor import executor
from app.validators.task_validator import TasksForm
from app.register.scheduler import scheduler
from flask import jsonify
from app.libs import task_config

api = Redprint("task")


# 新增job
@api.route('/addCron', methods=['post'])
def add_cron():
    jobargs = request.get_json()
    id = jobargs['task_id']
    trigger_type = jobargs['trigger_type']
    if trigger_type == "date":
        run_time = jobargs['run_time']
        job = scheduler.add_job(func="app.libs.task_config:my_job",
                                trigger=trigger_type,
                                run_date=run_time,
                                replace_existing=True,
                                coalesce=True,
                                id=id)
        print("添加一次性任务成功---[ %s ] " % id)
    elif trigger_type == 'interval':
        seconds = jobargs['interval_time']
        seconds = int(seconds)
        if seconds <= 0:
            raise TypeError('请输入大于0的时间间隔！')
        scheduler.add_job(func="task:my_job",
                          trigger=trigger_type,
                          seconds=seconds,
                          replace_existing=True,
                          coalesce=True,
                          id=id)
    elif trigger_type == "cron":
        day_of_week = jobargs["run_time"]["day_of_week"]
        hour = jobargs["run_time"]["hour"]
        minute = jobargs["run_time"]["minute"]
        second = jobargs["run_time"]["second"]
        scheduler.add_job(func="task:my_job", id=id, trigger=trigger_type, day_of_week=day_of_week,
                          hour=hour, minute=minute,
                          second=second, replace_existing=True)
        print("添加周期执行任务成功任务成功---[ %s ] " % id)
    return Sucess(msg="新增任务成功")

# 暂停
@api.route('/<task_id>/pause', methods=['GET'])
def pause_job(task_id):
    response = {'status': False}
    try:
        scheduler.pause_job(task_id)
        response['status'] = True
        response['msg'] = "job[%s] pause success!" % task_id
    except Exception as e:
        response['msg'] = str(e)
    return Sucess(response)

#启动
@api.route('/<task_id>/resume',methods=['GET'])
def start_resume_job(task_id):
    response = {'status': False}
    try:
        scheduler.resume_job(task_id)
        response['status'] = True
        response['msg'] = "job[%s] resume success!" % task_id
    except Exception as e:
        response['msg'] = str(e)
    return Sucess(response)

#删除
@api.route('/<task_id>/remove', methods=['GET'])
def semove_resume_job(task_id):
    response = {'status': False}
    try:
        scheduler.remove_job(task_id)
        response['status'] = True
        response['msg'] = "job[%s] remove success!" % task_id
    except Exception as e:
        response['msg'] = str(e)
    return Sucess(response)

#编辑
#编辑逻辑与新增大致相同，编辑时如果传的task_id 任务表中已存在，那么会直接替换原来的task_id。 

#查job信息，获取的信息包括了job类型和执行时间，可以打印出来结果再根据自己的代码逻辑进行编写
#查看所有的job信息
# ret_list = scheduler.get_jobs()
# # 查看指定的job信息
# ret_list = scheduler.get_job(jid)

