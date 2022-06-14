#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 21:45
# Filename:用户对象
import copy
import json

from constant import constants
from utils import sql_builder, sql_execute, db


class User:

    table = 'user'

    def __init__(self, uid):
        self.__uid = uid
        self.__name = None
        self.__email = None
        self.get_user()

    @property
    def uid(self):
        return self.__uid

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    def get_user(self):
        sql, args = sql_builder.gen_select_sql(User.table, ['%*'], condition={'id': {'=': self.__uid}}, limit=1)
        res = sql_execute.mysql_execute_sqls([{'sql': sql, 'args': args}])
        if res.get('result', []):
            self.__name = res['result'][0]['name']
            self.__email = res['result'][0]['email']

    # 返回给前端界面的用户信息
    def ui_user_info(self):
        user_info = {
            'id': self.__uid,
            'name': self.__name,
            'email': self.__email,
        }
        return user_info


def insert_user_redis(token, user_info, is_update=False):
    """
    在redis中录入用户token和uid
    :param token: 用户token
    :param user_info: 用户信息
    :param is_update: 是否更新
    :return:
    """
    r = db.get_db('user', 'redis')
    result = r.set(token, json.dumps(user_info), ex=constants.TOKEN_EXPIRE_TIME, nx=is_update)
    return result


def load_user_redis(token):
    """
    从redis读取用户uid
    :param token:
    :return:
    """
    r = db.get_db('user', 'redis')
    result = r.get(token)
    if result:
        result = json.loads(result.decode('utf-8'))
        # 更新过期时间
        insert_user_redis(token, copy.deepcopy(result), is_update=True)
    return result
