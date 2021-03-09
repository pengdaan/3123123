#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :category.py
@说明        :
@时间        :2020/08/14 15:41:27
@作者        :Leo
@版本        :1.0
"""

from flask import jsonify
from app.libs.code import Sucess

from app.libs.auth import auth_jwt
from app.libs.redprint import Redprint
from app.models.api import Api
from app.models.category import Category
from app.validators.category_validator import (
    addCategoryForm,
    updateCategoryForm,
)

api = Redprint("category")


@api.route("/add", methods=["POST"])
@auth_jwt
def add_category():
    """
    新增分类
    :return:
    """
    categoryData = addCategoryForm().validate_for_api()
    Category.add_category(
        categoryData.category_name.data,
        categoryData.project_id.data,
        categoryData.desc.data,
    )
    return Sucess()


@api.route("/del/<int:id>", methods=["DELETE"])
@auth_jwt
def del_category(id):
    """
    删除分类：必须在该分类下没有api才可以删除
    :param id:
    :return:
    """
    CategoryInfo = Category.query.filter_by(id=id).first_or_404("CategoryId")
    res = Api.get_category_detail(CategoryInfo.id)
    if len(res) > 0:
        return jsonify({"code": -1, "data": "", "msg": "该分类下存在接口"})
    else:
        Category.del_category(CategoryInfo.id)
        return Sucess()


@api.route("/update", methods=["POST"])
@auth_jwt
def update_category():
    """
    更新分类
    :return:
    """
    categoryData = updateCategoryForm().validate_for_api()
    Category.query.filter_by(id=categoryData.id.data).first_or_404("CategoryId")
    Category.update_category(categoryData.id.data, categoryData.category_name.data)
    return Sucess()


@api.route("/list/<int:project_id>", methods=["GET"])
@auth_jwt
def category_list(project_id):
    """
    获取项目下的分类列表
    :param project_id:
    :return:
    """
    res = Category.get_category_list(project_id)
    return Sucess(data=res)
