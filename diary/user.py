#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 19:55
# Filename: 用户注册、登录与退出

from flask import Blueprint, request, session, g

from constant import gen_response
from utils import sql_builder, sql_execute
from .module.User import user_token, User


# 蓝图注册：url_prefix会加在所有route之前
user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/register')
def register():
    if request.method != 'POST':
        return gen_response.error_response()

    form_data = request.form
    username = form_data.get('username', '')
    email = form_data.get('email', '')
    pwd = form_data.get('pwd', '')

    message_content = None
    table = 'user'
    if not username:
        message_content = 'Username is required'
    elif not email:
        message_content = 'Email is required'
    elif not pwd:
        message_content = 'Password is required'
    else:
        sql, args = sql_builder.gen_select_sql(table, ['%*'], condition={'email': email}, limit=1)
        res = sql_execute.mysql_execute_sqls([{'sql': sql, 'args': args}])
        if res.get('result', 1) != 0:
            message_content = f'Email {email} is already registered'
        else:
            salt = user_token.gen_salt()
            token = user_token.gen_token(pwd, salt)
            row = {'name': username, 'email': email, 'salt': salt, 'token': token}
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
    if request.method != 'POST':
        return gen_response.error_response()

    form_data = request.form
    email = form_data.get('email', '')
    pwd = form_data.get('pwd', '')

    message_content = None
    table = 'user'
    if not email:
        message_content = 'Email is required'
    elif not pwd:
        message_content = 'Password is required'
    else:
        sql, args = sql_builder.gen_select_sql(table, ['salt', 'token'], condition={'email': email}, limit=1)
        res = sql_execute.mysql_execute_sqls([{'sql': sql, 'args': args}])
        if res.get('result', 0) != 1:
            message_content = f'Email {email} is not registered'
        else:
            salt = res['result'][0]['salt']
            token = res['result'][0]['token']
            if not user_token.check_token(pwd, salt, token):
                message_content = 'Password is error'
            else:
                session.clear()
                session['user'] = User.User(token).ui_user_info()

    if message_content is not None:
        response = gen_response.error_response(message_content)
    else:
        response = gen_response.success_response()

    return response


@user_bp.route('/logout')
def logout():
    session.clear()
    return gen_response.success_response()


@user_bp.before_app_request
def load_logged_in_user():
    user = session.get('user', None)
    if user is None:
        g.user = None
    else:
        if User.User.check_user(user['id'], user['token']):
            g.user = User.User(user['token'])
        else:
            return gen_response.error_response()


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#
#         return view(**kwargs)
#
#     return wrapped_view
