#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :logger.py
@说明        :
@时间        :2021/03/04 13:48:21
@作者        :Leo
@版本        :1.0
"""

import logging
import sys

from pathlib import Path
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


def register_configure_logging(app):
    """配置日志"""
    path = Path(app.config["LOG_PATH"])
    if not path.exists():
        path.mkdir(parents=True)
    log_name = Path(path, "luna.log")
    logging.basicConfig(handlers=[InterceptHandler(level="INFO")], level="INFO")
    logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])  # 配置日志到标准输出流
    logger.add(
        log_name, rotation="500 MB", encoding="utf-8", colorize=False, level="INFO"
    )  # 配置日志到输出到文件
