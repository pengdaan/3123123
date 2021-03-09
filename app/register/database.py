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
    # from app.models.api import Api
    # from app.models.case import Case
    # from app.models.caseDetail import Case_Detail
    # from app.models.caseModule import CaseModule
    # from app.models.category import Category
    # from app.models.config import Config
    # from app.models.hook import Hook
    # from app.models.module import Module
    # from app.models.project import Project
    # from app.models.sqlConfig import Sql_Config
    # from app.models.tasks import ScheduledTasks
    # from app.models.tasksDetail import TasksDetail
    # from app.models.user import User
    # from app.models.variables import Variables
    # from app.models.cr_variables import Cr_Variable
    # from app.models.cr_case import CrCase
    # from app.models.cr_case_setup import Cr_Case_Setup
    # from app.models.cr_case_module_detail import Cr_Case_Module_Detail
    # from app.models.cr_case_detail import Cr_Case_Setup_Detail
    # from app.models.Parameters import Parameters
    # from app.models.plan import Plan
    # from app.models.planDetail import PlanDetail
    # from app.models.planReportMerge import planReportMerge
