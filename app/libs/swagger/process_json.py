#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :processJson.py
@说明        :swagger 转换httprunner后本地文件写入
@时间        :2020/11/13 10:19:36
@作者        :Leo
@版本        :1.0
"""

import json

from app.libs.httprunner import logger


def get_json(path, field=""):
    """
    获取json文件中的值，data.json和res.json可共用
    :param path:
    :param field:
    :return:
    """
    with open(path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
        if field:
            data = json_data.get(field)
            return data
        else:
            return json_data


def write_data(res, json_path):
    """
    把处理后的参数写入json文件
    :param res:
    :param json_path:
    :return:
    """

    if isinstance(res, dict) or isinstance(res, list):
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, sort_keys=True, indent=4)
            logger.log_info(
                "Interface Params Total：{} ,write to json file successfully!\n".format(
                    len(res)
                )
            )
    else:
        logger.log_error("{} Params is not dict.\n".format(write_data.__name__))
