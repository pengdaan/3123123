#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :caseDetail.py
@说明        :
@时间        :2020/08/13 17:07:58
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, Optional

from app.models.case_detail import Case_Detail
from app.models.case_module import CaseModule
from app.validators.base_validator import BaseForm as Form


class delCaseDetail(Form):
    id = IntegerField([DataRequired(message="caseDetail不允许为空")])
    case_id = IntegerField([DataRequired(message="caseId不允许为空")])
    module_id = IntegerField([DataRequired(message="moduleId不允许为空")])

    def validate_id(self, value):
        if not Case_Detail.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="CasedetailId不存在")

    def validate_module_id(self, value):
        if not CaseModule.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="CaseModuleId不存在")


class addCaseDetail(Form):
    # id 允许为空
    id = IntegerField(validators=[Optional()])
    api_id = IntegerField()
    case_api = StringField()
    user_id = IntegerField()
    case_id = IntegerField([DataRequired(message="caseId不允许为空")])
    name = StringField([Length(min=1, max=255), DataRequired(message="caseName不允许为空")])
    path = StringField([Length(min=1, max=255), DataRequired(message="path不允许为空")])
    setup = IntegerField()
    other_config_id = IntegerField(validators=[Optional()])
    sql_config_id = IntegerField(validators=[Optional()])


class UpdateCaseSetup(Form):
    id = IntegerField([DataRequired(message="CaseDetailId不允许为空")])
    name = StringField(DataRequired(message="name不允许为空"))
    setup = IntegerField([DataRequired(message="setup不允许为空")])
