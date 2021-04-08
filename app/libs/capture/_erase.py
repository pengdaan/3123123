#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :_erase.py
@说明        :
@时间        :2021/04/01 11:25:32
@作者        :Leo
@版本        :1.0
"""
from app.libs.capture import _request
import json


def is_api(data):
    res = [item[key] for item in data for key in item]
    for i in res:
        if "application/json" in i:
            return True
        if "application/x-www-form-urlencoded" in i:
            return True
    else:
        return False


def _header(data, desc=None):
    _api_header = {}
    for i in data:
        if desc:
            _api_header.update({i["name"]: ""})
        else:
            _api_header.update({i["name"]: i["value"]})
    return _api_header


def _params(data, desc=None):
    _api_params = {}
    _api_url = data.split("?")
    if len(_api_url) > 1:
        params_list = data.split("?")[1]
        params_detail = params_list.split("&")
        for i in params_detail:
            if "=" in i:
                s = i.split("=")
                if desc:
                    _api_params.update({s[0]: ""})
                else:
                    _api_params.update({s[0]: s[1]})
    return _api_params


def _api_type(data):
    for item in data:
        for k, v in item.items():
            if "Content-Type" in v:
                if "application/json" in item["value"]:
                    return 1
                if "application/x-www-form-urlencoded" in item["value"]:
                    return 2


def _form_data(name, url, method, headers, _dheaders, params, _dparams, form_data):
    _api_form_data = {}
    if len(form_data.keys()):
        for i in form_data.keys():
            _api_form_data.update({i: ""})
    _request.Base_Form_Data_Request["name"] = name
    _request.Base_Form_Data_Request["request"]["url"] = url
    _request.Base_Form_Data_Request["request"]["method"] = method
    _request.Base_Form_Data_Request["request"]["headers"] = headers
    _request.Base_Form_Data_Request["request"]["params"] = params
    _request.Base_Form_Data_Request["request"]["data"] = form_data
    _request.Base_Form_Data_Request["desc"]["header"] = _dheaders
    _request.Base_Form_Data_Request["desc"]["params"] = _dparams
    _request.Base_Form_Data_Request["desc"]["data"] = _api_form_data
    # print('form:----------->', _request.Base_Form_Data_Request)
    return _request.Base_Form_Data_Request


def _api_json(name, url, method, headers, _dheaders, params, _dparams, body):
    _request.Base_Json_Data_Request["name"] = name
    _request.Base_Json_Data_Request["request"]["url"] = url
    _request.Base_Json_Data_Request["request"]["method"] = method
    _request.Base_Json_Data_Request["request"]["headers"] = headers
    _request.Base_Json_Data_Request["request"]["params"] = params
    _request.Base_Json_Data_Request["desc"]["header"] = _dheaders
    _request.Base_Json_Data_Request["desc"]["params"] = _dparams
    if len(body) > 0:
        if body[0] == "[]":
            _request.Base_Json_Data_Request["request"]["json"] = []
        if body[0] == "{}":
            _request.Base_Json_Data_Request["request"]["json"] = {}
        else:
            try:
                _request.Base_Json_Data_Request["request"]["json"] = json.loads(body[0])
            except Exception:
                _request.Base_Json_Data_Request["request"]["json"] = body[0]
    else:
        _request.Base_Json_Data_Request["request"]["json"] = ""
    # print('json-----------》', _request.Base_Json_Data_Request)
    return _request.Base_Json_Data_Request


def _api_get_json(name, url, method, headers, params, _dheaders, _dparams):
    _request.Base_Get_Data_Request["name"] = name
    _request.Base_Get_Data_Request["request"]["url"] = url
    _request.Base_Get_Data_Request["request"]["method"] = method
    _request.Base_Get_Data_Request["request"]["headers"] = headers
    _request.Base_Get_Data_Request["request"]["params"] = params
    _request.Base_Get_Data_Request["desc"]["header"] = _dheaders
    _request.Base_Get_Data_Request["desc"]["params"] = _dparams
    # print("get ---------------》", _request.Base_Get_Data_Request)
    return _request.Base_Get_Data_Request
