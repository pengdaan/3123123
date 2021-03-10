#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :summary.py
@说明        :
@时间        :2021/03/09 14:25:26
@作者        :Leo
@版本        :1.0
'''
from app.libs.httprunner.parser import LazyString
from flask._compat import text_type
import re
import json
# from app.libs.run import ErrorHandler
from requests.cookies import RequestsCookieJar
import requests
from datetime import datetime
from app.libs.decimal_encoder import JSONEncoder
from app.models.report import Report
from bs4 import BeautifulSoup


def out_put_data(testcase_list, project_mapping, type=None):
    """[summary]
    把单个接口的variables和extract拼接，作为output输出
    Arguments:
      testcase_list {[type]} -- [description]
      project_mapping {[type]} -- [description]
    """
    outPutDataList = []
    if type == 1:
        for i in testcase_list["testcases"][0]["teststeps"]:
            if "extract" in i["desc"]:
                if isinstance(i["desc"]["extract"], dict):
                    extractList = list(i["desc"]["extract"].keys())
                    outPutDataList = extractList + outPutDataList
            if "variables" in i["desc"]:
                if isinstance(i["desc"]["variables"], dict):
                    variablesList = list(i["desc"]["variables"].keys())
                    outPutDataList = variablesList + outPutDataList
        testcase_list["testcases"][0]["config"]["output"] = outPutDataList
    else:
        for i in testcase_list[0]["teststeps"]:
            if "extract" in i["desc"]:
                if isinstance(i["desc"]["extract"], dict):
                    extractList = list(i["desc"]["extract"].keys())
                    outPutDataList = extractList + outPutDataList
            if "variables" in i["desc"]:
                if isinstance(i["desc"]["variables"], dict):
                    variablesList = list(i["desc"]["variables"].keys())
                    outPutDataList = variablesList + outPutDataList
        testcase_list[0]["config"]["output"] = outPutDataList
    return testcase_list


def update_in_out(in_out):
    # 清洗返回的数据,去掉LazyString
    try:
        new_in_out = {"out": in_out["out"], "in": {}}
        for (key, value) in in_out["in"].items():
            if isinstance(value, LazyString):
                hook_data = text_type(value)
                hook = re.search(r"(?<=LazyString\(\$\{)(.*)(?=\})", hook_data)[0]
                add_hook = {key: hook}
                new_in_out["in"].update(add_hook)
        return new_in_out
    except Exception as e:
        return in_out


def api_result(summary, in_out):
    """
    单接口测试返回
    """
    print('312312312',summary)
    result = {}
    out_data = update_in_out(in_out[0])
    result["out_data"] = out_data
    for detail in summary["details"]:
        for record in detail["records"]:
            data = record["meta_datas"]["data"]
            for meta_data in data:
                request = meta_data["request"]
                try:
                    req_data = json.dumps(request)
                    req_data = req_data.replace("\\n", "").replace("&#34;", "'")
                    req_data = eval(str(json.loads(req_data)))
                    req_data["body"] = json.loads(req_data["body"].replace("'", '"'))
                    req_data["headers"] = json.loads(request["headers"])
                    result["request"] = req_data
                except Exception as e:
                    result["request"] = str(e)
                response = meta_data["response"]
                result["response"] = {}
                result["response"]["headers"] = json.loads(response["headers"])
                print(meta_data["response"]["status_code"])
                print(meta_data["response"]["reason"])
                try:
                    result["response"]["body"] = (
                        json.loads(response["body"]) if response["body"] else ""
                    )
                    result["response"]["status_code"] = meta_data["response"][
                        "status_code"
                    ]
                except Exception as e:
                    result["response"]["body"] = meta_data["response"]["reason"]
                    result["response"]["status_code"] = meta_data["response"][
                        "status_code"
                    ]
        result["status"] = record["status"]
        result["msg"] = record["attachment"]
    return result


def apis_result(summary, in_out):
    """
    测试链路返回
    """
    result_list = []
    if len(in_out) > 0:
        result_list.append(in_out[0])
    for detail in summary["details"]:
        for record in detail["records"]:
            result = {}
            result["target_url"] = record["meta_datas"]["data"][0]["request"]["url"]
            result["name"] = record["name"]
            result["status"] = record["status"]
            result["msg"] = ErrorHandler(record["attachment"])
            data = record["meta_datas"]["data"]
            for meta_data in data:
                request = meta_data["request"]
                try:
                    req_data = json.dumps(request)
                    req_data = req_data.replace("\\n", "").replace("&#34;", "'")
                    req_data = eval(str(json.loads(req_data)))
                    req_data["body"] = json.loads(req_data["body"].replace("'", '"'))
                    req_data["headers"] = json.loads(request["headers"])
                    result["request"] = req_data
                except Exception as e:
                    result["request"] = str(e)
                response = meta_data["response"]
                result["response"] = {}
                result["response"]["headers"] = json.loads(response["headers"])
                try:
                    result["response"]["body"] = (
                        json.loads(response["body"]) if response["body"] else ""
                    )
                except Exception as e:
                    result["response"]["body"] = str(e)
            result_list.append(result)
    return result_list


def parse_summary(summary):
    """序列化summary"""
    for detail in summary["details"]:
        for record in detail["records"]:
            for key, value in record["meta_datas"]["data"][0]["request"].items():
                if isinstance(value, bytes):
                    record["meta_datas"]["data"][0]["request"][key] = value.decode(
                        "utf-8"
                    )
                if isinstance(value, RequestsCookieJar):
                    record["meta_datas"]["data"][0]["request"][
                        key
                    ] = requests.utils.dict_from_cookiejar(value)
                if isinstance(value, str):
                    try:
                        record["meta_datas"]["data"][0]["request"][key] = json.loads(
                            value
                        )
                    except Exception as e:
                        record["meta_datas"]["data"][0]["request"][key] = value

            for key, value in record["meta_datas"]["data"][0]["response"].items():
                if isinstance(value, bytes):
                    record["meta_datas"]["data"][0]["response"][key] = value.decode(
                        "utf-8"
                    )
                if isinstance(value, RequestsCookieJar):
                    record["meta_datas"]["data"][0]["response"][
                        key
                    ] = requests.utils.dict_from_cookiejar(value)
                if isinstance(value, str):
                    try:
                        value = record["meta_datas"]["data"][0]["response"][
                            key
                        ] = json.loads(value)

                    except Exception as e:
                        record["meta_datas"]["data"][0]["response"][key] = value

            if (
                "text/html"
                in record["meta_datas"]["data"][0]["response"]["content_type"]
            ):
                record["meta_datas"]["data"][0]["response"]["content"] = BeautifulSoup(
                    record["meta_datas"]["data"][0]["response"]["content"],
                    features="html.parser",
                ).prettify()

    return summary


def get_time_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_summary(name, summary, project, executor):
    """保存报告信息"""
    if "status" in summary.keys():
        return
    if name is None:
        name = get_time_now()
    for i in summary["details"]:
        i.pop("in_out")
    summary['details'][0]['name'] = name
    return Report.add_summary(
        pro_id=project,
        summary=json.dumps(summary, cls=JSONEncoder, ensure_ascii=False),
        report_name=name,
        create_time=get_time_now(),
        update_time=get_time_now(),
        executor=executor,
    )


def ErrorHandler(attachment):
    if "httprunner.exceptions.ExtractFailure" in attachment:
        result = re.findall("httprunner.exceptions.ExtractFailure:(.*)", attachment)
        if len(result) > 0:
            data = result[0]
            return data
    if "httprunner.exceptions.VariableNotFound" in attachment:
        result = re.findall("httprunner.exceptions.VariableNotFound:(.*)", attachment)
        if len(result) > 0:
            data = result[0]
            return data
    if "httprunner.exceptions.ParamsError" in attachment:
        result = re.findall("httprunner.exceptions.ParamsError:(.*)", attachment)
        if len(result) > 0:
            data = (
                result[0]
                + "   available response attributes: status_code, cookies, elapsed, headers, content, text, json, encoding, ok, reason, url."
            )
            return data
    else:
        return attachment
