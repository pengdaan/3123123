#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :project.py
@说明        :项目表
@时间        :2020/08/11 08:58:49
@作者        :Leo
@版本        :1.0
"""
from sqlalchemy import text

from flask_sqlalchemy import orm
from app.models.api import Api
from app.models.base import Base, db
from app.models.case import Case
from app.models.case_detail import Case_Detail
from app.models.user import User


class Project(Base):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    project_name = db.Column(db.String(255), nullable=False, comment="项目名称")
    desc = db.Column(db.String(255), nullable=True, comment="项目描述")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    # relationship 连表查询， backref[1对多]
    user_detail = db.relationship("User", backref="user_detail")

    @orm.reconstructor
    def __init__(self):
        self.fields = ["id", "project_name", "desc", "user_id", "user_detail"]

    @staticmethod
    def add_project(project_name, desc, user_id):
        """[summary]

        Args:
            project_name ([type]): [description]
            desc ([type]): [description]
            user_id ([type]): [description]
        """
        with db.auto_commit():
            project = Project()
            project.project_name = project_name
            project.desc = desc
            project.user_id = user_id
            db.session.add(project)
            db.session.flush()
            return project

    @staticmethod
    def update_project(project_id, project_name, desc, status=1):
        Project.query.filter_by(id=project_id).update(
            {"project_name": project_name, "desc": desc, "status": status}
        )
        db.session.commit()

    @staticmethod
    def del_project(project_id):
        taget_sql = "DELETE FROM project WHERE id=:project_id"
        db.session.execute(text(taget_sql), {"project_id": project_id})

    @staticmethod
    def get_tasks_project(page):
        if page == 1:
            res = Project.query.limit(5).offset(0).all()
        else:
            page = int(page - 1) * 5
            res = Project.query.limit(5).offset(page).all()
        count = Project.query.count()
        project_list = []
        for i in res:
            api_count = Api.query.filter_by(pro_id=i.id).count()
            case_count = Case.query.filter_by(pro_id=i.id).count()
            case_detail = Case.query.filter_by(pro_id=i.id).all()
            case_detail_list = []
            for c in case_detail:
                this_case_detail_Count = Case_Detail.query.filter_by(
                    case_id=c.id
                ).count()
                this_user_name = User.query.filter_by(id=c.user_id).first()
                this_case_detail = {
                    "pro_id": c.pro_id,
                    "case_id": c.id,
                    "case_name": c.case_name,
                    "user_id": this_user_name.username,
                    "count": this_case_detail_Count,
                }
                case_detail_list.append(this_case_detail)
            project = {
                "id": i.id,
                "project_name": i.project_name,
                "desc": i.desc,
                "api_count": api_count,
                "case_count": case_count,
                "project_case_detail": case_detail_list,
            }
            project_list.append(project)
        return {"tasks_list": project_list, "count": count}
