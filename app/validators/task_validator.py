#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :task.py
@说明        :
@时间        :2020/08/19 13:58:38
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired
from app.models.plan import Plan
from app.validators.base_validator import BaseForm as Form


class TaskForm(Form):
    robot = StringField()


class addTaskForm(TaskForm):
    plan_id = IntegerField([DataRequired(message="计划ID不允许为空")])
    name = StringField(DataRequired(message="定时任务名不能为空"))
    desc = StringField()
    type = StringField([DataRequired(message="类型不允许为空")])
    run_time = StringField()
    interval_time = IntegerField()

    def validate_plan_id(self, value):
        if Plan.query.filter_by(id=value.data).first() is None:
            raise ValidationError(message="计划不存在")


class updateTaskForm(addTaskForm):
    task_id = IntegerField([DataRequired(message="任务不允许为空")])
