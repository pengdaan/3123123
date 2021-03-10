#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :caseModule.py
@说明        :
@时间        :2020/08/11 13:59:04
@作者        :Leo
@版本        :1.0
"""

from sqlalchemy import text

from flask_sqlalchemy import orm
from app.models.base import Base, db


class CaseModule(Base):
    __tablename__ = "case_module"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    name = db.Column(db.String(255), comment="模块名称", nullable=False)
    body = db.Column(db.Text, comment="主体信息", nullable=False)
    func_name = db.Column(db.String(500), comment="场景中使用的函数", nullable=True)
    sql_config_id = db.Column(
        db.Integer, db.ForeignKey("sql_config.id", ondelete="CASCADE")
    )
    other_config_id = db.Column(
        db.Integer, db.ForeignKey("config.id", ondelete="CASCADE")
    )
    case_id = db.Column(db.Integer, db.ForeignKey("case.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))

    @orm.reconstructor
    def __init__(self):
        self.fields = [
            "id",
            "name",
            "body",
            "sql_config_id",
            "other_config_id",
            "case_id",
            "user_id",
        ]

    @staticmethod
    def del_case_module(id):
        taget_sql = "DELETE FROM case_module WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def update_module(id, name, body, other_config_id, sql_config_id):
        print(
            "id, name, body, other_config_id, sql_config_id",
            id,
            name,
            body,
            other_config_id,
            sql_config_id,
        )
        CaseModule.query.filter_by(id=id).update(
            {
                "name": name,
                "body": body,
                "other_config_id": other_config_id,
                "sql_config_id": sql_config_id,
            }
        )
        return db.session.commit()

    @staticmethod
    def add_api_module(name, body, case_id, user_id, other_config_id, sql_config_id):
        with db.auto_commit():
            CaseModuleInfo = CaseModule()
            CaseModuleInfo.name = name
            CaseModuleInfo.body = body
            CaseModuleInfo.case_id = case_id
            CaseModuleInfo.user_id = user_id
            CaseModuleInfo.other_config_id = other_config_id
            CaseModuleInfo.sql_config_id = sql_config_id
            db.session.add(CaseModuleInfo)
            db.session.flush()
            return CaseModuleInfo

    @staticmethod
    def update_module_name(id, name, body):
        CaseModule.query.filter_by(id=id).update(
            {
                "name": name,
                "body": body,
            }
        )
        return db.session.commit()
