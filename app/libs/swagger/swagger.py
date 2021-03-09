#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :swagger.py
@说明        :swagger 转httprunner
@时间        :2020/11/13 10:20:10
@作者        :Leo
@版本        :1.0
"""

import requests

from app.libs.httprunner import logger
from app.libs.swagger.process_api import (
    add_swagger_Api_by_module,
    get_swagger_Api,
    get_swagger_api_body,
)
from app.libs.swagger.process_category import get_swagger_tag
from app.models.hook import Hook


class AnalysisJson:
    """swagger自动生成测试用例"""

    def __init__(self, url, pro_id, add_type, uId):
        self.url = url
        self.pro_id = pro_id
        self.add_type = add_type
        self.uId = uId
        self.interface = {}
        self.case_list = []
        self.tags_list = []
        self.http_suite = {
            "config": {"name": "", "base_url": "", "variables": {}},
            "testcases": [],
        }
        self.http_testcase = {"name": "", "testcase": "", "variables": {}}

    def retrieve_data(self):
        """
        主函数
        :return:
        """

        try:
            # r = requests.get('http://192.168.242.63:30168/v2/api-docs').json()
            r = requests.get(self.url).json()
            # write_data(r, 'data.json')
        except Exception as e:
            logger.log_error("请求swagger url 发生错误. 详情原因: {}".format(e))
            return "请求swagger url 发生错误. 详情原因: {}".format(e)
        self.data = r["paths"]  # 接口数据
        self.url = "https://" + r["host"]
        self.title = r["info"]["title"] if "title " in r["info"] else "swagger缺乏该字段"
        self.http_suite["config"]["name"] = self.title
        self.http_suite["config"]["base_url"] = self.url

        self.definitions = r["definitions"]  # body参数
        for tag_dict in r["tags"]:
            self.tags_list.append(tag_dict["name"])
        i = 0
        for tag in self.tags_list:
            self.http_suite["testcases"].append(
                {"name": "", "testcase": "", "variables": {}}
            )
            self.http_suite["testcases"][i]["name"] = tag
            self.http_suite["testcases"][i]["testcase"] = "testcases/" + tag + ".json"
            i += 1
            # 屏蔽本地文件方式写入
            # suite_path = os.path.join(
            #     os.path.abspath(os.path.join(os.getcwd(), ".")), 'testsuites')
        # testcase_path = os.path.join(suite_path, 'demo_testsuite.json')
        # write_data(self.http_suite, testcase_path)
        if isinstance(self.data, dict):
            for tag in self.tags_list:
                self.http_case = {
                    "config": {"name": "", "base_url": "", "variables": {}},
                    "teststeps": [],
                }

                for key, value in self.data.items():
                    for method in list(value.keys()):
                        params = value[method]
                        if not params["deprecated"]:  # 接口是否被弃用
                            if params["tags"][0] == tag:
                                self.http_case["config"]["name"] = params["tags"][0]
                                self.http_case["config"]["base_url"] = self.url
                                case = self.retrieve_params(params, key, method, tag)
                                self.http_case["teststeps"].append(case)
                        else:
                            logger.log_info(
                                "interface path: {}, if name: {}, is deprecated.".format(
                                    key, params["description"]
                                )
                            )
                            break
                # api_path = os.path.join(
                #     os.path.abspath(
                #         os.path.join(os.path.dirname("__file__"),
                #                      os.path.pardir)), 'testcases')
                # api_path = os.path.join(
                #     os.path.abspath(os.path.join(os.getcwd(), ".")),
                #     'testcases')
                # print('api_path:', api_path)
                # testcase_path = os.path.join(api_path, tag + '.json')
                # write_data(self.http_case, testcase_path)

        else:
            logger.log_error("解析接口数据异常！url 返回值 paths 中不是字典.")
            return "error"

    def retrieve_params(self, params, api, method, tag):
        """
        解析json，把每个接口数据都加入到一个字典中
        :param params:
        :param params_key:
        :param method:
        :param key:
        :return:
        replace('false', 'False').replace('true', 'True').replace('null','None')
        """
        http_interface = {
            "name": "",
            "variables": {},
            "request": {
                "url": "",
                "method": "",
                "headers": {},
                "json": {},
                "params": {},
                "data": {},
            },
            "validate": [],
            "output": [],
        }
        http_testcase = {
            "name": "",
            "api": "",
            "variables": {},
            "validate": [],
            "extract": [],
            "output": [],
        }

        name = params["summary"].replace("/", "_")
        http_interface["name"] = name
        http_testcase["name"] = name
        http_testcase["api"] = "api/{}/{}.json".format(tag, name)
        http_interface["request"]["method"] = method.upper()
        http_interface["request"]["url"] = api.replace("{", "$").replace("}", "")
        parameters = params.get("parameters")  # 未解析的参数字典
        responses = params.get("responses")
        if not parameters:  # 确保参数字典存在
            parameters = {}
        for each in parameters:
            if each.get("in") == "body":  # body 和 query 不会同时出现
                schema = each.get("schema")
                if schema:
                    ref = schema.get("$ref")
                    if ref:
                        param_key = ref.split("/")[-1]
                        param = self.definitions[param_key]["properties"]
                        for key, value in param.items():
                            if "example" in value.keys():
                                http_interface["request"]["json"].update(
                                    {key: value["example"]}
                                )
                            else:
                                http_interface["request"]["json"].update({key: ""})
            elif each.get("x-examples"):
                schema = each.get("schema")
                if schema:
                    if schema.get("type") == "array":
                        for value in each.get("x-examples").values():
                            http_interface["request"]["json"] = eval(value)
            elif each.get("in") == "formData":
                name = each.get("name")
                for key in each.keys():
                    if "x-example" in key:
                        http_interface["request"]["data"].update({name: each[key]})
            elif each.get("in") == "query":
                name = each.get("name")
                for key in each.keys():
                    if "example" in key:
                        http_interface["request"]["params"].update({name: each[key]})
        for each in parameters:
            # if each.get('in') == 'path':
            #     name = each.get('name')
            #     for key in each.keys():
            #         if 'example' in key:
            #             http_interface['request']['json'].update({name: each[key]})
            #     else:
            #
            #         http_interface['request']['json'].update({name: ''})
            if each.get("in") == "header":
                name = each.get("name")
                for key in each.keys():
                    if "example" in key:
                        http_interface["request"]["headers"].update({name: each[key]})
                    else:
                        if name == "token":
                            http_interface["request"]["headers"].update(
                                {name: "$token"}
                            )
                        else:
                            http_interface["request"]["headers"].update({name: ""})
        for key, value in responses.items():
            schema = value.get("schema")
            if schema:
                ref = schema.get("$ref")
                if ref:
                    param_key = ref.split("/")[-1]
                    res = self.definitions[param_key]["properties"]
                    i = 0
                    for k, v in res.items():
                        if "example" in v.keys():
                            http_interface["validate"].append({"eq": []})
                            http_interface["validate"][i]["eq"].append("content." + k)
                            http_interface["validate"][i]["eq"].append(v["example"])

                            http_testcase["validate"].append({"eq": []})
                            http_testcase["validate"][i]["eq"].append("content." + k)
                            http_testcase["validate"][i]["eq"].append(v["example"])
                            i += 1
                else:
                    http_interface["validate"].append({"eq": []})
            else:
                http_interface["validate"].append({"eq": []})
        if http_interface["request"]["json"] == {}:
            del http_interface["request"]["json"]
        if http_interface["request"]["params"] == {}:
            del http_interface["request"]["params"]

        # api_path = os.path.join(
        #     os.path.abspath(os.path.join(os.getcwd(), ".")), 'api')
        # print(' api_path:', api_path)
        # tags_path = os.path.join(api_path, tag)
        # print('tag:', tag)
        cateId = get_swagger_tag(self.pro_id, tag)
        api_body = get_swagger_api_body(http_interface)

        apiId = get_swagger_Api(
            http_interface["request"]["url"],
            http_interface["name"],
            self.pro_id,
            http_interface["request"]["method"],
            cateId,
        )
        # print('apiId ----------->', apiId)
        # if not os.path.exists(tags_path):
        #     os.mkdir(tags_path)
        # json_path = os.path.join(tags_path, http_interface['name'] + '.json')
        # print('http_interface：', http_interface)
        add_swagger_Api_by_module(
            apiId, str(api_body), self.uId, api_type=self.add_type
        )
        # 屏蔽本地写入文件
        # write_data(http_interface, json_path)

        return http_testcase
