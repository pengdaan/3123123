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
    responseCode = 2005
    data = ""
    msg = "invalid parameter"


class Sucess(APIException):
    responseCode = 2000
    data = ""
    msg = "success"


class Fail(APIException):
    responseCode = 2004
    data = ""
    msg = "success"


class ServerError(APIException):
    responseCode = 500
    data = ""
    msg = "sorry, we made a mistake !"


class NotFound(APIException):
    responseCode = 404
    data = ""
    msg = "this resource are not found"


class AuthFailed(APIException):
    responseCode = 401
    data = ""
    msg = "authorization failed"
