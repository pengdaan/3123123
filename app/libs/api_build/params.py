#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :params.py
@说明        :
@时间        :2021/03/09 14:20:09
@作者        :Leo
@版本        :1.0
'''


def update_teststeps_params_by_list(testcase_list):
    """
    如果api中没有params，则添加config的params进去，有则使用原来的
    :param testcase_list:
    :return:
    """
    # TODO:config的params合并到每个执行步骤中，达到params公用的效果
    config = testcase_list["testcases"][0]["config"]
    if config["request"].get("params"):
        data = config["request"].get("params")
        for i in testcase_list["testcases"][0]["teststeps"]:
            if "params" not in i["request"]:
                i["request"]["params"] = data
            else:
                d1 = i["request"]["params"]
                d3 = dict(data, **d1)
                i["request"]["params"] = d3
    if config.get("validate"):
        for i in testcase_list["testcases"][0]["teststeps"]:
            if i.get("validate"):
                validates = i["validate"] + config["validate"]
                i["validate"] = validates
            else:
                i["validate"] = config["validate"]


def update_teststeps_params(testcase_list):
    """
    如果api中没有params，则添加config的params进去，有则使用原来的
    :param testcase_list:
    :return:
    """
    # TODO:config的params合并到每个执行步骤中，达到params公用的效果
    config = testcase_list[0]["config"]
    if config["request"].get("params"):
        data = config["request"].get("params")
        if "params" not in testcase_list[0]["teststeps"][0]["request"]:
            testcase_list[0]["teststeps"][0]["request"]["params"] = data
        else:
            d1 = testcase_list[0]["teststeps"][0]["request"]["params"]
            d3 = dict(data, **d1)
            testcase_list[0]["teststeps"][0]["request"]["params"] = d3
