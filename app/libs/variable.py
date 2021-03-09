#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :variable.py
@说明        :处理variables
@时间        :2020/10/09 14:37:26
@作者        :Leo
@版本        :1.0
"""


def get_all_key_by_dict(data):
    keys = []
    if isinstance(data, list) and len(data) > 0:
        for i in data:
            keys = keys + (list(i.keys()))
    keys = sorted(set(keys), key=keys.index)
    return keys


def update_all_key_by_dict(list, keys):
    index = []
    for i, dic in enumerate(list):
        for key in keys:
            if key in dic:
                index.append(i)
    return index


def update_list(list, index):
    new_list = list
    if len(index) > 0:
        for i in index:
            del new_list[i]
    return new_list
