#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :sqlConfig.py
@说明        :
@时间        :2020/08/11 14:02:10
@作者        :Leo
@版本        :1.0
"""

from datetime import datetime

from sqlalchemy import text
from app.models.base import Base, db
from app.models.project import Project


class Sql_Config(Base):
    __tablename__ = "sql_config"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    name = db.Column(db.String(255), comment="数据库名称", nullable=False)
    host = db.Column(db.String(255), comment="数据库host", nullable=False)
    username = db.Column(db.String(50), comment="用户名", nullable=False)
    password = db.Column(db.String(50), comment="账号", nullable=False)
    database = db.Column(db.String(50), comment="密码", nullable=False)
    port = db.Column(db.Integer, comment="端口号", nullable=False)
    pro_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))

    __table_args__ = (db.UniqueConstraint("pro_id", "host", "database"),)

    @staticmethod
    def get_sql_config_by_id(id, type=None):
        if type:
            res = Sql_Config.query.filter_by(id=id).first()
            res = {
                "id": res.id,
                "name": res.name,
                "host": res.host,
                "database": res.database,
                "username": res.username,
                "password": res.password,
                "port": res.port,
                "pro_id": res.pro_id,
            }
        else:
            res = Sql_Config.query.filter_by(id=id).first()
        return res

    @staticmethod
    def add_sql_config(name, host, username, password, database, port, pro_id):
        with db.auto_commit():
            sql_info = Sql_Config()
            sql_info.name = name
            sql_info.host = host
            sql_info.username = username
            sql_info.password = password
            sql_info.database = database
            sql_info.port = port
            sql_info.pro_id = pro_id
            db.session.add(sql_info)
            db.session.flush()
            return sql_info

    @staticmethod
    def del_sql_config(id):
        taget_sql = "DELETE FROM sql_config WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def update_sql_config(id, name, host, username, password, database, port):
        Sql_Config.query.filter_by(id=id, status=1).update(
            {
                "name": name,
                "host": host,
                "username": username,
                "password": password,
                "database": database,
                "port": port,
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        return db.session.commit()

    @staticmethod
    def is_empty_sql_config_list(pro_id):
        Project.query.filter_by(id=pro_id, status=1).first_or_404("ProId")
        res = Sql_Config.query.filter_by(pro_id=pro_id, status=1).all()
        config_list = []
        if len(res) > 0:
            for i in res:
                result = {
                    "id": i.id,
                    "name": i.name,
                    "host": i.host,
                    "database": i.database,
                    "create_time": i.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "update_time": i.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                config_list.append(result)
        return config_list

    @staticmethod
    def search_sql_list(pro_id, kw):
        res = (
            Sql_Config.query.filter_by(pro_id=pro_id)
            .filter(Sql_Config.name.like("%{0}%".format(kw)))
            .all()
        )
        config_list = []
        if len(res) > 0:
            for i in res:
                result = {
                    "id": i.id,
                    "name": i.name,
                    "host": i.host,
                    "database": i.database,
                    "create_time": i.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "update_time": i.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                config_list.append(result)
        return config_list
