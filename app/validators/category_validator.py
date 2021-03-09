#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :catego.py
@说明        :
@时间        :2020/08/14 16:24:42
@作者        :Leo
@版本        :1.0
"""

from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired

from app.models.category import Category
from app.models.project import Project
from app.validators.base_validator import BaseForm as Form


class CategoryBaseForm(Form):
    category_name = StringField(validators=[DataRequired(message="分类名不允许为空")])
    desc = StringField()
    project_id = IntegerField(validators=[DataRequired(message="proId不允许为空")])

    def validate_project_id(self, value):
        if not Project.query.filter_by(id=value.data, status=1).first():
            raise ValidationError(message="proId不存在")


class addCategoryForm(CategoryBaseForm):
    def validate_category_name(self, value):
        if Category.query.filter_by(
            pro_id=self.project_id.data, category_name=value.data, status=1
        ).first():
            raise ValidationError(message="该分类已存在")


class updateCategoryForm(CategoryBaseForm):
    id = IntegerField()

    def validate_id(self, value):
        if not Category.query.filter_by(id=value.data).first():
            raise ValidationError(message="该分类不存在")
