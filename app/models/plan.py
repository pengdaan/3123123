#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :plan.py
@说明        :
@时间        :2020/12/03 11:53:40
@作者        :Leo
@版本        :1.0
"""


from sqlalchemy import text
from app.models.base import Base, db


class Plan(Base):
    __tablename__ = "plan"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    name = db.Column(db.String(255), comment="计划名称", nullable=False)
    case_list = db.Column(db.String(255), comment="用例列表")
    desc = db.Column(db.String(255), comment="计划描述")
    pro_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))
    isTasks = db.Column(db.Integer, default=0, comment="任务状态:0:未加入,1:已加入 默认为0")
    executor = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    executor_detail = db.relationship("User", backref="executor_detail")

    @staticmethod
    def add_project_plan(pro_id, name, executor, desc):
        # 添加任务
        with db.auto_commit():
            planInfo = Plan()
            planInfo.pro_id = pro_id
            planInfo.name = name
            planInfo.executor = executor
            planInfo.desc = desc
            db.session.add(planInfo)
            db.session.flush()
            return planInfo

    def update_project_plan(id, name, desc):
        # 更新任务
        Plan.query.filter_by(id=id).update({"name": name, "desc": desc})
        db.session.commit()

    @staticmethod
    def update_planCaseList(id, case_list):
        # 添加/添加case
        Plan.query.filter_by(id=id).update({"case_list": case_list})
        db.session.commit()

    @staticmethod
    def update_isTasks(id, isTasks):
        # 更新任务状态
        Plan.query.filter_by(id=id).update({"isTasks": isTasks})
        db.session.commit()

    @staticmethod
    def update_status(id, status):
        # 更新执行状态
        Plan.query.filter_by(id=id).update({"status": status})
        db.session.commit()

    @staticmethod
    def update_isStatus(id, status):
        # 更新任务执行的状态 1:准备就绪 2:执行中,3:已停止
        Plan.query.filter_by(id=id).update({"status": status})
        db.session.commit()

    @staticmethod
    def del_plan(id):
        # 物理删除
        taget_sql = "DELETE FROM plan WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})
