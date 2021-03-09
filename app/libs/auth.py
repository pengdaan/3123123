#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :auth.py
@说明        :令牌生成器
@时间        :2020/08/07 09:43:16
@作者        :Leo
@版本        :1.0
"""

import time
from functools import wraps

import jwt
from flask import current_app, g, request

from app.libs.code import AuthFailed
from app.models.user import User


def luna_auth_token(account, username):
    """[summary]
    载荷（Payload）
    iss: jwt签发者
    sub: jwt所面向的用户
    aud: 接收jwt的一方
    exp: jwt的过期时间，这个过期时间必须要大于签发时间
    nbf: 定义在什么时间之前，该jwt都是不可用的.
    iat: jwt的签发时间
    jti: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。

    Args:
        account ([type]): 用户id
        username ([type]): 用户名
    """
    t = int(time.time())
    # token的有效期设置为半年
    token = {
        "iat": t,
        "exp": t + 15778463, 
        "sub": account,
        "username": username,
        "user_id": account,
    }
    # 有效载体,进行加密签名的密钥,指明签名算法方式
    return jwt.encode(token, current_app.config["SECERET_KEY"], algorithm="HS256")


def verify_refresh_token(token):
     # raise AuthFailed(data="Error token", code=2002)
    try:
        decode_token = jwt.decode(
            token, current_app.config["SECERET_KEY"], algorithm="HS256"
        )
        if decode_token:
            # g变量是线程隔离的，不会出现数据错乱
            g.user = decode_token["user_id"]
            return decode_token
    except jwt.ExpiredSignatureError:
        # token有效时间判断
        User.update_user_status(token, 0)
        raise AuthFailed(data="Token has expired", code=2001)
    except jwt.InvalidTokenError:
        # token是否正确判断
        User.update_user_status(token, 0)
        raise AuthFailed(data="Error token", code=2002)


def auth_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Token")
        User.query.filter_by(token=token).first_or_404("token")
        if not token:
            raise AuthFailed(msg="Token has expired", code=2001)
        else:
            user = verify_refresh_token(token)
            UserList = User.get_login_user_list()
            if user["user_id"] not in UserList:
                raise AuthFailed(msg="User does not exist", code=2003)
            else:
                return func(*args, **kwargs)

    return wrapper
