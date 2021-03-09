#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :swagger.py
@说明        :swagger导入
@时间        :2020/11/16 16:57:27
@作者        :Leo
@版本        :1.0
"""

from app.libs.code import Sucess
from app.libs.redprint import Redprint
from app.libs.swagger.swagger import AnalysisJson
from app.validators.swagger_validator import SwaggerBaseForm

api = Redprint("swagger")


@api.route("/add", methods=["POST"])
def addSuagger():
    swaggerData = SwaggerBaseForm().validate_for_api()
    res = AnalysisJson(
        swaggerData.url.data,
        swaggerData.pro_id.data,
        swaggerData.add_type.data,
        swaggerData.user_id.data,
    ).retrieve_data()

    if res is None:
        return Sucess()
