#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :Parameters.py
@说明        :数据参数化列表
@时间        :2020/10/16 15:23:27
@作者        :Leo
@版本        :1.0
"""

import json
from datetime import datetime

from sqlalchemy import text

from app.libs.code import AuthFailed, NotFound
from flask_sqlalchemy import orm
from app.libs.tools_func import serialize_sqlalchemy_obj
from app.models.base import Base, db


class Parameters(Base):
    __tablename__ = "parameters"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    case_id = db.Column(db.Integer, db.ForeignKey("case.id", ondelete="CASCADE"))
    key = db.Column(db.String(255), comment="参数名", nullable=False)
    parameters = db.Column(db.Text, nullable=True, comment="Parameters内容")

    @orm.reconstructor
    def __init__(self):
        # 指明需要序列化的key
        self.fields = ["id", "case_id", "parameters"]

    @staticmethod
    def add_parameters(case_id, key, parametersData):
        with db.auto_commit():
            parameters = Parameters()
            parameters.case_id = int(case_id)
            parameters.key = key
            parameters.parameters = json.dumps(parametersData)
            parameters.status = 0
            db.session.add(parameters)
            db.session.flush()
            return parameters

    @staticmethod
    def update_parameters(id, key, parameters):
        Parameters.query.filter_by(id=id).update(
            {"parameters": json.dumps(parameters), "key": key}
        )
        db.session.flush()
        db.session.commit()

    @staticmethod
    def update_parameters_status(id, status):
        Parameters.query.filter_by(id=id).update({"status": status})
        db.session.flush()
        db.session.commit()

    @staticmethod
    def key_is_exist(case_id, key, id=None):
        if id is not None:
            taget_sql = "SELECT * FROM `parameters` WHERE find_in_set(:key, `key`) and case_id = :case_id and id !=:id"
            result = db.session.execute(
                text(taget_sql), {"case_id": case_id, "key": key, "id": id}
            ).fetchall()
            is_exist = serialize_sqlalchemy_obj(result)
            return is_exist
        else:
            taget_sql = "SELECT * FROM `parameters` WHERE find_in_set(:key, `key`) and case_id = :case_id"
            result = db.session.execute(
                text(taget_sql), {"case_id": case_id, "key": key}
            ).fetchall()
            is_exist = serialize_sqlalchemy_obj(result)
            return is_exist

    @staticmethod
    def del_parameters(id):
        taget_sql = "DELETE FROM parameters WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})
