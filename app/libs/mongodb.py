#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :mongodb.py
@说明        :抓包数据处理
@时间        :2021/04/22 09:22:55
@作者        :Leo
@版本        :1.0
'''
from pymongo import MongoClient
from flask import app
from app.config.setting import config


class LunaMongo(object):
    def __init__(self, address, port, database):
        self.conn = MongoClient(host=address, port=port)
        self.db = self.conn[database]

    def get_state(self):
        return self.conn is not None and self.db is not None

    def find(self, col, condition, column=None):
        """[summary]
        Args:
            col ([str]): [表名]
            condition ([type]): [查询的字段]
            column ([type], optional): [查询指定字段的数据,将要返回的字段对应值设置为 1]. Defaults to None.

        Returns:
            [list]: [返回查询集合]
        """
        if self.get_state():
            if column is None:
                res = self.db[col].find(condition)
            else:
                res = self.db[col].find(condition, column)
        else:
            res = None
        self.close()
        return res

    def find_one(self, col, condition, column=None):
        """[summary]
        Args:
            col ([type]): [表名]
            condition ([type]): [查询的字段]
            column ([type], optional): [查询指定字段的数据,将要返回的字段对应值设置为 1]. Defaults to None.

        Returns:
            [dict]: [返回查询集合]
        """
        if self.get_state():
            if column is None:
                res = self.db[col].find_one(condition)
            else:
                res = self.db[col].find_one(condition, column)
        else:
            res = None
        self.close()
        return res

    def close(self):
        return self.conn.close()


def initialDB():
    env = config[app.get_env()]
    mongodb = LunaMongo(address=env.MONGO_DB_URI['address'], port=env.MONGO_DB_URI['port'], database=env.MONGODB)
    return mongodb
