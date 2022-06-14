#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 19:55
# Filename: 用户注册、登录与退出
import flask
from flask import Blueprint, request, session, g

from constant import gen_response
from utils import sql_builder, sql_execute
from module.User import User
from module.User import user_token

# 蓝图注册：url_prefix会加在所有route之前
user_bp = Blueprint('user', __name__, url_prefix='/user')
# TODO：蓝图的POST请求


@user_bp.route('/register')
def register():
    # if request.method != 'POST':
    #     return gen_response.error_response()

    form_data = request.form
    username = form_data.get('username', '')
    email = form_data.get('email', '')
    pwd = form_data.get('pwd', '')

    message_content = None
    table = User.User.table
    if not username:
        message_content = 'Username is required'
    elif not email:
        message_content = 'Email is required'
    elif not pwd:
        message_content = 'Password is required'
    else:
        sql, args = sql_builder.gen_select_sql(table, ['%*'], condition={'email': {'=': email}}, limit=1)
        res = sql_execute.mysql_execute_sqls([{'sql': sql, 'args': args}])
        if res.get('result', []):
            message_content = f'Email {email} is already registered'
        else:
            salt = user_token.gen_salt()
            bcrypt_str = user_token.gen_bcrypt_str(pwd, salt)
            row = {'name': username, 'email': email, 'salt': salt, 'bcrypt_str': bcrypt_str}
            ins_sql, ins_args = sql_builder.gen_insert_sql(table, row)
            ins_res = sql_execute.mysql_execute_sqls([{'sql': ins_sql, 'args': ins_args}])
            if 'error' in ins_res:
                message_content = 'registration failed'

    if message_content is not None:
        response = gen_response.error_response(message_content)
    else:
        response = gen_response.success_response()

    return response


@user_bp.route('/login')
def login():
    # TODO：要使用POST
    # if request.method != 'POST':
    #     return gen_response.error_response()

    form_data = request.form
    email = form_data.get('email', '')
    pwd = form_data.get('pwd', '')

    message_content = None
    table = User.User.table
    if not email:
        message_content = 'Email is required'
    elif not pwd:
        message_content = 'Password is required'
    else:
        sql, args = sql_builder.gen_select_sql(table, ['id', 'salt', 'bcrypt_str'], condition={'email': {'=': email}}, limit=1)
        res = sql_execute.mysql_execute_sqls([{'sql': sql, 'args': args}])
        if not res.get('result', []):
            message_content = f'Email {email} is not registered'
        else:
            uid = res['result'][0]['id']
            salt = res['result'][0]['salt']
            bcrypt_str = res['result'][0]['bcrypt_str']
            if not user_token.check_pwd(pwd, salt, bcrypt_str):     # 校验密码
                message_content = 'Password is error'
            else:
                session.clear()
                token = user_token.gen_token()
                result = User.insert_user_redis(token, {'id': uid, 'email': email})
                if result:
                    session['token'] = token
                else:
                    message_content = '登录失败，请重新尝试登录'

    if message_content is not None:
        response = gen_response.error_response(message_content)
    else:
        response = gen_response.success_response()
        # TODO: token的返回优化
        response['token'] = session['token']

    return response


@user_bp.route('/logout')
def logout():
    session.clear()
    return gen_response.success_response()


@user_bp.route('/info')
def info():
    response = gen_response.success_response()
    user_info = flask.g.user_info    # 用户相关的对象
    response.update({'info': user_info['user'].ui_user_info()})
    return response
