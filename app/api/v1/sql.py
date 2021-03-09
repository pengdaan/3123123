#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :sql.py
@说明        :
@时间        :2020/08/14 15:43:59
@作者        :Leo
@版本        :1.0
"""

import records
from app.libs.code import Sucess

from app.libs.auth import auth_jwt
from app.libs.mysql import MYSQL
from app.libs.redprint import Redprint
from app.models.sqlconfig import Sql_Config as SqlConfig
from app.validators.sql_validator import (
    addSQLForm,
    connectSQLForm,
    searchSQLForm,
    updateSQLForm,
)

api = Redprint("sql")


@api.route("/add", methods=["POST"])
@auth_jwt
def add_sql_config():
    sqlData = addSQLForm().validate_for_api()
    SqlConfig.add_sql_config(
        sqlData.name.data,
        sqlData.host.data,
        sqlData.username.data,
        sqlData.password.data,
        sqlData.database.data,
        sqlData.port.data,
        sqlData.pro_id.data,
    )
    return Sucess()


@api.route("/del/<int:id>", methods=["GET"])
@auth_jwt
def del_sql_config(id):
    SqlConfig.query.filter_by(id=id, status=1).first_or_404("SqlId")
    SqlConfig.del_sql_config(id)
    return Sucess()


@api.route("/detail/<int:id>", methods=["GET"])
@auth_jwt
def sql_config_detail(id):
    """
    根据id获取配置详情
    :param id:
    :return:
    """
    res = SqlConfig.query.filter_by(id=id, status=1).first_or_404("SqlId")
    result = {
        "id": res.id,
        "name": res.name,
        "host": res.host,
        "database": res.database,
        "username": res.username,
        "password": res.password,
        "port": res.port,
        "pro_id": res.pro_id,
    }
    return Sucess(data=result)


@api.route("/update", methods=["POST"])
@auth_jwt
def sql_config_update():
    """
    根据id获取配置详情
    :param id:
    :return:
    """
    sqlData = updateSQLForm().validate_for_api()
    SqlConfig.update_sql_config(
        sqlData.id.data,
        sqlData.name.data,
        sqlData.host.data,
        sqlData.username.data,
        sqlData.password.data,
        sqlData.database.data,
        sqlData.port.data,
    )
    return Sucess()


@api.route("/list/<int:pro_id>", methods=["GET"])
@auth_jwt
def sql_config_List(pro_id):
    """
    根据id获取配置详情
    :param id:
    :return:
    """
    res = SqlConfig.is_empty_sql_config_list(pro_id)
    return Sucess(data=res)


@api.route("/connect", methods=["POST"])
def sql_cconnection():
    """
    执行数据库查询
    :param id:
    :return:
    """
    sqlData = connectSQLForm().validate_for_api()
    result = SqlConfig.query.filter_by(id=sqlData.id.data).first_or_404("SqlId")
    db_connect = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(
        result.username, result.password, result.host, result.port, result.database
    )
    db = records.Database(db_connect)
    try:
        rows = db.query(sqlData.data.data)
        db.close()
        res = rows.all(as_dict=True)
        return Sucess(data=res)
    except Exception as e:
        return Sucess(code=1006, data=str(e))


@api.route("/debug/<int:id>", methods=["GET"])
@auth_jwt
def sql_debug_cconnection(id):
    """
    debug 数据库连接
    :param id:
    :return:
    """
    res = SqlConfig.query.filter_by(id=id).first_or_404("SqlId")
    sql = MYSQL(
        host=res.host,
        user=res.username,
        pwd=res.password,
        db=res.database,
        port=res.port,
    )
    if sql.status:
        sql.Close()
        return Sucess(msg="数据库连接成功")
    else:
        return Sucess(code=-1, msg=str(sql.error))


@api.route("/search", methods=["POST"])
@auth_jwt
def search_sql_config_List():
    """
    根据关键字查询数据里
    :param id:
    :return:
    """
    sqlData = searchSQLForm().validate_for_api()
    pro_id = sqlData.pro_id.data
    kw = sqlData.kw.data
    if not kw:
        res = SqlConfig.is_empty_sql_config_list(pro_id)
    else:
        res = SqlConfig.search_sql_list(pro_id, kw)
    return Sucess(data=res)
