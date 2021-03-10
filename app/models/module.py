#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :module.py
@说明        :
@时间        :2020/08/11 14:01:14
@作者        :Leo
@版本        :1.0
"""

from sqlalchemy import text

from flask_sqlalchemy import orm
from app.models.base import Base, db
from app.models.sqlconfig import Sql_Config
from app.models.user import User


class Module(Base):
    __tablename__ = "module"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    name = db.Column(db.String(255), comment="模块名称", nullable=False)
    func_name = db.Column(db.String(500), comment="场景中使用的函数", nullable=True)
    body = db.Column(db.Text, comment="主体信息", nullable=False)
    api_id = db.Column(db.Integer, db.ForeignKey("api.id", ondelete="CASCADE"))
    sql_config_id = db.Column(
        db.Integer, db.ForeignKey("sql_config.id", ondelete="CASCADE")
    )
    api_detail = db.relationship("Api", backref="module_detail")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    __table_args__ = (db.UniqueConstraint("name", "api_id", "user_id"),)

    @orm.reconstructor
    def __init__(self):
        self.fields = [
            "id",
            "name",
            "body",
            "api_id",
            "sql_config_id",
            "api_detail",
            "user_id",
        ]

    @staticmethod
    def is_empty_api_module(name, api_id, user_id):
        return Module.query.filter_by(name=name, api_id=api_id, user_id=user_id).first()

    @staticmethod
    def add_api_module(name, body, api_id, user_id, sql_config_id=None):
        with db.auto_commit():
            module = Module()
            module.name = name
            module.body = body
            module.api_id = api_id
            module.user_id = user_id
            module.sql_config_id = sql_config_id
            db.session.add(module)
            db.session.flush()
            return module

    @staticmethod
    def del_module(id):
        taget_sql = "DELETE FROM module WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def is_empty_api_module_by_apiId(api_id):
        Modules = Module.query.filter_by(api_id=api_id).all()
        moduleList = []
        if len(Modules) > 0:
            for i in Modules:
                modules = {"id": i.id, "name": i.name, "api_id": api_id}
                moduleList.append(modules)
        return moduleList

    @staticmethod
    def update_module(id, name, body, func_name, sql_config_id=None):
        Module.query.filter_by(id=id).update(
            {
                "name": name,
                "body": body,
                "func_name": func_name,
                "sql_config_id": sql_config_id,
            }
        )
        db.session.commit()

    @staticmethod
    def update_module_name(id, name):
        Module.query.filter_by(id=id).update(
            {
                "name": name,
            }
        )
        return db.session.commit()

    @staticmethod
    def get_api_modules(id, status=None):
        modules = []
        res = Module.query.filter_by(api_id=id).all()
        if status:
            if len(res) > 0:
                for i in res:
                    user_detail = User.filter_by(id=i.user_id).first()
                    data = {
                        "search_name": user_detail.name + "-" + i.name,
                        "module_id": i.id,
                        "name": i.name,
                        "body": i.body,
                        "api_id": i.api_id,
                        "user_id": i.user_id,
                        "sql_config_id": i.sql_config_id,
                    }
                    modules.append(data)
        else:
            if len(res) > 0:
                for i in res:
                    if i.sql_config_id:
                        sqlConfigDetail = Sql_Config.query.filter_by(
                            id=i.sql_config_id
                        ).first_or_404()
                        sql_config_id = i.sql_config_id
                        sql_name = sqlConfigDetail.name
                    else:
                        sql_config_id = 0
                        sql_name = None
                    data = {
                        "module_id": i.id,
                        "name": i.name,
                        "body": i.body,
                        "api_id": i.api_id,
                        "user_id": i.user_id,
                        "sql_config_detail": {
                            "sql_config_id": sql_config_id,
                            "sql_config_name": sql_name,
                        },
                    }
                    modules.append(data)

        return modules

    @staticmethod
    def get_api_modules_by_key(id, key):
        modules = []
        res = (
            Module.filter_by(api_id=id)
            .query.filter(Module.name.like("%" + key + "%"))
            .all()
        )
        if len(res) > 0:
            for i in res:
                user_detail = User.filter_by(id=i.user_id).first()
                data = {
                    "search_name": user_detail.name + "-" + i.name,
                    "module_id": i.id,
                    "name": i.name,
                    "body": i.body,
                    "api_id": i.api_id,
                    "user_id": i.user_id,
                }
                modules.append(data)
        return modules

    @staticmethod
    def get_api_modules_by_user_id(id, user_id):
        modules = []
        res = Module.query.filter_by(api_id=id, user_id=user_id).all()
        if len(res) > 0:
            for i in res:
                user_detail = User.filter_by(id=i.user_id).first()
                data = {
                    "search_name": user_detail.name + "-" + i.name,
                    "module_id": i.id,
                    "name": i.name,
                    "body": i.body,
                    "api_id": i.api_id,
                    "user_id": i.user_id,
                }
                modules.append(data)
        return modules
