#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :category.py
@说明        :
@时间        :2020/08/14 15:41:27
@作者        :Leo
@版本        :1.0
"""

from app.libs.code import Sucess
from app.libs.auth import auth_jwt
from app.libs.redprint import Redprint
from app.models.case import Case
from app.models.tag import Case_Tag
from app.validators.tag_validator import addTagForm, updateTagForm

api = Redprint("tag")


@api.route("/add", methods=["POST"])
@auth_jwt
def add_tag():
    """
    新增标签
    :return:
    """
    tagData = addTagForm().validate_for_api()
    Case_Tag.add_ca_tag(tagData.tag_name.data, tagData.pro_id.data, tagData.desc.data)
    return Sucess()


@api.route("/del/<int:id>", methods=["DELETE"])
@auth_jwt
def del_tag(id):
    """
    删除标签：必须在该分类下没有case才可以删除
    :param id:
    :return:
    """
    TagInfo = Case_Tag.query.filter_by(id=id).first_or_404("TagId")
    res = Case.get_all_case_by_tag(TagInfo.id)
    if res:
        return Sucess(code=-1, data="该标签下存在接口")
    else:
        Case_Tag.del_ca_tag(TagInfo.id)
        return Sucess()


@api.route("/update", methods=["POST"])
@auth_jwt
def update_category():
    """
    更新标签
    :return:
    """
    TagData = updateTagForm().validate_for_api()
    Case_Tag.query.filter_by(id=TagData.id.data).first_or_404("TagId")
    Case_Tag.update_ca_tag(TagData.id.data, TagData.tag_name.data)
    return Sucess()


@api.route("/list/<int:project_id>", methods=["GET"])
@auth_jwt
def tag_list(project_id):
    """
    获取项目下的分类列表
    :param project_id:
    :return:
    """
    res = Case_Tag.get_category_list(project_id)
    return Sucess(data=res)
