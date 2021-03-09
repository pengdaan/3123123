#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :project.py
@说明        :project校验
@时间        :2020/08/11 09:17:36
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Length

from app.models.project import Project
from app.validators.base_validator import BaseForm as Form


class ProjectBaseForm(Form):
    project_name = StringField(
        validators=[Length(min=1, max=50), DataRequired(message="项目名不允许为空")]
    )
    desc = StringField()
    user_id = IntegerField()


class addProjectForm(ProjectBaseForm):
    def validate_project_name(self, value):
        if Project.query.filter_by(project_name=value.data, status=1).first():
            raise ValidationError(message="项目已存在")


class updateProjectForm(ProjectBaseForm):
    project_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])

    def validate_project_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="项目不存在")


class searchProjectForm(Form):
    kw = StringField()
