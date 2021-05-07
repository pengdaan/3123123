#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :variable.py
@说明        :处理variables
@时间        :2020/10/09 14:37:26
@作者        :Leo
@版本        :1.0
"""
from app.models.variable import Variable


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


def update_project_persistence(pro_id, api_id, data):
    """[summary]
    更新持久化的参数
    Args:
        pro_id ([type]): [description]
        api_id ([type]): [description]
        data ([type]): [description]
    """
    target_variable = Variable.get_variable_list(pro_id, api_id)
    if len(target_variable):
        for i in target_variable:
            if i['name'] in data[0]['out']:
                Variable.update_variable_status(i["id"], 1, data[0]['out'][i['name']], i['name'])


def add_persistence_by_api(pro_id, data):
    """[summary]
    api 执行前,persistence写入到variables中
    Args:
        data ([type]): [description]
    """
    for i in data:
        if 'headers' in i['request']:
            for h_key, h_value in i['request']['headers'].items():
                if "Per" in str(h_value):
                    _persistence = str(h_value).replace('Per_', '')
                    _persistence_detail = Variable.get_variable_detail(pro_id, _persistence)
                    if 'data' in _persistence_detail and _persistence_detail['data']:
                        try:
                            i['request']['headers'].update({h_key: eval(_persistence_detail['data'])})
                        except Exception:
                            i['request']['headers'].update({h_key: _persistence_detail['data']})
        if 'json' in i['request']:
            for j_key, j_value in i['request']['json'].items():
                if "Per" in str(j_value):
                    _persistence = str(j_value).replace('Per_', '')
                    _persistence_detail = Variable.get_variable_detail(pro_id, _persistence)
                    if 'data' in _persistence_detail and _persistence_detail['data']:
                        try:
                            i['request']['json'].update({j_key: eval(_persistence_detail['data'])})
                        except Exception:
                            i['request']['json'].update({j_key: _persistence_detail['data']})
        if 'params' in i['request']:
            for p_key, p_value in i['request']['params'].items():
                if "Per" in str(p_value):
                    _persistence = str(p_value).replace('Per_', '')
                    _persistence_detail = Variable.get_variable_detail(pro_id, _persistence)
                    if 'data' in _persistence_detail and _persistence_detail['data']:
                        try:
                            i['request']['params'].update({p_key: eval(_persistence_detail['data'])})
                        except Exception:
                            i['request']['params'].update({p_key: _persistence_detail['data']})
        if 'data' in i['request']:
            for d_key, d_value in i['request']['data'].items():
                if "Per" in str(d_value):
                    _persistence = str(d_value).replace('Per_', '')
                    _persistence_detail = Variable.get_variable_detail(pro_id, _persistence)
                    if 'data' in _persistence_detail and _persistence_detail['data']:
                        try:
                            i['request']['data'].update({d_key: eval(_persistence_detail['data'])})
                        except Exception:
                            i['request']['data'].update({d_key: _persistence_detail['data']})

