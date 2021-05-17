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


class Category(Base):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    category_name = db.Column(db.String(255), nullable=False, comment="分类名称",index=True)
    desc = db.Column(db.String(255), nullable=True, comment="分类描述")
    pro_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))
    __table_args__ = (db.UniqueConstraint("category_name", "pro_id"),)

    @orm.reconstructor
    def __init__(self):
        self.fields = ["id", "category_name", "desc", "pro_id"]

    @staticmethod
    def add_category(category_name, pro_id, desc=None):
        with db.auto_commit():
            category_info = Category()
            category_info.category_name = category_name
            category_info.pro_id = pro_id
            category_info.desc = desc
            db.session.add(category_info)
            db.session.flush()
            return category_info

    @staticmethod
    def del_category(id):
        # 物理删除
        taget_sql = "DELETE FROM category WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def update_category(id, category_name):
        Category.query.filter_by(id=id).update(
            {
                "category_name": category_name,
            }
        )
        db.session.commit()

    @staticmethod
    def get_category_list(pro_id):
        result = Category.query.filter_by(pro_id=pro_id, status=1).all()
        category_list = []
        for i in result:
            children = []
            for n in i.category_detail:
                data = {"api_id": n.id, "label": n.name}
                children.append(data)
            if len(children) > 0:
                category = {"id": i.id, "label": i.category_name, "children": children}
            else:
                category = {"id": i.id, "label": i.category_name, "children": []}
            category_list.append(category)
        return category_list
