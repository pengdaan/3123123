#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :error.py
@说明        :
@时间        :2020/08/06 11:02:39
@作者        :Leo
@版本        :1.0
"""

from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = "sorry, we made a mistake !"
    data = ""

    def __init__(self, msg=None, code=None, data=None, headers=None):
        if code:
            self.code = code
        if data:
            self.data = data
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            code=self.code,
            data=self.data,
            request=request.method + " " + self.get_url_no_param(),
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [("Content-Type", "application/json")]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split("?")
        return main_path[0]
