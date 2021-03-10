#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :tasks.py
@说明        :
@时间        :2020/08/11 14:02:36
@作者        :Leo
@版本        :1.0
"""

import time

from sqlalchemy import text

from app.models.base import Base, db
from app.models.case import Case
from app.models.project import Project
from app.models.user import User


class ScheduledTask(Base):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    name = db.Column(db.String(255), comment="计划任务名称", nullable=False)
    desc = db.Column(db.String(500), comment="计划任务描述", nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey("plan.id", ondelete="CASCADE"))
    schedule = db.Column(db.String(255), comment="执行的内容", nullable=True)
    type = db.Column(db.Integer, comment="执行的类型,1,date:作业任务只会执行一次;2,interval:固定时间间隔触发;3,cron:特定时间周期性地触发")
    robot = db.Column(db.String(500), comment="机器人推送", nullable=True)

