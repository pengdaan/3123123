#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :config.py
@说明        :
@时间        :2020/08/11 14:00:10
@作者        :Leo
@版本        :1.0
"""

from sqlalchemy import text

from flask_sqlalchemy import orm
from app.models.base import Base, db


class Config(Base):
    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    name = db.Column(db.String(255), comment="环境名称", nullable=False)
    body = db.Column(db.Text, comment="主体信息", nullable=False)
    base_url = db.Column(db.String(255), comment="基础域名", nullable=False)
    type = db.Column(db.Integer, nullable=False, comment="类型,1:运行配置,2:数据库配置", default=1)
    pro_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))

    __table_args__ = (db.UniqueConstraint("name", "pro_id"),)

    @staticmethod
    def add_config(name, body, base_url, pro_id, type=1):
        with db.auto_commit():
            config = Config()
            config.name = name
            config.body = body
            config.base_url = base_url
            config.pro_id = pro_id
            config.type = type
            db.session.add(config)
            return config

    @staticmethod
    def del_config(id):
        taget_sql = "DELETE FROM config WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def update_config(id, name, body, base_url, type=1):
        Config.query.filter_by(id=id).update(
            {"name": name, "body": body, "base_url": base_url, "type": type}
        )
        db.session.commit()

    @staticmethod
    def config_list(pro_id, type):
        if type:
            res = Config.query.filter_by(pro_id=pro_id, type=type).all()
        else:
            res = Config.query.filter_by(pro_id=pro_id).all()
        config_list = []
        if len(res) > 0:
            for i in res:
                result = {
                    "id": i.id,
                    "name": i.name,
                    "request": i.body,
                    "base_url": i.base_url,
                    "type": i.type,
                    "create_time": i.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "update_time": i.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                config_list.append(result)
        return config_list

    @staticmethod
    def search_config_list(pro_id, kw):
        res = (
            Config.query.filter_by(pro_id=pro_id)
            .filter(Config.name.like("%{0}%".format(kw)))
            .all()
        )
        config_list = []
        if len(res) > 0:
            for i in res:
                result = {
                    "id": i.id,
                    "name": i.name,
                    "request": i.body,
                    "base_url": i.base_url,
                    "type": i.type,
                    "create_time": i.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "update_time": i.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                config_list.append(result)
        return config_list
