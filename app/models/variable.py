#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :variable.py
@说明        :
@时间        :2021/04/20 16:58:32
@作者        :Leo
@版本        :1.0
'''

from sqlalchemy import text
from app.models.base import Base, db
from app.models.module import Module
from app.models.case import Case
from app.models.case_module import CaseModule
from app.models.api import Api


class Variable(Base):
    __tablename__ = "variable"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    name = db.Column(db.String(255), nullable=False, comment="变量名")
    data = db.Column(db.Text, nullable=True, comment="变量详情")
    api_id = db.Column(db.Integer, db.ForeignKey('api.id', ondelete="CASCADE"))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id', ondelete="CASCADE"))
    pro_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"))
    case_id = db.Column(db.Integer, db.ForeignKey('case.id', ondelete="CASCADE"))
    case_module_id = db.Column(db.Integer, db.ForeignKey('case_module.id', ondelete="CASCADE"))

    __table_args__ = (db.UniqueConstraint("name", "pro_id"),)

    @staticmethod
    def add_variable(name, case_id, pro_id, api_id, module_id, case_module_id):
        with db.auto_commit():
            variable = Variable()
            variable.name = name
            variable.api_id = api_id
            variable.pro_id = pro_id
            variable.case_id = case_id
            variable.module_id = module_id
            variable.case_module_id = case_module_id
            variable.status = 1
            db.session.add(variable)
            db.session.flush()
            return variable

    @staticmethod
    def update_variable_status(id, status, data, name):
        Variable.query.filter_by(id=id).update(
            {
                "status": status,
                "data": str(data),
                "name": name
            }
        )
        db.session.commit()

    @staticmethod
    def get_variable_list(pro_id, api_id=None, case_id=None):
        variable_list = []
        if api_id:
            res = Variable.query.filter_by(pro_id=pro_id, api_id=api_id, status=1).all()
        elif case_id:
            res = Variable.query.filter_by(pro_id=pro_id, case_id=case_id, status=1).all()
        else:
            res = Variable.query.filter_by(pro_id=pro_id, status=1).all()
        for i in res:
            variable = {}
            variable.update({"id": i.id, "name": i.name, "pro_id": i.pro_id, "api_id": i.api_id, "module_id": i.module_id, "case_id": i.case_id, "case_module_id": i.case_module_id, "data": i.data})
            variable_list.append(variable)
        return variable_list

    @staticmethod
    def get_variable_detail(pro_id, name):
        variable = {}
        res = Variable.query.filter_by(pro_id=pro_id, name=name, status=1).first()
        if res:
            variable.update({"id": res.id, "name": res.name, "data": res.data})
        return variable

    @staticmethod
    def get_variable(name):
        ModuleInfo = Module.query.filter(Module.body.like("%" + name + "%")).all()
        apis_detail = []
        cases_detail = []
        for i in ModuleInfo:
            apis = {}
            ApiInfo = Api.query.filter_by(id=i.api_id).first()
            apis.update({"api_id": i.api_id, "api_name": ApiInfo.name, "module_id": i.id, "module_name": i.name})
            apis_detail.append(apis)
        CaseModuleInfo = CaseModule.query.filter(CaseModule.body.like("%" + name + "%")).all()
        for k in CaseModuleInfo:
            cases = {}
            CaseInfo = Case.query.filter_by(id=k.case_id).first()
            cases.update({"case_id": k.case_id, "case_name": CaseInfo.case_name})
            cases_detail.append(cases)
        res = {"apis_detail": apis_detail, "cases_detail": cases_detail}
        return res

    @staticmethod
    def del_variable(id):
        # 物理删除
        taget_sql = "DELETE FROM `variable` WHERE `id`=:id"
        db.session.execute(text(taget_sql), {"id": id})
