#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :processCategory.py
@说明        :swagger转httprunner 分类录入
@时间        :2020/11/13 10:19:15
@作者        :Leo
@版本        :1.0
"""
from app.models.category import Category


def get_swagger_tag(pro_id, tag):
    """[summary]
    获取项目分类id

    Args:
        pro_id ([type]): [description]
        tag ([type]): [description]
    """
    CategoryInfo = Category.query.filter_by(
        pro_id=pro_id, category_name=tag, status=1
    ).first()
    if not CategoryInfo:
        CategoryInfo = Category.add_category(tag, pro_id, "")
    return CategoryInfo.id
