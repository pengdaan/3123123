#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :consumer.py
@说明        :
@时间        :2020/08/19 16:41:17
@作者        :Leo
@版本        :1.0
"""
"""消费者"""


import os
import time
import pika
from flask import Flask, jsonify, render_template, request
import app
from app.libs import run
from app.models.case import Case
from app.models.case_detail import Case_Detail
from app.models.case_module import CaseModule
from app.models.config import Config
from app.models.tasks import ScheduledTasks as Task
from app.register.wsIO import socketio


def consumer(queue):
    # 证书创建
    config_name = os.getenv("FLASK_ENV", "development")
    Luna_config = app.config[config_name]
    mq_config = getattr(Luna_config, "FLASK_PIKA_PARAMS")
    # 获取配置类的属性
    credentials = pika.PlainCredentials("guest", "guest")
    # # 本地连接
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=mq_config["host"], port=mq_config["port"], credentials=credentials
        )
    )
    channel = conn.channel()
    # 再次创建队列，防止队列不存在的情况出现，和生产者队列同名
    channel.queue_declare(queue=queue)
    # no_ack 表名是否告知发送端是否接受消息，True - 接收
    channel.basic_consume(queue, callback, auto_ack=True)
    # 开启监听，进程夯住，等待消息
    print("waiting for message To exit   press CTRL+C")
    channel.start_consuming()
    conn.close()


# 回调函数，用于队列任务结束后的回调，用于将数据返回发送端，表明是否执行完毕
def callback(ch, method, properties, body):
    data = eval(body)
    tasks_list = []
    if len(data["data"]) > 0:
        for req in data["data"]:
            executor = req["user_id"] if req["user_id"] != "" else None
            caseDetail = Case_Detail.get_case_detail(req["case_id"])
            case = Case.query.filter_by(id=req["case_id"]).first()
            case_list = []
            if len(caseDetail) > 0:
                for i in caseDetail:
                    baseData = CaseModule.query.filter_by(id=i.module_id).first()
                    if baseData.sql_config_id:
                        body_detail = eval(baseData.body)
                        body_detail["request"]["json"]["id"] = int(
                            baseData.sql_config_id
                        )
                        body_detail["request"]["json"]["other_config_id"] = int(
                            baseData.other_config_id
                        )
                    else:
                        body_detail = eval(baseData.body)
                    case_list.append(body_detail)
                config = Config.query.filter_by(id=req["config_id"]).first()
                if config:
                    host = None
                    config = eval(config.body)
                    summary = run.debug_api(
                        case_list,
                        req["pro_id"],
                        case_id=req["case_id"],
                        config=run.parse_host(host, config),
                        status=1,
                        run_type=None,
                        name=case.case_name,
                        executor=executor,
                    )
                    if isinstance(summary, int):
                        case_tasks_id = Task.add_case_tasks(
                            case_id=req["case_id"], case_status=1, summary=summary
                        )
                        tasks_list.append(str(case_tasks_id))
                    else:
                        case_tasks_id = Task.add_case_tasks(
                            case_id=req["case_id"],
                            case_status=0,
                            summary=summary["msg"],
                        )
                        tasks_list.append(str(case_tasks_id))
                else:
                    case_tasks_id = Task.add_case_tasks(
                        case_id=req["case_id"], case_status=0, summary="项目配置不存在，请检查"
                    )
                    tasks_list.append(str(case_tasks_id))
            else:
                case_tasks_id = Task.add_case_tasks(
                    case_id=req["case_id"], case_status=0, summary="用例数量为空，请检查"
                )
                tasks_list.append(str(case_tasks_id))
        tasks_detail = ",".join(tasks_list)
        projet_taskId = Task.add_project_tasks(
            pro_id=req["pro_id"],
            executor=data["executor"],
            count=len(data["data"]),
            tasks_detail=tasks_detail,
        )
        result = Task.get_project_tasks_detail(projet_taskId.id)
        socketio.sleep(3)
        socketio.emit(
            "server_response",
            {"code": 4004, "data": result, "msg": "项目用例集执行完毕"},
            namespace="/test",
        )
    else:
        socketio.emit(
            "server_response",
            {"code": 4005, "data": "", "msg": "Case不存在用例"},
            namespace="/test",
        )
