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
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


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
    # 日志路径
    LOG_PATH = ""
    # mongodb数据库
    MONGODB = "bmtest"
    # 配置时区
    SCHEDULER_TIMEZONE = "Asia/Shanghai"


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:8852075@127.0.0.1/luna?charset=utf8&autocommit=true"
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.240.82:31989/luna?charset=utf8&autocommit=true'
    # 调度器开关
    SCHEDULER_API_ENABLED = False
    # ------持久化位置-------
    SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)}
    # 线程池配置
    SCHEDULER_EXECUTORS = {
        "default": ThreadPoolExecutor(20),
        "processpool": ProcessPoolExecutor(5),
    }
    # 抓包MONGO配置
    MONGO_DB_URI = {"address": "192.168.240.84", "port": 31965}


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@192.168.240.82:31989/luna?charset=utf8&autocommit=true"
    # 调度器开关
    SCHEDULER_API_ENABLED = False
    # ------持久化位置-------
    SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)}
    # 线程池配置
    SCHEDULER_EXECUTORS = {
        "default": ThreadPoolExecutor(20),
        "processpool": ProcessPoolExecutor(5),
    }
    # 抓包MONGO配置
    MONGO_DB_URI = {"address": "192.168.240.84", "port": 31965}


config = {"development": DevelopmentConfig, "production": ProductionConfig}
