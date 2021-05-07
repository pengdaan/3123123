#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :db.py
@说明        :db注册
@时间        :2020/08/06 15:41:43
@作者        :Leo
@版本        :1.0
"""

from flask_migrate import Migrate

from app.libs.db import db

migrate = Migrate(db=db)


def register_plugin(app):
    # db拓展对象注册到app
    db.init_app(app)
    # 注册Flask-Migrate到app
    migrate.init_app(app)
    # 需要把model类导入，否则创建表失败
    from app.models.api import Api
    from app.models.case import Case
    from app.models.case_detail import Case_Detail
    from app.models.case_module import CaseModule
    from app.models.category import Category
    from app.models.config import Config
    from app.models.hook import Hook
    from app.models.module import Module
    from app.models.project import Project
    from app.models.sqlconfig import Sql_Config
    from app.models.task import ScheduledTask
    from app.models.user import User
    from app.models.parameter import Parameters
    from app.models.plan import Plan
    from app.models.plan_detail import PlanDetail
    from app.models.plan_report_merge import planReportMerge
    from app.models.variable import Variable

