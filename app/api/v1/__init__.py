#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :__init__.py
@说明        :api版本控制
@时间        :2020/08/05 21:53:22
@作者        :Leo
@版本        :1.0
"""

from flask import Blueprint

from app.api.v1 import (
    api,
    case,
    category,
    config,
    hook,
    module,
    parameter,
    plan,
    project,
    report,
    sql,
    swagger,
    tag,
    task,
    user,
    capture
)


def create_blueprint_v1():
    """[summary]
    api 版本控制
    Returns:
        [type]: [description]
    """
    bp_v1 = Blueprint("v1", __name__)
    user.api.register(bp_v1)
    project.api.register(bp_v1)
    api.api.register(bp_v1)
    case.api.register(bp_v1)
    category.api.register(bp_v1)
    config.api.register(bp_v1)
    hook.api.register(bp_v1)
    module.api.register(bp_v1)
    report.api.register(bp_v1)
    sql.api.register(bp_v1)
    task.api.register(bp_v1)
    parameter.api.register(bp_v1)
    tag.api.register(bp_v1)
    swagger.api.register(bp_v1)
    plan.api.register(bp_v1)
    capture.api.register(bp_v1)

    return bp_v1
