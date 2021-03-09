#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :report.py
@说明        :
@时间        :2020/08/14 15:43:50
@作者        :Leo
@版本        :1.0
"""

import json
import time
from datetime import datetime
from app.libs.code import Sucess
from flask import render_template, request
from app.libs.hook_code import BASE_SUMMARYS
from app.libs.redprint import Redprint
from app.models.project import Project
from app.models.report import Report
from app.models.user import User
from app.validators.report_validator import searchReportForm

api = Redprint("report")


@api.route("/list/<int:pro_id>/<int:page_id>", methods=["GET"])
def report_list(pro_id, page_id):
    Project.query.filter_by(id=pro_id, status=1).first_or_404("ProjectId")
    reportsList = []
    if page_id == 1:
        res = (
            Report.query.filter_by(pro_id=pro_id)
            .order_by(Report.id.desc())
            .limit(10)
            .offset(0)
            .all()
        )
    else:
        page = int(page_id - 1) * 10
        res = (
            Report.query.filter_by(pro_id=pro_id)
            .order_by(Report.id.desc())
            .limit(10)
            .offset(page)
            .all()
        )
    count = Report.query.filter_by(pro_id=pro_id).count()
    if res:
        for i in res:
            if i.executor:
                user = User.query.filter_by(id=i.executor).first_or_404("UserId")
                userName = user.username
            else:
                userName = "系统"
            listdetail = {
                "id": i.id,
                "report_name": i.report_name,
                "pro_id": i.pro_id,
                "executor": userName,
                "create_time": i.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            reportsList.append(listdetail)

    reportsLists = {}
    reportsLists["result_list"] = reportsList
    reportsLists["total"] = count
    return Sucess(data=reportsLists)


@api.route("/detail/<int:id>")
def report_detail(id):
    report = Report.query.filter_by(id=id).first_or_404("reportId")
    summary = json.loads(report.summary, encoding="utf-8")
    summary["html_report_name"] = report.report_name
    start_at_timestamp = summary["time"]["start_at"]
    utc_time_iso_8601_str = datetime.utcfromtimestamp(start_at_timestamp).isoformat()
    summary["time"]["start_datetime"] = utc_time_iso_8601_str
    summary['details'][0]['name'] = report.report_name
    return render_template("template.html", summary=summary)


@api.route("/search", methods=["POST"])
def search_report():
    reportData = searchReportForm().validate_for_api()
    kw = reportData.kw.data
    pro_id = reportData.pro_id.data
    page = reportData.page.data if reportData.page.data else 1
    reportsLists = {}
    reportsList = []
    if not kw:
        if page == 1:
            res = (
                Report.query.filter_by(pro_id=pro_id)
                .order_by(Report.id.desc())
                .limit(10)
                .offset(0)
                .all()
            )
        else:
            page = int(page - 1) * 10
            res = (
                Report.query.filter_by(pro_id=pro_id)
                .order_by(Report.id.desc())
                .limit(10)
                .offset(page)
                .all()
            )
    else:
        if page == 1:
            res = (
                Report.query.filter_by(pro_id=pro_id)
                .filter(Report.report_name.like("%{0}%".format(kw)))
                .order_by(Report.id.desc())
                .limit(10)
                .offset(0)
                .all()
            )
        else:
            page = int(page - 1) * 10
            res = (
                Report.query.filter_by(pro_id=pro_id)
                .filter(Report.report_name.like("%{0}%".format(kw)))
                .order_by(Report.id.desc())
                .limit(10)
                .offset(page)
                .all()
            )
    count = (
        Report.query.filter_by(pro_id=pro_id)
        .filter(Report.report_name.like("%{0}%".format(kw)))
        .count()
    )
    if res:
        for i in res:
            if i.executor:
                user = User.query.filter_by(id=i.executor).first_or_404("UserId")
                userName = user.username
            else:
                userName = "系统"
            listdetail = {
                "id": i.id,
                "report_name": i.report_name,
                "pro_id": i.pro_id,
                "executor": userName,
                "create_time": i.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            reportsList.append(listdetail)
    reportsLists["result_list"] = reportsList
    reportsLists["total"] = count
    return Sucess(data=reportsLists)


@api.route("/del/<int:id>", methods=["GET"])
def del_report(id):
    Report.query.filter_by(id=id).first_or_404("reportId")
    Report.del_report(id)
    return Sucess()


@api.route("/suite", methods=["GET"])
def report_suite_detail():
    report_list = request.args.get("report_ids").split(",")
    print("this.report_list:", report_list)
    for i in report_list:
        report = Report.query.filter_by(id=int(i)).first_or_404("reportId")
        summary = json.loads(report.summary, encoding="utf-8")
        start_at_timestamp = summary["time"]["start_at"]
        utc_time_iso_8601_str = datetime.utcfromtimestamp(
            start_at_timestamp
        ).isoformat()
        summary["time"]["start_datetime"] = utc_time_iso_8601_str
        SUMMARYS = BASE_SUMMARYS
        SUMMARYS["stat"]["testcases"]["total"] = (
            SUMMARYS["stat"]["testcases"]["total"]
            + summary["stat"]["testcases"]["total"]
        )
        SUMMARYS["stat"]["testcases"]["success"] = (
            SUMMARYS["stat"]["testcases"]["success"]
            + summary["stat"]["testcases"]["success"]
        )
        SUMMARYS["stat"]["testcases"]["fail"] = (
            SUMMARYS["stat"]["testcases"]["fail"] + summary["stat"]["testcases"]["fail"]
        )
        SUMMARYS["stat"]["teststeps"]["total"] = (
            SUMMARYS["stat"]["teststeps"]["total"]
            + summary["stat"]["teststeps"]["total"]
        )
        SUMMARYS["stat"]["teststeps"]["failures"] = (
            SUMMARYS["stat"]["teststeps"]["failures"]
            + summary["stat"]["teststeps"]["failures"]
        )
        SUMMARYS["stat"]["teststeps"]["errors"] = (
            SUMMARYS["stat"]["teststeps"]["errors"]
            + summary["stat"]["teststeps"]["errors"]
        )
        SUMMARYS["stat"]["teststeps"]["skipped"] = (
            SUMMARYS["stat"]["teststeps"]["skipped"]
            + summary["stat"]["teststeps"]["skipped"]
        )
        SUMMARYS["stat"]["teststeps"]["expectedFailures"] = (
            SUMMARYS["stat"]["teststeps"]["expectedFailures"]
            + summary["stat"]["teststeps"]["expectedFailures"]
        )
        SUMMARYS["stat"]["teststeps"]["unexpectedSuccesses"] = (
            SUMMARYS["stat"]["teststeps"]["unexpectedSuccesses"]
            + summary["stat"]["teststeps"]["unexpectedSuccesses"]
        )
        SUMMARYS["stat"]["teststeps"]["successes"] = (
            SUMMARYS["stat"]["teststeps"]["successes"]
            + summary["stat"]["teststeps"]["successes"]
        )
        SUMMARYS["time"]["start_at"] = (
            SUMMARYS["time"]["start_at"] + summary["time"]["start_at"]
        )
        SUMMARYS["time"]["duration"] = (
            SUMMARYS["time"]["duration"] + summary["time"]["duration"]
        )
        SUMMARYS["details"].append(summary["details"][0])
    start_at_timestamp = SUMMARYS["time"]["start_at"]
    utc_time_iso_8601_str = datetime.utcfromtimestamp(start_at_timestamp).isoformat()
    SUMMARYS["time"]["start_datetime"] = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()
    )
    return render_template("template.html", summary=SUMMARYS)
