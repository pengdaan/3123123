#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :request_header.py
@说明        :规范请求头
@时间        :2020/08/05 22:51:23
@作者        :Leo
@版本        :1.0
"""
from flask import abort, request


def register_headers(app):
    """
    规范请求头信息
    :param app:
    :return:
    """

    @app.before_request
    def api_specification():
        if request.method == "POST":
            if (
                "Content-Type" not in request.headers
                or "application/json" not in request.headers["Content-Type"]
            ):
                abort(412)
