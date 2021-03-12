#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :hook.py
@说明        :
@时间        :2020/08/11 14:00:54
@作者        :Leo
@版本        :1.0
"""

from sqlalchemy import text

from app.libs.tools_func import serialize_sqlalchemy_obj
from app.models.api import Api
from app.models.base import Base, db


class Hook(Base):

    __tablename__ = "hook"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    code = db.Column(db.Text, comment="Hook代码", nullable=True)
    pro_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))
    api_id = db.Column(db.Integer, db.ForeignKey("api.id", ondelete="CASCADE"))
    fun_name = db.Column(db.String(500), comment="函数名")
    desc = db.Column(db.String(500), comment="描述")
    __table_args__ = (db.UniqueConstraint("id", "pro_id"),)

    @staticmethod
    def add_hook(pro_id, code, desc, fun_name, api_id=None):
        with db.auto_commit():
            hook = Hook()
            hook.pro_id = pro_id
            hook.code = code
            hook.desc = desc
            hook.api_id = api_id
            hook.fun_name = fun_name
            db.session.add(hook)
            db.session.flush()
            return hook

    @staticmethod
    def add_ApiHook(pro_id, api_id, fun_name, code):
        with db.auto_commit():
            hook = Hook()
            hook.pro_id = pro_id
            hook.code = code
            hook.api_id = api_id
            hook.fun_name = fun_name
            db.session.add(hook)
            db.session.flush()
            return hook

    @staticmethod
    def update_Hook(id, code, desc, fun_name, api_id=None):
        Hook.query.filter_by(id=id).update(
            {"code": code, "fun_name": fun_name, "api_id": api_id, "desc": desc}
        )
        db.session.commit()

    @staticmethod
    def update_ApiHook(id, code, fun_name):
        Hook.query.filter_by(id=id).update({"code": code, "fun_name": fun_name})
        db.session.commit()

    @staticmethod
    def is_empty_hook_detail(pro_id):
        data = Hook.query.filter_by(pro_id=pro_id).first()
        res = {"project_id": data.pro_id, "code": data.code, "id": data.id}
        return res

    @staticmethod
    def _hook_is_activite_by_api(func_name, api_id=None, pro_id=None):
        """[summary]
        函数在api中是否使用
        Args:
            func_name ([type]): [description]
            api_id ([type], optional): [description]. Defaults to None.
            pro_id ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        api_ids = []
        if api_id:
            taget_sql = "SELECT * FROM module WHERE find_in_set(:func_name, func_name) and api_id =:api_id"
            result = db.session.execute(
                text(taget_sql), {"func_name": func_name, "api_id": api_id}
            ).fetchall()
            is_activite = serialize_sqlalchemy_obj(result)
        else:
            Api_info = Api.query.filter_by(pro_id=pro_id).all()
            if len(Api_info) > 0:
                for i in Api_info:
                    api_ids.append(i.id)
            if len(api_ids) > 0:
                apis = ",".join("%s" % a for a in api_ids)
                taget_sql = "SELECT * FROM module WHERE find_in_set(:func_name, func_name) and api_id in ({}) ".format(
                    apis
                )
                result = db.session.execute(
                    text(taget_sql), {"func_name": func_name}
                ).fetchall()
                is_activite = serialize_sqlalchemy_obj(result)
        return is_activite

    @staticmethod
    def _hook_is_activite_by_case(func_name, pro_id):
        """[summary]
        函数在case中是否使用
        Args:
            func_name ([type]): [description]
            api_id ([type], optional): [description]. Defaults to None.
            pro_id ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        module_ids = []
        case_ids = []
        cases = "SELECT id,case_name FROM `case` WHERE pro_id =:pro_id"
        case_result = db.session.execute(text(cases), {"pro_id": pro_id}).fetchall()
        cases_info = serialize_sqlalchemy_obj(case_result)
        if len(cases_info) > 0:
            for i in cases_info:
                case_ids.append(i["id"])
        if len(case_ids) > 0:
            pro_all_case = ",".join("%s" % a for a in case_ids)
        modules = "SELECT id,name FROM `case_module` WHERE case_id in ({}) ".format(
            pro_all_case
        )
        modules_result = db.session.execute(
            text(modules), {"pro_id": pro_id}
        ).fetchall()
        modules_info = serialize_sqlalchemy_obj(modules_result)
        if len(modules_info) > 0:
            for i in modules_info:
                module_ids.append(i["id"])
        if len(module_ids) > 0:
            case_all_modules = ",".join("%s" % a for a in module_ids)
        taget_sql = "SELECT * FROM `case_module` WHERE find_in_set(:func_name, func_name) and id in ({}) ".format(
            case_all_modules
        )
        result = db.session.execute(
            text(taget_sql), {"func_name": func_name}
        ).fetchall()
        is_activite = serialize_sqlalchemy_obj(result)
        return is_activite

    @staticmethod
    def del_hook(id):
        taget_sql = "DELETE FROM hook WHERE id=:id"
        db.session.execute(text(taget_sql), {"id": id})

    @staticmethod
    def order_by_hook_id(pro_id, fun_name, id):
        taget_sql = "SELECT * FROM hook WHERE pro_id =:pro_id and fun_name=:fun_name and id !=:id"
        result = db.session.execute(
            text(taget_sql), {"pro_id": pro_id, "fun_name": fun_name, "id": id}
        ).fetchall()
        is_activite = serialize_sqlalchemy_obj(result)
        return is_activite
