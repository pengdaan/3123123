#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :redprint.py
@说明        :红图注册
@时间        :2020/08/05 21:22:57
@作者        :Leo
@版本        :1.0
"""


class Redprint:
    def __init__(self, name):
        """[summary]
        红图对象,使用红图代替蓝图
        Args:
            name ([str]): [红图的名字]
        """
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f

        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = "/" + self.name
            for f, rule, options in self.mound:
                endpoint = self.name + "+" + options.pop("endpoint", f.__name__)
                bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
