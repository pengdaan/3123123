#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :case_detail.py
@说明        :
@时间        :2020/08/11 11:47:10
@作者        :Leo
@版本        :1.0
"""
from sqlalchemy import text

from flask_sqlalchemy import orm
from app.models.base import Base, db


class Case_Detail(Base):
    __tablename__ = "case_detail"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    name = db.Column(db.String(255), comment="接口名称", nullable=False)
    path = db.Column(db.String(255), comment="请求地址", nullable=False)
    setup = db.Column(db.Integer, nullable=False, comment="步骤")
    case_id = db.Column(db.Integer, db.ForeignKey("case.id", ondelete="CASCADE"))
    api_id = db.Column(db.Integer, db.ForeignKey("api.id", ondelete="CASCADE"))
    api_detail = db.relationship("Case", backref="case_details")
    module_id = db.Column(
        db.Integer, db.ForeignKey("case_module.id", ondelete="CASCADE")
    )
    module_detail = db.relationship("CaseModule", backref="module_details")

    @orm.reconstructor
    def __init__(self):
        self.fields = [
            "id",
            "name",
            "path",
            "setup",
            "case_id",
            "api_id",
            "api_detail",
            "module_id",
            "module_detail",
        ]

    @staticmethod
    def del_case_detail(id, case_id):
        taget_sql = "DELETE FROM case_detail WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def add_case_detail(name, module_id, path, setup, case_id, api_id):
        with db.auto_commit():
            CaseDetailInfo = Case_Detail()
            CaseDetailInfo.name = name
            CaseDetailInfo.module_id = module_id
            CaseDetailInfo.path = path
            CaseDetailInfo.setup = setup
            CaseDetailInfo.api_id = api_id
            CaseDetailInfo.case_id = case_id
            db.session.add(CaseDetailInfo)
            db.session.flush()
            return CaseDetailInfo

    @staticmethod
    def case_detail_update_setup(id, setup, name):
        Case_Detail.query.filter_by(id=id).update({"setup": setup, "name": name})
        return db.session.commit()

    @staticmethod
    def get_case_detail(case_id):
        res = (
            Case_Detail.query.filter_by(case_id=case_id)
            .order_by(Case_Detail.setup.asc())
            .all()
        )
        return res

    @staticmethod
    def case_detail_update_setups(data):
        for i in data:
            Case_Detail.query.filter_by(id=i["id"]).update(
                {
                    "setup": i["setup"],
                }
            )
            db.session.commit()
