#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :case.py
@说明        :
@时间        :2020/08/11 11:46:38
@作者        :Leo
@版本        :1.0
"""

from sqlalchemy import text

from flask_sqlalchemy import orm
from app.models.api import Api
from app.models.base import Base, db
from app.models.config import Config


class Case(Base):
    __tablename__ = "case"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    case_name = db.Column(db.String(255), nullable=False, comment="用例名称")
    config_id = db.Column(db.Integer, db.ForeignKey("config.id", ondelete="CASCADE"))
    desc = db.Column(db.String(255), nullable=True, comment="用例描述")
    pro_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    tag_id = db.Column(db.Integer, db.ForeignKey("ca_tag.id", ondelete="CASCADE"))
    tag_detail = db.relationship("Case_Tag", backref="tag_detail")

    __table_args__ = (db.UniqueConstraint("case_name", "pro_id"),)

    @orm.reconstructor
    def __init__(self):
        self.fields = [
            "id",
            "case_name",
            "config_id",
            "pro_id",
            "tag_id",
            "tag_detail",
            "user_id",
        ]

    @staticmethod
    def add_Case(pro_id, case_name, user_id, config_id, desc, tag_id):
        print(pro_id, case_name, user_id, config_id, desc, tag_id)
        with db.auto_commit():
            case = Case()
            case.pro_id = pro_id
            case.case_name = case_name
            case.user_id = user_id
            case.config_id = config_id
            case.tag_id = tag_id
            case.desc = desc
            db.session.add(case)
            db.session.flush()
            return case

    @staticmethod
    def update_Case(id, pro_id, case_name, config_id, tag_id, desc):
        Case.query.filter_by(id=id, pro_id=pro_id).update(
            {
                "case_name": case_name,
                "config_id": config_id,
                "config_id": config_id,
                "desc": desc,
                "tag_id": tag_id,
            }
        )
        db.session.commit()

    @staticmethod
    def del_case(id):
        # 物理删除
        taget_sql = "DELETE FROM `case` WHERE `id`=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def get_Case_detail(id):
        result = Case.query.filter_by(id=id, status=1).first_or_404("Case")
        configInfo = Config.query.filter_by(id=result.config_id).first_or_404("Case")
        case_detail = []
        for n in result.case_details:
            apiDetail = Api.query.filter_by(id=n.api_id, status=1).first_or_404("Api")
            data = {
                "api_id": n.api_id,
                "method": apiDetail.method,
                "api_name": apiDetail.name,
                "case_detail_id": n.id,
                "name": n.name,
                "module_id": n.module_id,
                "path": n.path,
                "setup": n.setup,
            }
            case_detail.append(data)
        case = {
            "id": result.id,
            "tag_id": result.tag_id,
            "tag_name": result.tag_detail.tag_name,
            "desc": result.desc,
            "case_name": result.case_name,
            "pro_id": result.pro_id,
            "config_id": result.config_id,
            "config_name": configInfo.name,
            "case_detail": case_detail,
        }
        return case

    @staticmethod
    def get_all_case_by_caseList(caList):
        case_list = []
        for i in caList:
            result = Case.query.filter_by(id=int(i)).first_or_404("Case 不存在")
            case_detail = {
                "case_id": result.id,
                "pro_id": result.pro_id,
                "config_id": result.config_id,
                "user_id": 1,
            }
            case_list.append(case_detail)
        return case_list

    @staticmethod
    def get_all_case_by_project(pro_id, executor=1):
        case_list = []
        result = Case.query.filter_by(pro_id=pro_id, status=1).all()
        if len(result) > 0:
            for i in result:
                case_detail = {
                    "case_id": i.id,
                    "pro_id": i.pro_id,
                    "config_id": i.config_id,
                    "user_id": executor,
                }
                case_list.append(case_detail)
        return case_list

    @staticmethod
    def get_all_case_by_tag(tag_id, executor=1):
        case_list = []
        result = Case.query.filter_by(tag_id=tag_id, status=1).all()
        if len(result) > 0:
            for i in result:
                case_detail = {
                    "case_id": i.id,
                    "pro_id": i.pro_id,
                    "config_id": i.config_id,
                    "user_id": executor,
                    "tag_id": i.tag_id,
                }
                case_list.append(case_detail)
        return case_list
