#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :db.py
@说明        :重载sqlalchemy的部分方法
@时间        :2020/08/06 15:19:12
@作者        :Leo
@版本        :1.0
"""

from contextlib import contextmanager

from flask_sqlalchemy import BaseQuery
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from app.libs.code import NotFound, Sucess


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    # def filter_by(self, **kwargs):
    #     if 'status' not in kwargs.keys():
    #         kwargs['status'] = 1
    #     return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident, key):
        rv = self.get(ident)
        if not rv:
            raise NotFound(msg="%s is not exist" % key)
        return rv

    def first_or_404(self, key):
        rv = self.first()
        if key == "token":
            if not rv:
                raise Sucess(msg="%s has expired" % key, code=4001)
        else:
            if not rv:
                raise NotFound(msg="%s is not exist" % key)
        return rv


db = SQLAlchemy(query_class=Query)
