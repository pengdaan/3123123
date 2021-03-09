#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :planReport.py
@说明        :
@时间        :2020/12/03 12:00:00
@作者        :Leo
@版本        :1.0
"""

from sqlalchemy import text

from flask_sqlalchemy import orm
from app.models.base import Base, db


class PlanDetail(Base):
    __tablename__ = "plan_detail"

    id = db.Column(db.Integer, primary_key=True, comment="id")
    case_id = db.Column(db.Integer, db.ForeignKey("case.id", ondelete="CASCADE"))
    case_status = db.Column(
        db.Integer,
        default=1,
        comment="Case状态:0:失败,1:成功 默认为1",
    )
    Case_detail = db.relationship("Case", backref="Case_detail")
    summary = db.Column(db.Text(16777216), comment="报告报文", nullable=False)

    @staticmethod
    def add_plan_detail(case_id, case_status, summary):
        with db.auto_commit():
            planDetailInfo = PlanDetail()
            planDetailInfo.case_id = case_id
            planDetailInfo.case_status = case_status
            planDetailInfo.summary = summary
            db.session.add(planDetailInfo)
            db.session.flush()
            return planDetailInfo.id
