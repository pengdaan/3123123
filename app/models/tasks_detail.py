#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :tasksDetail.py
@说明        :
@时间        :2020/08/11 14:03:12
@作者        :Leo
@版本        :1.0
"""

from app.models.base import Base, db


class TasksDetail(Base):
    __tablename__ = "tasks_detail"

    id = db.Column(db.Integer, primary_key=True, comment="id")
    case_id = db.Column(db.Integer, db.ForeignKey("case.id", ondelete="CASCADE"))
    case_status = db.Column(
        db.Integer,
        default=1,
        comment="Case状态:0:失败,1:成功 默认为1",
    )
    summary = db.Column(db.Text(16777216), comment="报告报文", nullable=False)
