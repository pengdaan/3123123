#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :variable.py
@说明        :
@时间        :2021/04/20 17:23:35
@作者        :Leo
@版本        :1.0
'''

from app.libs.auth import auth_jwt
from app.libs.code import Sucess, Fail
from app.libs.redprint import Redprint
from app.models.variable import Variable

api = Redprint("variable")
