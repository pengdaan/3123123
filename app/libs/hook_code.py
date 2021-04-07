#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :hook_code.py
@说明        :
@时间        :2021/03/04 15:14:51
@作者        :Leo
@版本        :1.0
"""

BASE_CODE_HOOK_SETUP = """
# -*- encoding: utf-8 -*-
# write you code
# 内容调试成功后,请删除调试代码

def hook_setup(*args):
    pass

    """

BASE_CODE_HOOK_TEARDOWN = """
# write you code
# 内容调试成功后,请删除调试代码

def hook_teardown(*args):
    pass

    """

BASE_CODE_HOOK_SQL = """
# write you code
# 内容调试成功后,请删除调试代码

def create():
    pass

    """

BASE_SUMMARYS = {
    "success": True,
    "stat": {
        "testcases": {"total": 0, "success": 0, "fail": 0},
        "teststeps": {
            "total": 0,
            "failures": 0,
            "errors": 0,
            "skipped": 0,
            "expectedFailures": 0,
            "unexpectedSuccesses": 0,
            "successes": 0,
        },
    },
    "time": {"start_at": 0, "duration": 0},
    "platform": {
        "httprunner_version": "2.5.7",
        "python_version": "CPython 3.7.2",
        "platform": "Darwin-17.6.0-x86_64-i386-64bit",
    },
    "details": [],
    "html_report_name": "聚合报告页",
}
