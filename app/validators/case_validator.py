#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :case.py
@说明        :
@时间        :2020/08/13 14:39:42
@作者        :Leo
@版本        :1.0
"""

from wtforms import FieldList, IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Length

from app.models.case import Case
from app.models.config import Config
from app.models.project import Project
from app.validators.base_validator import BaseForm as Form


class CaseBaseForm(Form):
    config_id = IntegerField(validators=[DataRequired(message="configId不允许为空")])
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])
    desc = StringField()
    tag_id = IntegerField()

    def validate_config_id(self, value):
        if not Config.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="配置不存在")

    def validate_pro_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="项目不存在")


class CaseForm(CaseBaseForm):
    id = IntegerField()
    user_id = IntegerField()
    case_name = StringField(
        validators=[Length(min=1, max=255), DataRequired(message="name不允许为空")]
    )

    def validate_id(self, value):
        if Case.query.filter_by(id=value.data, status=1).first():
            return self

    def validate_case_name(self, value):
        if Case.query.filter_by(
            pro_id=self.pro_id.data, status=1, case_name=value.data
        ).first():
            raise ValidationError(message="case已存在")


class UpdateCaseForm(CaseBaseForm):
    id = IntegerField(validators=[DataRequired(message="Id不允许为空")])
    case_name = StringField(
        validators=[Length(min=1, max=255), DataRequired(message="name不允许为空")]
    )
    config_id = IntegerField(validators=[DataRequired(message="configId不允许为空")])

    def validate_id(self, value):
        if Case.query.filter_by(id=value.data, status=1).first():
            return self


class CaseRunForm(CaseBaseForm):
    case_id = IntegerField(validators=[DataRequired(message="caseId不允许为空")])

    def validate_case_id(self, value):
        if not Case.query.filter_by(
            id=value.data,
            status=1,
        ).first():
            raise ValidationError(message="case不存在")


class DebugCaseForm(CaseRunForm):
    module_list = FieldList(
        StringField(), validators=[Length(min=1), DataRequired(message="list不允许为空")]
    )


class SetupForm(Form):
    setups = FieldList(
        StringField(), validators=[Length(min=1), DataRequired(message="list不允许为空")]
    )


class CopyCaseForm(Form):
    id = IntegerField()
    user_id = IntegerField()
    pro_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])
    case_name = StringField(
        validators=[Length(min=1, max=255), DataRequired(message="name不允许为空")]
    )

    def validate_case_name(self, value):
        if Case.query.filter_by(
            pro_id=self.pro_id.data, status=1, case_name=value.data
        ).first():
            raise ValidationError(message="case已存在")