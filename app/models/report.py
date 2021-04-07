#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :report.py
@说明        :
@时间        :2020/08/11 14:01:45
@作者        :Leo
@版本        :1.0
"""
import time

from sqlalchemy import text

from flask_sqlalchemy import orm
from app.models.base import Base, db


class Report(Base):
    __tablename__ = "report"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    summary = db.Column(db.Text(16777216), comment="报告报文", nullable=False)
    report_name = db.Column(db.String(255), comment="报告名称", nullable=False)
    executor = db.Column(db.Integer, comment="执行者", nullable=True)
    pro_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))

    @orm.reconstructor
    def __init__(self):
        self.fields = ["id", "summary", "report_name", "executor", "pro_id"]

    @staticmethod
    def add_summary(pro_id, summary, report_name, create_time, update_time, executor=1):
        with db.auto_commit():
            report = Report()
            report.pro_id = pro_id
            report.summary = summary
            report.executor = executor
            report.report_name = report_name
            report.create_time = create_time
            report.update_time = update_time
            db.session.add(report)
            db.session.flush()
            return report.id

    @staticmethod
    def del_report(id):
        taget_sql = "DELETE FROM report WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def get_report_count():
        TaskresultList = Report.query.all()
        taskslist = []
        for i in TaskresultList:
            un_time = int(time.mktime(i.create_time.timetuple()) * 1000)
            data = {"date": un_time, "count": 10}
            taskslist.append(data)
        return taskslist
