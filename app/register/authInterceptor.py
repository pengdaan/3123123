#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :error_handler.py
@说明        :AOP 全局异常处理
@时间        :2020/08/06 23:31:41
@作者        :Leo
@版本        :1.0
"""

import re

from flask import request

from app.config.setting import BaseConfig
from app.libs.code import ServerError
from app.libs.error import APIException, HTTPException


def register_error_headers(app):
    """
    统一拦截处理和统一错误处理
    """

    @app.errorhandler(Exception)
    def custom_error_handler(e):
        if isinstance(e, APIException):
            return e
        if isinstance(e, HTTPException):
            code = e.code
            msg = e.description
            data = 1007
            return APIException(msg, code, data)
        else:
            # 测试环境直接返回报错，不返回异常处理
            if app.config["ENV"] != "development":
                return ServerError()
            else:
                raise e


def TokenFilter(app):
    """[summary]
    认证拦截器
    Args:
        app ([type]): [description]
    """

    @app.before_request
    def before_request():
        ignore_check_login_urls = BaseConfig.IGNORE_CHECK_LOGIN_URLS
        path = request.path
        # 如果是静态文件就不要查询用户信息了
        pattern = re.compile("%s" % "|".join(ignore_check_login_urls))
        if pattern.match(path):
            return

    return
