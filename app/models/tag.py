#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :category.py
@说明        :
@时间        :2020/08/11 13:39:19
@作者        :Leo
@版本        :1.0
"""

from sqlalchemy import text

from flask_sqlalchemy import orm
from app.models.base import Base, db


class Case_Tag(Base):
    __tablename__ = "ca_tag"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    tag_name = db.Column(db.String(255), nullable=False, comment="标签名称")
    desc = db.Column(db.String(255), nullable=True, comment="标签描述")
    pro_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))

    @orm.reconstructor
    def __init__(self):
        self.fields = ["id", "tag_name", "desc", "pro_id"]

    @staticmethod
    def add_ca_tag(tag_name, pro_id, desc=None):
        with db.auto_commit():
            tag_info = Case_Tag()
            tag_info.tag_name = tag_name
            tag_info.pro_id = pro_id
            tag_info.desc = desc
            db.session.add(tag_info)
            db.session.flush()
            return tag_info

    @staticmethod
    def del_ca_tag(id):
        # 物理删除
        taget_sql = "DELETE FROM ca_tag WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def update_ca_tag(id, tag_name):
        Case_Tag.query.filter_by(id=id).update(
            {
                "tag_name": tag_name,
            }
        )
        db.session.commit()

    @staticmethod
    def get_category_list(pro_id):
        result = Case_Tag.query.filter_by(pro_id=pro_id, status=1).all()
        tag_list = []
        for i in result:
            children = []
            for n in i.tag_detail:
                data = {"case_id": n.id, "label": n.case_name}
                children.append(data)
            if len(children) > 0:
                tags = {"id": i.id, "label": i.tag_name, "children": children}
            else:
                tags = {"id": i.id, "label": i.tag_name, "children": []}
            tag_list.append(tags)
        return tag_list
