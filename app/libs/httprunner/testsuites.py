#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :testsuites.py
@说明        :testsuites组装
@时间        :2021/02/22 16:48:26
@作者        :Leo
@版本        :1.0
"""
import json
from app.models.parameter import Parameters


def _parameters(case_id):
    lists = []
    desc = {}
    parameters = Parameters.query.filter_by(case_id=case_id, status=1).all()
    if len(parameters) > 0:
        for i in parameters:
            parameters_info = json.loads(i.parameters)
            lists = lists + parameters_info["parameters"]
            desc.update(parameters_info["desc"])
        _parameters = {"parameters": lists, "desc": desc}
        # print(_parameters)
        return _parameters
    else:
        return None


def get_case_parameters(case_id):
    this_arameters = {}
    parameters = _parameters(case_id)
    if parameters is not None:
        parameter_list = parameters
        if len(parameter_list) > 0:
            parameter_data = parameter_list["parameters"]
            for i in parameter_data:
                for key, value in i.items():
                    if value.find("$") == 1:
                        this_arameters.update(i)
                    if "-" in key:
                        new_value = []
                        values = value.split("|")
                        for v in values:
                            new_value.append(eval(v))
                        new_dict = {key: new_value}
                        this_arameters.update(new_dict)
                    else:
                        values = value.split(",")
                        target_values = []
                        try:
                            for i in values:
                                target_values.append(json.loads(i))
                        except Exception:
                            target_values = values
                        new_dict = {key: target_values}
                        this_arameters.update(new_dict)
    # print("this_arameters-----》",this_arameters)
    return this_arameters


def add_testsuites(case_list, case_id):
    case_parameters = get_case_parameters(case_id)
    # print('case_parameters:------>',case_parameters)
    testsuites = {
        "project_mapping": case_list["project_mapping"],
        "testsuites": [
            {
                "config": case_list["testcases"][0]["config"],
                "testcases": {
                    "testcase_suites": {
                        "variables": {},  # 该字段暂时无用
                        "testcase": "testcase_suites",  # 该字段暂时无用
                        "parameters": case_parameters,
                        "testcase_def": {
                            "config": case_list["testcases"][0]["config"],
                            "teststeps": case_list["testcases"][0]["teststeps"],
                        },
                    },
                },
            }
        ],
    }
    return testsuites
