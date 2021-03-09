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
from app.models.tasks_detail import TasksDetail
from app.models.user import User


class ScheduledTasks(Base):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    pro_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))
    executor = db.Column(db.Integer, comment="执行者", nullable=False)
    count = db.Column(db.Integer, comment="执行的用例数量")
    tasks_detail = db.Column(db.String(255), comment="项目内的用例详情")

    @staticmethod
    def get_project_tasks_list(page, kw):
        if not kw:
            if page == 1:
                res = (
                    ScheduledTasks.query.order_by(ScheduledTasks.id.desc())
                    .limit(10)
                    .offset(0)
                    .all()
                )
            else:
                page = int(page - 1) * 10
                res = (
                    ScheduledTasks.query.order_by(ScheduledTasks.id.desc())
                    .limit(10)
                    .offset(page)
                    .all()
                )
            count = ScheduledTasks.query.count()
        else:
            project_ids = []
            projects = Project.query.filter(
                Project.project_name.like("%{0}%".format(kw))
            ).all()
            for i in projects:
                project_ids.append(i.id)
            if page == 1:
                res = (
                    ScheduledTasks.query.filter(ScheduledTasks.pro_id.in_(project_ids))
                    .order_by(ScheduledTasks.id.desc())
                    .limit(10)
                    .offset(0)
                    .all()
                )
            else:
                page = int(page - 1) * 10
                res = (
                    ScheduledTasks.query.filter(ScheduledTasks.pro_id.in_(project_ids))
                    .order_by(ScheduledTasks.id.desc())
                    .limit(10)
                    .offset(page)
                    .all()
                )
            count = len(res)
        tasks_list = []
        if len(res) > 0:
            for i in res:
                project_name = (
                    Project.query.filter_by(id=i.pro_id).first()
                ).project_name
                executor = (User.query.filter_by(id=i.executor).first()).username
                data = {
                    "id": i.id,
                    "project_name": project_name,
                    "executor": executor,
                    "count": i.count,
                    "create_time": i.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                tasks_list.append(data)
        return {"tasks_list": tasks_list, "count": count}

    @staticmethod
    def del_tasks_detail(task_detail):
        if isinstance(task_detail, list):
            for i in task_detail:
                del_data = TasksDetail.query.filter_by(id=i).first()
                db.session.delete(del_data)
                db.session.commit()

    @staticmethod
    def del_project_tasks(id):
        taget_sql = "DELETE FROM tasks WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def get_project_tasks_detail(tasks_id):
        ScheduledTasks_data = ScheduledTasks.query.filter_by(id=tasks_id).first_or_404(
            "taskId"
        )
        tasks_detail_list = []
        project_name = (
            Project.query.filter_by(id=ScheduledTasks_data.pro_id).first()
        ).project_name
        executor = (
            User.query.filter_by(id=ScheduledTasks_data.executor).first()
        ).username
        tasks_detail = (ScheduledTasks_data.tasks_detail).split(",")
        for i in tasks_detail:
            this_tasks_detail = TasksDetail.query.filter_by(id=int(i)).first()
            if this_tasks_detail:
                case_name = (
                    Case.query.filter_by(id=this_tasks_detail.case_id).first()
                ).case_name
                target_tasks_status = (
                    "SUCESS" if this_tasks_detail.case_status == 1 else "ERROR"
                )
                target_tasks_detail = {
                    "id": int(i),
                    "case_name": case_name,
                    "status": target_tasks_status,
                    "summary": this_tasks_detail.summary,
                }
                tasks_detail_list.append(target_tasks_detail)
        return {
            "pro_id": ScheduledTasks_data.pro_id,
            "project_name": project_name,
            "target_tasks_detail": tasks_detail_list,
        }

    @staticmethod
    def get_tasks_count():
        TaskresultList = ScheduledTasks.query.all()
        taskslist = []
        for i in TaskresultList:
            un_time = int(time.mktime(i.create_time.timetuple()) * 1000)
            data = {"date": un_time, "count": i.count}
            taskslist.append(data)
        return taskslist

    @staticmethod
    def add_case_tasks(case_id, case_status, summary):
        with db.auto_commit():
            case_tasks_info = TasksDetail()
            case_tasks_info.case_id = case_id
            case_tasks_info.case_status = case_status
            case_tasks_info.summary = summary
            db.session.add(case_tasks_info)
            db.session.flush()
            return case_tasks_info.id

    @staticmethod
    def add_project_tasks(pro_id, executor, count, tasks_detail):
        with db.auto_commit():
            project_tasks = ScheduledTasks()
            project_tasks.pro_id = pro_id
            project_tasks.executor = executor
            project_tasks.count = count
            project_tasks.tasks_detail = tasks_detail
            db.session.add(project_tasks)
            db.session.flush()
            return project_tasks
