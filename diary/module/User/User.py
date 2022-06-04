#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 21:45
# Filename:用户对象
from utils import sql_builder, sql_execute


class User:

    table = 'user'

    def __init__(self, token):
        self.__token = token
        self.__uid = None
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
        sql, args = sql_builder.gen_select_sql(User.table, ['%*'], condition={'token': self.__token}, limit=1)
        res = sql_execute.mysql_execute_sqls([{'sql': sql, 'args': args}])['result'][0]
        self.__uid = res['id']
        self.__username = res['username']
        self.__email = res['email']

    # 返回给前端界面的用户信息
    def ui_user_info(self):
        user = {
            'id': self.__uid,
            'name': self.__username,
            'email': self.__email,
            'token': self.__token
        }
        return user

    @staticmethod
    def check_user(uid, token):
        sql, args = sql_builder.gen_select_sql(User.table, ['id'], condition={'id': {'=': uid}, 'token': {'=': token}})
        res = sql_execute.mysql_execute_sqls([{'sql': sql, 'args': args}])
        correct = False
        if res['result']:
            correct = True
        return correct
