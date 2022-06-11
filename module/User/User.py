#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 21:45
# Filename:用户对象
from constant import constants
from utils import sql_builder, sql_execute, db


class User:

    table = 'user'

    def __init__(self, uid):
        self.__uid = uid
        self.__username = None
        self.__email = None
        self.get_user()

    @property
    def uid(self):
        return self.__uid

    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    def get_user(self):
        sql, args = sql_builder.gen_select_sql(User.table, ['%*'], condition={'id': self.__uid}, limit=1)
        res = sql_execute.mysql_execute_sqls([{'sql': sql, 'args': args}])['result'][0]
        # TODO：未找到该用户时的处理
        self.__username = res['username']
        self.__email = res['email']

    # 返回给前端界面的用户信息
    def ui_user_info(self):
        user_info = {
            'id': self.__uid,
            'name': self.__username,
            'email': self.__email,
        }
        return user_info


def insert_user_redis(token, uid):
    """
    在redis中录入用户token和uid
    :param token:
    :param uid:
    :return:
    """
    r = db.get_db('user', 'redis')
    # 设置值，只有name不存在时，执行设置操作（添加）
    result = r.setnx(token, uid, px=constants.TOKEN_EXPIRE_TIME)
    return result


def load_user_redis(token):
    """
    从redis读取用户uid
    :param token:
    :return:
    """
    r = db.get_db('user', 'redis')
    result = r.get(token)
    # TODO：更新过期时间
    return result
