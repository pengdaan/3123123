#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :_request.py
@说明        :
@时间        :2021/04/01 13:55:01
@作者        :Leo
@版本        :1.0
"""

Base_Form_Data_Request = {
    "name": "",
    "times": 1,
    "skipUnless": True,
    "request": {
        "url": "",
        "method": "",
        "verify": False,
        "headers": {},
        "params": {},
        "data": {},
    },
    "desc": {"header": {}, "params": {}, "data": {}, "variables": {}, "extract": {}},
}


Base_Json_Data_Request = {
    "name": "",
    "times": 1,
    "skipUnless": True,
    "request": {
        "url": "",
        "method": "",
        "verify": False,
        "headers": {},
        "params": {},
        "json": {},
    },
    "desc": {"header": {}, "data": {}, "params": {}, "variables": {}, "extract": {}},
}


Base_Get_Data_Request = {
    "name": "",
    "times": 1,
    "skipUnless": True,
    "request": {
        "url": "",
        "method": "",
        "verify": False,
        "headers": {},
        "params": {},
    },
    "desc": {"header": {}, "params": {}, "variables": {}, "extract": {}},
}
