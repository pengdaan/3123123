#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :base.py
@说明        :模型基础类
@时间        :2020/08/06 09:57:17
@作者        :Leo
@版本        :1.0
"""
from datetime import datetime

from app.libs.db import db


class Base(db.Model):
    __abstract__ = True
    status = db.Column(db.Integer, default=1, comment="状态:0,1 默认为1")
    create_time = db.Column(
        db.DateTime,
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        comment="创建时间",
    )
    update_time = db.Column(
        db.DateTime,
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        comment="更新时间",
    )

    def __getitem__(self, item):
        # 获取序列化的key的value
        return getattr(self, item)

    def keys(self):
        # 获取默认字段
        return self.fields

    def hide(self, *keys):
        # 隐藏返回的字段
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        # 添加需要返回的字段
        for key in keys:
            self.fields.append(key)
        return self
