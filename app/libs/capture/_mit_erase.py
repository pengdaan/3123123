#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :_mit_erase.py
@说明        :
@时间        :2021/04/23 14:00:53
@作者        :Leo
@版本        :1.0
'''
from app.libs.capture import _request


def _desc(data):
    _desc_data = {}
    for k, v in data.items():
        _desc_data.update({k: ""})
    return _desc_data


def api_body(data):
    try:
        return eval(data)
    except Exception:
        return ''


def _api_json(name, url, method, headers, _dheaders, params, _dparams, body):
    _request.Base_Json_Data_Request["name"] = name
    _request.Base_Json_Data_Request["request"]["url"] = url
    _request.Base_Json_Data_Request["request"]["method"] = method
    _request.Base_Json_Data_Request["request"]["headers"] = headers
    _request.Base_Json_Data_Request["request"]["params"] = params
    _request.Base_Json_Data_Request["desc"]["header"] = _dheaders
    _request.Base_Json_Data_Request["desc"]["params"] = _dparams
    _request.Base_Json_Data_Request["request"]["json"] = body
    return _request.Base_Json_Data_Request


def _api_get_json(name, url, method, headers, _dheaders, params, _dparams):
    _request.Base_Get_Data_Request["name"] = name
    _request.Base_Get_Data_Request["request"]["url"] = url
    _request.Base_Get_Data_Request["request"]["method"] = method
    _request.Base_Get_Data_Request["request"]["headers"] = headers
    _request.Base_Get_Data_Request["request"]["params"] = params
    _request.Base_Get_Data_Request["desc"]["header"] = _dheaders
    _request.Base_Get_Data_Request["desc"]["params"] = _dparams
    return _request.Base_Get_Data_Request