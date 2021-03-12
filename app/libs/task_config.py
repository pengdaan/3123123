#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :task_config.py
@说明        :定时器执行方法配置
@时间        :2021/03/10 10:40:01
@作者        :Leo
@版本        :1.0
"""

from app.libs.plan_run import run_plan_by_user
from app.models.user import User
from app.register.scheduler import scheduler


def run_plan_by_task(plan_id, task_id):
    # 在任务中获取程序上文进行操作
    with scheduler.app.app_context():
        userInfo = User.query.filter_by(username="admin").first_or_404("UserId 不存在")
        run_plan_by_user(plan_id, userInfo.id, task_id)
