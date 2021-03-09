#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :code.py
@说明        :
@时间        :2020/08/06 10:57:22
@作者        :Leo
@版本        :1.0
"""

__author__ = "leo"

from app.libs.error import APIException


class parameterException(APIException):
    code = 401
    data = ""
    msg = "invalid parameter"


class Sucess(APIException):
    code = 201
    data = ""
    msg = "success"


class Fail(APIException):
    code = 202
    data = ""
    msg = "fail"


class ServerError(APIException):
    code = 500
    data = ""
    msg = "sorry, we made a mistake !"


class NotFound(APIException):
    code = 404
    data = ""
    msg = "this resource are not found"


class AuthFailed(APIException):
    code = 201
    data = ""
    msg = "authorization failed"
