#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :mq.py
@说明        :
@时间        :2020/08/19 17:00:52
@作者        :Leo
@版本        :1.0
"""

# -*- coding: utf-8 -*-

from flask_pika import Pika

fpika = Pika()


def register_RabbitMq(app):
    fpika.init_app(app)
