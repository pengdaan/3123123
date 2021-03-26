#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :planReport.py
@说明        :
@时间        :2020/12/03 12:00:00
@作者        :Leo
@版本        :1.0
"""


from app.models.base import Base, db
from app.models.plan_detail import PlanDetail
from app.models.user import User
from app.libs.times import get_time


class planReportMerge(Base):
    __tablename__ = "plan_detail_merge"

    id = db.Column(db.Integer, primary_key=True, comment="id")
    plan_id = db.Column(db.Integer, db.ForeignKey("plan.id", ondelete="CASCADE"))
    plan_detail = db.relationship("Plan", backref="plan_detail")
    plan_report_detail = db.Column(db.String(255), comment="项目内的报告详情")
    executor = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))

    @staticmethod
    def add_planReportMerge(plan_id, plan_report_detail, user_id):
        with db.auto_commit():
            planReportMergeInfo = planReportMerge()
            planReportMergeInfo.plan_id = plan_id
            planReportMergeInfo.executor = user_id
            planReportMergeInfo.plan_report_detail = plan_report_detail
            planReportMergeInfo.create_time = get_time()
            planReportMerge.update_time = get_time()
            db.session.add(planReportMergeInfo)
            db.session.flush()
            return planReportMergeInfo

    @staticmethod
    def get_planReportMerge(plan_id, page):
        reports = []
        caseDetail = []
        Allcount = planReportMerge.query.filter_by(plan_id=plan_id).count()
        if page == 1:
            ReportInfo = (
                planReportMerge.query.filter_by(plan_id=plan_id)
                .limit(10)
                .offset(0)
                .all()
            )
        else:
            page = int(page - 1) * 10
            ReportInfo = (
                planReportMerge.query.filter_by(plan_id=plan_id)
                .limit(10)
                .offset(page)
                .all()
            )
        for i in ReportInfo:
            reportList = i.plan_report_detail.split(",")
            for case in reportList:
                PlanDetailInfo = PlanDetail.query.filter_by(id=int(case)).first()
                caseData = {
                    "case_name": PlanDetailInfo.Case_detail.case_name,
                    "case_id": PlanDetailInfo.Case_detail.id,
                    "case_status": "SUCCESS"
                    if PlanDetailInfo.case_status == 1
                    else "ERROR",
                    "summary": PlanDetailInfo.summary,
                }
                caseDetail.append(caseData)

            UserInfo = User.query.filter_by(id=i.executor).first()
            data = {
                "id": i.id,
                "reportList": reportList,
                "case_detail": caseDetail,
                "update_time": i.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                "count": len(reportList),
                "executor": UserInfo.username,
            }
            reports.append(data)
        return {"reportList": reports, "count": Allcount}
