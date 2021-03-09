#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :run.py
@说明        :用例执行
@时间        :2020/08/12 17:31:01
@作者        :Leo
@版本        :1.0
"""

__author__ = "leo"

import datetime
import importlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
import types
from ast import literal_eval
from functools import reduce
from urllib.parse import urlparse

import requests
import yaml
from bs4 import BeautifulSoup
from flask._compat import text_type
from requests.cookies import RequestsCookieJar

from app.libs.decimal_encoder import JSONEncoder
from app.libs.httprunner.api import HttpRunner
from app.libs.httprunner.parser import ERROR, LazyString
from app.libs.httprunner.testsuites import add_testsuites
from app.libs.variable import get_all_key_by_dict, update_all_key_by_dict, update_list
from app.models.config import Config
from app.models.hook import Hook
from app.models.report import Report
from app.libs.api_build import header
from app.libs.api_build import params
from app.libs.api_summary import summary as luna_summary


def parse_host(ip, api):

    if not isinstance(ip, list):
        return api
    if not api:
        return api
    try:
        parts = urlparse(api["request"]["url"])
    except KeyError:
        parts = urlparse(api["request"]["base_url"])
    host = parts.netloc
    if host:
        for content in ip:
            content = content.strip()
            if host in content and not content.startswith("#"):
                ip = re.findall(
                    r"\b(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b",
                    content,
                )
                if ip:
                    if "headers" in api["request"].keys():
                        api["request"]["headers"]["Host"] = host
                    else:
                        api["request"].setdefault("headers", {"Host": host})
                    try:
                        api["request"]["url"] = api["request"]["url"].replace(
                            host, ip[-1]
                        )
                    except KeyError:
                        api["request"]["base_url"] = api["request"]["base_url"].replace(
                            host, ip[-1]
                        )
    return api


def is_function(tup):
    """Takes (name, object) tuple, returns True if it is a function."""
    name, item = tup
    return isinstance(item, types.FunctionType)


def is_variable(tup):
    """Takes (name, object) tuple, returns True if it is a variable."""
    name, item = tup
    if callable(item):
        # function or class
        return False

    if isinstance(item, types.ModuleType):
        # imported module
        return False

    if name.startswith("_"):
        # private property
        return False

    return True


class FileLoader(object):
    @staticmethod
    def dump_yaml_file(yaml_file, data):
        """dump yaml file"""
        with io.open(yaml_file, "w", encoding="utf-8") as stream:
            yaml.dump(
                data,
                stream,
                indent=4,
                default_flow_style=False,
                encoding="utf-8",
                allow_unicode=True,
            )

    @staticmethod
    def dump_json_file(json_file, data):
        """dump json file"""
        with io.open(json_file, "w", encoding="utf-8") as stream:
            json.dump(
                data, stream, indent=4, separators=(",", ": "), ensure_ascii=False
            )

    @staticmethod
    def dump_python_file(python_file, data):
        """dump python file"""
        with io.open(python_file, "w", encoding="utf-8") as stream:
            stream.write(data)

    @staticmethod
    def dump_binary_file(binary_file, data):
        """dump file"""
        with io.open(binary_file, "wb") as stream:
            stream.write(data)

    @staticmethod
    def load_python_module(file_path):
        """load python module.

        Args:
            file_path: python path

        Returns:
            dict: variables and functions mapping for specified python module

                {
                    "variables": {},
                    "functions": {}
                }

        """
        debugtalk_module = {"variables": {}, "functions": {}}

        sys.path.insert(0, file_path)

        module = importlib.import_module("debugtalk")
        # 修复重载bug
        importlib.reload(module)
        sys.path.pop(0)
        for name, item in vars(module).items():
            if is_function((name, item)):
                debugtalk_module["functions"][name] = item
            elif is_variable((name, item)):
                if isinstance(item, tuple):
                    continue
                debugtalk_module["variables"][name] = item
            else:
                pass

        return debugtalk_module


def parse_tests(
    testcases, project, case_id, debugtalk=None, name=None, config=None, type=None
):
    """get blocusts case structure
    testcases: list
    config: none or dict
    debugtalk: dict
    """
    if debugtalk is None:
        refs = {
            "env": {},
            "def-api": {},
            "def-testcase": {},
        }
    else:
        refs = {"env": {}, "def-api": {}, "def-testcase": {}, "debugtalk": debugtalk}
    testset = {
        "config": {
            "name": testcases[-1]["name"],
            "variables": [],
        },
        "teststeps": testcases,
    }
    if config:
        if "parameters" in config.keys():
            for content in config["parameters"]:
                for key, value in content.items():
                    try:
                        content[key] = eval(value.replace("\n", ""))
                    except Exception as e:
                        content[key] = value
        testset["config"] = config
    if name:
        testset["config"]["name"] = name
    global_variables = []
    if case_id:
        if not testset["config"].get("variables"):
            testset["config"]["variables"] = global_variables
        else:
            testset["config"]["variables"].extend(global_variables)

        testset["config"]["refs"] = refs
    else:
        if not testset["config"].get("variables"):
            testset["config"]["variables"] = global_variables
        else:
            testset["config"]["variables"].extend(global_variables)
        testset["config"]["refs"] = refs
    return testset


# def load_debugtalk1(project_id):
#     """import debugtalk.py in sys.path and reload
#         project: int
#     """
#     # debugtalk.py
#     code = (Hook.query.filter_by(pro_id=project_id).first_or_404('Code')).code
#     file_path = os.path.join(tempfile.mkdtemp(prefix='FasterRunner'),
#                              "debugtalk.py")
#     FileLoader.dump_python_file(file_path, code)
#     debugtalk = FileLoader.load_python_module(os.path.dirname(file_path))
#     shutil.rmtree(os.path.dirname(file_path))
#     return debugtalk


def load_debugtalk(project_id, apiIds):
    """import debugtalk.py in sys.path and reload
    project: int
    """
    # debugtalk.py
    codes = ""
    ProCode = Hook.query.filter_by(pro_id=project_id, api_id=None).all()
    if len(ProCode) > 0:
        for i in ProCode:
            codes = codes + i.code
    if isinstance(apiIds, list):
        for i in apiIds:
            api_codes = Hook.query.filter_by(api_id=i).all()
            if len(api_codes) > 0:
                for i in api_codes:
                    codes = codes + i.code
    else:
        if apiIds is not None:
            api_codes = Hook.query.filter_by(api_id=apiIds).all()
            if len(api_codes) > 0:
                for i in api_codes:
                    codes = codes + i.code
    file_path = os.path.join(tempfile.mkdtemp(prefix="LunaRunner"), "debugtalk.py")
    FileLoader.dump_python_file(file_path, codes)
    # print('Code 集合',codes)
    debugtalk = FileLoader.load_python_module(os.path.dirname(file_path))
    shutil.rmtree(os.path.dirname(file_path))
    return debugtalk


def debug_api(
    apiIds,
    api,
    project,
    case_id,
    name=None,
    config=None,
    status=None,
    run_type=None,
    executor=None,
):
    """debug api
    api :dict or list
    project: int
    """
    try:
        # testcases
        if isinstance(api, dict):
            """
            case scripts or teststeps
            """
            api = [api]
        testcase_list = [
            parse_tests(
                api,
                project,
                case_id,
                load_debugtalk(project, apiIds),
                name=name,
                config=config,
            )
        ]
        kwargs = {"failfast": False}
        runner = HttpRunner(**kwargs)
        project_mapping = add_project_mapping(testcase_list)
        if status == 1:
            # case运行模式
            testcase_list = {
                "project_mapping": project_mapping,
                "testcases": testcase_list,
            }
            header.update_case_header(testcase_list)
            testcase_list = add_sql_config(testcase_list)
            params.update_teststeps_params_by_list(testcase_list)
            testcase_list = luna_summary.out_put_data(testcase_list, project_mapping, type=1)
            print("我这里开始数据装载---->", testcase_list)
            testsuites = add_testsuites(testcase_list, case_id)
            runner.run(testsuites)
            in_out = runner.get_vars_out()
            if run_type == 1:
                # case运行模式的debug模式
                summary = luna_summary.apis_result(runner._summary, in_out)
                return summary
            else:
                # case运行模式的case
                summary = luna_summary.parse_summary(runner._summary)
                return luna_summary.save_summary(
                    name=name, summary=summary, project=project, executor=executor
                )

        elif status == 2:
            # 性能运行模式
            testcase_list = [
                parse_tests(api, project, case_id, name=name, config=config)
            ]
            return testcase_list
        else:
            # 单个api运行模式
            # print('testcase_list', testcase_list)
            header.update_api_header(testcase_list)
            params.update_teststeps_params(testcase_list)
            testcase_list = update_teststeps_validate(testcase_list)
            testcase_list = luna_summary.out_put_data(testcase_list, project_mapping)
            testcase_list = {
                "project_mapping": project_mapping,
                "testcases": testcase_list,
            }
            runner.run(testcase_list)
            in_out = runner.get_vars_out()
            summary = luna_summary.api_result(runner._summary, in_out)
            return summary
    except Exception as e:
        ERROR["msg"] = str(e)
        return ERROR


def add_project_mapping(testcase_list):
    """[summary]
    改变了原有的设计模式，把config的参数合并到变量中，而不是把变量合并到config中

    Args:
        testcase_list ([type]): [description]

    Returns:
        [type]: [description]
    """
    config = testcase_list[0]["config"]
    data = config.get("variables")
    for i in testcase_list[0]["teststeps"]:
        if "variables" in i and isinstance(i["variables"], list):
            keys = get_all_key_by_dict(i["variables"])
            index = update_all_key_by_dict(data, keys)
            new_config = update_list(data, index)
            i["variables"] = new_config + i["variables"]
            all_keys = get_all_key_by_dict(i["variables"])
            # print('all_keys',all_keys)
            if all_keys:
                for new_key in all_keys:
                    if new_key not in i["desc"]["variables"]:
                        i["desc"]["variables"][new_key] = ""
    project_mapping = {
        "name": config.get("name", ""),
        "env": config.get("refs").get("env", {}),
        "variables": {},
        "functions": config.get("refs").get("debugtalk").get("functions", {}),
    }
    return project_mapping


# def out_put_data(testcase_list, project_mapping, type=None):
#     """[summary]
#     把单个接口的variables和extract拼接，作为output输出
#     Arguments:
#       testcase_list {[type]} -- [description]
#       project_mapping {[type]} -- [description]
#     """
#     outPutDataList = []
#     if type == 1:
#         for i in testcase_list["testcases"][0]["teststeps"]:
#             if "extract" in i["desc"]:
#                 if isinstance(i["desc"]["extract"], dict):
#                     extractList = list(i["desc"]["extract"].keys())
#                     outPutDataList = extractList + outPutDataList
#             if "variables" in i["desc"]:
#                 if isinstance(i["desc"]["variables"], dict):
#                     variablesList = list(i["desc"]["variables"].keys())
#                     outPutDataList = variablesList + outPutDataList
#         testcase_list["testcases"][0]["config"]["output"] = outPutDataList
#     else:
#         for i in testcase_list[0]["teststeps"]:
#             if "extract" in i["desc"]:
#                 if isinstance(i["desc"]["extract"], dict):
#                     extractList = list(i["desc"]["extract"].keys())
#                     outPutDataList = extractList + outPutDataList
#             if "variables" in i["desc"]:
#                 if isinstance(i["desc"]["variables"], dict):
#                     variablesList = list(i["desc"]["variables"].keys())
#                     outPutDataList = variablesList + outPutDataList
#         testcase_list[0]["config"]["output"] = outPutDataList
#     return testcase_list


def update_teststeps_validate(testcase_list):
    """
    config 中的断言合并到api中，达到设置公共断言的效果
    :param testcase_list:
    :return:
    """
    config = testcase_list[0]["config"]
    if "validate" in config:
        if "validate" in testcase_list[0]["teststeps"][0]:
            validates = (
                testcase_list[0]["teststeps"][0]["validate"] + config["validate"]
            )
            testcase_list[0]["teststeps"][0]["validate"] = validates
        else:
            testcase_list[0]["teststeps"][0]["validate"] = config["validate"]
    return testcase_list


# def update_in_out(in_out):
#     try:
#         new_in_out = {"out": in_out["out"], "in": {}}
#         for (key, value) in in_out["in"].items():
#             if isinstance(value, LazyString):
#                 hook_data = text_type(value)
#                 hook = re.search(r"(?<=LazyString\(\$\{)(.*)(?=\})", hook_data)[0]
#                 add_hook = {key: hook}
#                 new_in_out["in"].update(add_hook)
#         return new_in_out
#     except Exception as e:
#         return in_out


# def api_result(summary, in_out):
#     """
#     单接口测试返回
#     """
#     result = {}
#     out_data = update_in_out(in_out[0])
#     result["out_data"] = out_data
#     for detail in summary["details"]:
#         for record in detail["records"]:
#             data = record["meta_datas"]["data"]
#             for meta_data in data:
#                 request = meta_data["request"]
#                 try:
#                     req_data = json.dumps(request)
#                     req_data = req_data.replace("\\n", "").replace("&#34;", "'")
#                     req_data = eval(str(json.loads(req_data)))
#                     req_data["body"] = json.loads(req_data["body"].replace("'", '"'))
#                     req_data["headers"] = json.loads(request["headers"])
#                     result["request"] = req_data
#                 except Exception as e:
#                     result["request"] = str(e)
#                 response = meta_data["response"]
#                 result["response"] = {}
#                 result["response"]["headers"] = json.loads(response["headers"])
#                 print(meta_data["response"]["status_code"])
#                 print(meta_data["response"]["reason"])
#                 try:
#                     result["response"]["body"] = (
#                         json.loads(response["body"]) if response["body"] else ""
#                     )
#                     result["response"]["status_code"] = meta_data["response"][
#                         "status_code"
#                     ]
#                 except Exception as e:
#                     result["response"]["body"] = meta_data["response"]["reason"]
#                     result["response"]["status_code"] = meta_data["response"][
#                         "status_code"
#                     ]
#         result["status"] = record["status"]
#         result["msg"] = record["attachment"]
#     return result


# def apis_result(summary, in_out):
#     """
#     测试链路返回
#     """
#     result_list = []
#     if len(in_out) > 0:
#         result_list.append(in_out[0])
#     for detail in summary["details"]:
#         for record in detail["records"]:
#             result = {}
#             result["target_url"] = record["meta_datas"]["data"][0]["request"]["url"]
#             result["name"] = record["name"]
#             result["status"] = record["status"]
#             result["msg"] = ErrorHandler(record["attachment"])
#             data = record["meta_datas"]["data"]
#             for meta_data in data:
#                 request = meta_data["request"]
#                 try:
#                     req_data = json.dumps(request)
#                     req_data = req_data.replace("\\n", "").replace("&#34;", "'")
#                     req_data = eval(str(json.loads(req_data)))
#                     req_data["body"] = json.loads(req_data["body"].replace("'", '"'))
#                     req_data["headers"] = json.loads(request["headers"])
#                     result["request"] = req_data
#                 except Exception as e:
#                     result["request"] = str(e)
#                 response = meta_data["response"]
#                 result["response"] = {}
#                 result["response"]["headers"] = json.loads(response["headers"])
#                 try:
#                     result["response"]["body"] = (
#                         json.loads(response["body"]) if response["body"] else ""
#                     )
#                 except Exception as e:
#                     result["response"]["body"] = str(e)
#             result_list.append(result)
#     return result_list


def add_sql_config(testcase_list):
    for i in testcase_list["testcases"][0]["teststeps"]:
        if i["request"]["url"] == "/api/1/sql/connect":
            sql_config_id = i["request"]["json"]["other_config_id"]
            sqlConfigDetail = Config.query.filter_by(id=sql_config_id).first_or_404(
                "sql_config_id"
            )
            i["request"]["url"] = sqlConfigDetail.base_url + "/api/1/sql/connect"
    return testcase_list


def updateValues(config_variables, case_variables):
    # TODO: 往config中添加variables,给out_put调用,暂时弃用。
    all_variables = []
    if len(config_variables) > 0 and len(case_variables) > 0:
        # 先剔去重复的数据
        case_variables = reduce(
            lambda x, y: x if y in x else x + [y],
            [
                [],
            ]
            + case_variables,
        )
        config_variables = reduce(
            lambda x, y: x if y in x else x + [y],
            [
                [],
            ]
            + config_variables,
        )
        # 先处理相同的元素,以case_variables为准。
        for i in case_variables:
            for k in config_variables:
                if i.keys() & k.keys():
                    print("i:", i)
                    print("k:", k)
                    config_variables.remove(k)
                    all_variables.append(i)
        all_variables = case_variables + config_variables
        all_variables = reduce(
            lambda x, y: x if y in x else x + [y],
            [
                [],
            ]
            + all_variables,
        )
        # 再处理相同的元素,剔除case_variables中已经添加到all_variables的数据。
        all_variables = [
            dict(t) for t in set([tuple(d.items()) for d in all_variables])
        ]
        for i in case_variables[:]:
            for k in all_variables:
                if i.keys() & k.keys():
                    index = case_variables.index(i)
                    del case_variables[index]
        all_variables.extend(case_variables)
    else:
        all_variables = config_variables + case_variables
    return all_variables


# def parse_summary(summary):
#     """序列化summary"""
#     for detail in summary["details"]:
#         for record in detail["records"]:
#             for key, value in record["meta_datas"]["data"][0]["request"].items():
#                 if isinstance(value, bytes):
#                     record["meta_datas"]["data"][0]["request"][key] = value.decode(
#                         "utf-8"
#                     )
#                 if isinstance(value, RequestsCookieJar):
#                     record["meta_datas"]["data"][0]["request"][
#                         key
#                     ] = requests.utils.dict_from_cookiejar(value)
#                 if isinstance(value, str):
#                     try:
#                         record["meta_datas"]["data"][0]["request"][key] = json.loads(
#                             value
#                         )
#                     except Exception as e:
#                         record["meta_datas"]["data"][0]["request"][key] = value

#             for key, value in record["meta_datas"]["data"][0]["response"].items():
#                 if isinstance(value, bytes):
#                     record["meta_datas"]["data"][0]["response"][key] = value.decode(
#                         "utf-8"
#                     )
#                 if isinstance(value, RequestsCookieJar):
#                     record["meta_datas"]["data"][0]["response"][
#                         key
#                     ] = requests.utils.dict_from_cookiejar(value)
#                 if isinstance(value, str):
#                     try:
#                         value = record["meta_datas"]["data"][0]["response"][
#                             key
#                         ] = json.loads(value)

#                     except Exception as e:
#                         record["meta_datas"]["data"][0]["response"][key] = value

#             if (
#                 "text/html"
#                 in record["meta_datas"]["data"][0]["response"]["content_type"]
#             ):
#                 record["meta_datas"]["data"][0]["response"]["content"] = BeautifulSoup(
#                     record["meta_datas"]["data"][0]["response"]["content"],
#                     features="html.parser",
#                 ).prettify()

#     return summary


# def save_summary(name, summary, project, executor):
#     """保存报告信息"""
#     if "status" in summary.keys():
#         return
#     if name is None:
#         name = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     for i in summary["details"]:
#         i.pop("in_out")
#     summary['details'][0]['name'] = name
#     return Report.add_summary(
#         pro_id=project,
#         summary=json.dumps(summary, cls=JSONEncoder, ensure_ascii=False),
#         report_name=name,
#         create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         update_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         executor=executor,
#     )


# def ErrorHandler(attachment):
#     if "httprunner.exceptions.ExtractFailure" in attachment:
#         result = re.findall("httprunner.exceptions.ExtractFailure:(.*)", attachment)
#         if len(result) > 0:
#             data = result[0]
#             return data
#     if "httprunner.exceptions.VariableNotFound" in attachment:
#         result = re.findall("httprunner.exceptions.VariableNotFound:(.*)", attachment)
#         if len(result) > 0:
#             data = result[0]
#             return data
#     if "httprunner.exceptions.ParamsError" in attachment:
#         result = re.findall("httprunner.exceptions.ParamsError:(.*)", attachment)
#         if len(result) > 0:
#             data = (
#                 result[0]
#                 + "   available response attributes: status_code, cookies, elapsed, headers, content, text, json, encoding, ok, reason, url."
#             )
#             return data
#     else:
#         return attachment


def parseType(types, value):
    """[summary]
    类型转换
    Args:
        type ([type]): [description]
        value ([type]): [description]
    """
    if types == 1:
        if isinstance(value, str):
            data = value
        else:
            data = str(value)
    if types == 2:
        if isinstance(value, int):
            data = value
        else:
            data = int(value)
    if types == 3:
        if isinstance(value, float):
            data = value
        else:
            data = float(value)
    if types == 4:
        if value == "True" or value == "true":
            data = True
        else:
            data = False
    if types == 5:
        if isinstance(value, list):
            data = value
        else:
            data = literal_eval(value)
    if types == 6:

        if isinstance(value, dict):
            data = value
        else:
            data = json.loads(value)
    return data
