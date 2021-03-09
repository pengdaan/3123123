#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :mysql.py
@说明        :
@时间        :2020/08/19 13:41:22
@作者        :Leo
@版本        :1.0
"""

import pymysql

__author__ = "leo"


class MYSQL:
    def __init__(self, host, user, pwd, db, port):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port
        self.status = False
        self.error = None

        self._conn = self.GetConnect()
        if self._conn:
            self.status = True
            self._cur = self._conn.cursor()
        else:
            self.status = False

    # 连接数据库
    def GetConnect(self):
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                database=self.db,
                port=self.port,
            )
        except Exception as err:
            # print ("连接数据库失败, %s" % err)
            self.error = "连接数据库失败, %s" % err
        else:
            print("数据库连接成功")
            return conn

    # 执行查询
    def ExecQuery(self, sql):
        res = ""
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
        except Exception as err:
            res = "查询失败,, %s" % err
            return res
        else:
            return res

    # 执行非查询类语句
    def ExecNonQuery(self, sql):
        flag = False
        try:
            self._cur.execute(sql)
            self._conn.commit()
            flag = True
        except Exception as err:
            flag = False
            self._conn.rollback()
            print("执行失败, %s" % err)
        else:
            return flag

    # 获取连接信息
    def GetConnectInfo(self):
        print("连接信息：")
        print("服务器:%s , 用户名:%s , 数据库:%s " % (self.host, self.user, self.db))

    # 关闭数据库连接
    def Close(self):
        if self._conn:
            try:
                if type(self._cur) == "object":
                    self._cur.close()
                if type(self._conn) == "object":
                    self._conn.close()
            except Exception as e:
                raise ("关闭异常, %s,%s" % (type(self._cur), type(self._conn)))
