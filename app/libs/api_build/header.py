#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :header.py
@说明        :
@时间        :2021/03/09 11:47:03
@作者        :Leo
@版本        :1.0
"""


def update_api_header(testList):
    # TPDO 更新config中的header到api中
    # print(testList)
    if isinstance(testList, list):
        data = testList[0]
        if "headers" in data["config"]["request"]:
            config_headers = data["config"]["request"]["headers"]
            if data["teststeps"]:
                for i in data["teststeps"]:
                    if "request" in i:
                        if "headers" in i["request"]:
                            api_headers = i["request"]["headers"]
                            if config_headers:
                                for i in config_headers.keys():
                                    if i not in api_headers:
                                        api_headers[i] = config_headers[i]


def update_case_header(testList):
    # TPDO 更新config中的header到case_api中
    if isinstance(testList, dict):
        data = testList["testcases"][0]
        if "headers" in data["config"]["request"]:
            config_headers = data["config"]["request"]["headers"]
            if data["teststeps"]:
                for i in data["teststeps"]:
                    if "request" in i:
                        if "headers" in i["request"]:
                            api_headers = i["request"]["headers"]
                            if config_headers:
                                for i in config_headers.keys():
                                    if i not in api_headers:
                                        api_headers[i] = config_headers[i]
