#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :func_name.py
@说明        :
@时间        :2021/03/01 15:01:17
@作者        :Leo
@版本        :1.0
"""

import re


def get_func_name(data):
    """[summary]
    获取api场景中所使用到的函数

    Args:
        data ([type]): [description]

    Returns:
        [type]: [description]
    """
    func_lists = []
    if "request" in data:
        api_request = data["request"]
        if "json" in api_request:
            for v in api_request["json"].values():
                if isinstance(v, str):
                    func_list = re.findall(r"(?<=\$\{)(.*)(?=\()", v)
                    func_lists = func_lists + func_list
        if "data" in api_request:
            for v in api_request["data"].values():
                if isinstance(v, str):
                    func_list = re.findall(r"(?<=\$\{)(.*)(?=\()", v)
                    func_lists = func_lists + func_list

        if "params" in api_request:
            for v in api_request["params"].values():
                if isinstance(v, str):
                    func_list = re.findall(r"(?<=\$\{)(.*)(?=\()", v)
                    func_lists = func_lists + func_list

        if "variables" in data:
            if len(data["variables"]) > 0:
                for i in data["variables"]:
                    for v in i.values():
                        if isinstance(v, str):
                            func_list = re.findall(r"(?<=\$\{)(.*)(?=\()", v)
                            func_lists = func_lists + func_list

        if "setup_hooks" in data:
            if len(data["setup_hooks"]) > 0:
                for i in data["setup_hooks"]:
                    if isinstance(i, str):
                        func_list = re.findall(r"(?<=\$\{)(.*)(?=\()", i)
                        func_lists = func_lists + func_list

        if "teardown_hooks" in data:
            if len(data["teardown_hooks"]) > 0:
                for i in data["teardown_hooks"]:
                    if isinstance(i, str):
                        func_list = re.findall(r"(?<=\$\{)(.*)(?=\()", i)
                        func_lists = func_lists + func_list

    new_list = list(set(func_lists))
    fun_names = ",".join(new_list)
    return fun_names
