#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :api.py
@说明        : api管理[和模块关联]
@时间        :2020/08/11 11:44:39
@作者        :Leo
@版本        :1.0
"""

from sqlalchemy import text

from flask_sqlalchemy import orm
from app.models.base import Base, db


class Api(Base):
    __tablename__ = "api"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    name = db.Column(db.String(255), comment="接口名称", nullable=False)
    path = db.Column(db.String(500), comment="请求地址", nullable=False)
    method = db.Column(db.String(50), comment="请求方式", nullable=False)
    pro_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))
    cat_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"))
    type = db.Column(
        db.Integer,
        default=1,
        comment="接口类型:1,2 默认为1，1:接口；2:数据库",
    )
    category_detail = db.relationship("Category", backref="category_detail")

    __table_args__ = (db.UniqueConstraint("path", "cat_id", "status"),)

    @orm.reconstructor
    def __init__(self):
        self.fields = [
            "id",
            "name",
            "path",
            "method",
            "cat_id",
            "type",
            "category_detail",
            "pro_id",
        ]

    @staticmethod
    def add_api(name, method, path, pro_id, cat_id, type):
        with db.auto_commit():
            api = Api()
            api.name = name
            api.method = method
            api.path = path
            api.pro_id = pro_id
            api.cat_id = cat_id
            api.type = type
            db.session.add(api)
            db.session.flush()
            return api

    @staticmethod
    def del_api(id):
        # 物理删除
        taget_sql = "DELETE FROM `api` WHERE `id`=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def update_api(id, name, method, path, cat_id, api_type):

        Api.query.filter_by(id=id).update(
            {
                "name": name,
                "method": method,
                "path": path,
                "cat_id": cat_id,
                "type": api_type,
            }
        )
        db.session.commit()

    @staticmethod
    def get_category_detail(cat_id):
        res = Api.query.filter_by(cat_id=cat_id).all()
        return res
