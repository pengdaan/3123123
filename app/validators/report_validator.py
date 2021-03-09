#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :report.py
@说明        :
@时间        :2020/08/18 20:22:56
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Length, Optional
from app.validators.base_validator import BaseForm as Form


class ReportForm(Form):
    report_name = StringField(
        validators=[Length(min=1, max=255), DataRequired(message="name不允许为空")]
    )
    pro_id = IntegerField(validators=[DataRequired(message="projectId不允许为空")])


class searchReportForm(Form):
    kw = StringField(validators=[Optional()])
    pro_id = IntegerField(validators=[DataRequired(message="projectId不允许为空")])
    page = IntegerField(validators=[Optional()])
