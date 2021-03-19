#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :user.py
@说明        :用户表
@时间        :2020/08/06 15:12:25
@作者        :Leo
@版本        :1.0
"""


from werkzeug.security import check_password_hash, generate_password_hash

from app.libs.code import AuthFailed
from flask_sqlalchemy import orm
from app.models.base import Base, db


class User(Base):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    username = db.Column(db.String(255), unique=True, nullable=False, comment="用户名")
    password = db.Column(db.String(255), nullable=False, comment="密码")
    email = db.Column(db.String(255), unique=True, nullable=False, comment="邮箱")
    token = db.Column(db.String(255), nullable=True, comment="token")

    @orm.reconstructor
    def __init__(self):
        # 指明需要序列化的key
        self.fields = ["id", "username", "email", "token"]

    @staticmethod
    def set_password(password):
        """
        对用户密码进行hash加密
        :param password:
        :return:
        """

        return generate_password_hash(password)

    @staticmethod
    def add_user(username, pwd, email):
        """
        注册用户
        :param user:
        :param pwd:
        :param email:
        :return:
        """
        with db.auto_commit():
            user = User()
            user.username = username
            user.password = user.set_password(pwd)
            user.email = email
            user.status = 0
            db.session.add(user)
            # 如果需要返回值时使用
            db.session.flush()
            return user.id

    @staticmethod
    def verify(username, password):
        """[summary]

        Args:
            username ([type]): 账号
            password ([type]): 密码

        Raises:
            NotFound: 用户不存在
            AuthFailed: 密码不正确

        Returns:
            [type]: 返回用户名，用户id
        """
        user = User.query.filter_by(username=username).first_or_404("username")
        if not user.check_password(password):
            raise AuthFailed(msg=" Incorrect account or password", error_code=3002)
        return {"uid": user.id, "username": user.username}

    def check_password(self, raw):
        if not self.password:
            return False
        return check_password_hash(self.password, raw)

    @staticmethod
    def add_token(userId, token):
        """[summary]

        Args:
            token ([type]): 系统令牌写入数据库

        Returns:
            [type]: [description]
        """
        with db.auto_commit():
            User.query.filter_by(id=userId).update({"status": 1, "token": token})
            db.session.commit()

    @staticmethod
    def update_user_status(args, status, type=1):
        if type == 1:
            with db.auto_commit():
                User.query.filter_by(token=args).update(
                    {
                        "status": status,
                    }
                )
                db.session.commit()
        else:
            with db.auto_commit():
                User.query.filter_by(id=args).update(
                    {
                        "status": status,
                    }
                )
                db.session.commit()

    @staticmethod
    def get_login_user_list(status=None):
        list = []
        if status:
            login_user_list = User.query.filter_by(status=1).all()
            for i in login_user_list:
                list.append(i.id)
            return list
        else:
            login_user_list = User.query.all()
            for i in login_user_list:
                list.append({"id": i.id, "name": i.username})
            return list

