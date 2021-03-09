#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :setting.py
@说明        :项目运行配置文件
@时间        :2020/08/05 20:30:57
@作者        :Leo
@版本        :1.0
"""
import os


class BaseConfig:
    """[summary]
    基础配置类
    """

    SECERET_KEY = os.getenv("SECERET_KEY", "bluemoon")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = True
    # session设置
    SESSION_KEY = "app"
    #
    IGNORE_CHECK_LOGIN_URLS = ["^/static", "^/favicon.ico"]
    # optional pooling params
    FLASK_PIKA_POOL_PARAMS = {"pool_size": 8, "pool_recycle": 600}
    # 日志路径
    LOG_PATH = ""


class DevelopmentConfig(BaseConfig):
    FLASK_PIKA_PARAMS = {
        "host": "127.0.0.1",  # amqp.server.com
        "username": "guest",  # convenience param for username
        "password": "guest",  # convenience param for password
        "port": 5672,  # amqp server port
    }
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:8852075@127.0.0.1/Luna?charset=utf8&autocommit=true"
    #  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.240.82:31989/luna?charset=utf8&autocommit=true'
    # 测试环境[用于内侧]
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.240.82:31004/Luna?charset=utf8&autocommit=true'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.240.82:31522/Luna?charset=utf8&autocommit=true'
    CELERY_RESULT_MQTT = "amqp://guest:guest@127.0.0.1:5672"


class ProductionConfig(BaseConfig):
    FLASK_PIKA_PARAMS = {
        "host": "192.168.240.82",  # amqp.server.com
        "username": "guest",  # convenience param for username
        "password": "guest",  # convenience param for password
        "port": 30457,  # amqp server port
    }
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@192.168.240.82:31989/luna?charset=utf8&autocommit=true"
    CELERY_RESULT_MQTT = "amqp://guest:guest@192.168.240.82:30457"


config = {"development": DevelopmentConfig, "production": ProductionConfig}
