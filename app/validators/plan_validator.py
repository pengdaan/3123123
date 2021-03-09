#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :plan.py
@说明        :
@时间        :2020/12/03 14:59:47
@作者        :Leo
@版本        :1.0
"""

from wtforms import FieldList, IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Length

from app.models.plan import Plan
from app.models.project import Project
from app.validators.base_validator import BaseForm as Form


class PlanBaseForm(Form):
    id = IntegerField()
    name = StringField(validators=[DataRequired(message="项目名不允许为空")])
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])
    desc = StringField()
    isTasks = IntegerField()
    case_list = StringField()
    executor = IntegerField()

    def validate_pro_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="项目不存在")


class UpdatePlanCaseForm(Form):
    id = IntegerField(validators=[DataRequired(message="计划Id不允许为空")])
    case_list = FieldList(
        StringField(), validators=[Length(min=1), DataRequired(message="list不允许为空")]
    )

    def validate_id(self, value):
        if not Plan.query.filter_by(id=value.data).first():
            raise ValidationError(message="计划不存在")


class UpdatePlanisTasksForm(Form):
    id = IntegerField(validators=[DataRequired(message="计划Id不允许为空")])
    isTasks = IntegerField()

    def validate_id(self, value):
        if not Plan.query.filter_by(id=value.data).first():
            raise ValidationError(message="计划不存在")
