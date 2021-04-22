#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :variable.py
@说明        :
@时间        :2021/04/20 16:58:32
@作者        :Leo
@版本        :1.0
'''

from sqlalchemy import text
from flask_sqlalchemy import orm
from app.models.base import Base, db


class Variable(Base):
    __tablename__ = "variable"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    name = db.Column(db.String(255), nullable=False, comment="变量名")
    desc = db.Column(db.String(255), nullable=True, comment="变量描述")
    api_id = db.Column(db.Integer, db.ForeignKey('api.id', ondelete="CASCADE"))
    pro_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"))
    case_id = db.Column(db.Integer, db.ForeignKey('case.id', ondelete="CASCADE"))

    __table_args__ = (db.UniqueConstraint("name", "pro_id"),)

