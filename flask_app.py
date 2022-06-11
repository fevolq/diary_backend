#!-*-coding:utf-8 -*-
# python3.7
# @Author: F___Q
# Create time: 2022/6/11 16:51
# Filename:
import datetime
import logging
import random
import time
from functools import wraps

import flask
from flask import Flask, request, session, g
from flask.typing import ResponseReturnValue
from flask.views import View

from conf import reg_route
from module.User import User
from utils import util, db
from constant import gen_response

# 日志初始化
util.init_logging('')


def create_app(secret_key='dev'):
    flask_app = Flask(__name__)
    flask_app.config.from_mapping(
        SECRET_KEY=secret_key,
    )

    @flask_app.route('/')
    def hello():
        return 'Hello World!!!'

    # 注册蓝图
    for bp in reg_route.bp_route:
        # TODO: 加入蓝图的注册日志
        flask_app.register_blueprint(bp)

    return flask_app


app: Flask = create_app()

logic = None


class TemplateView(View):

    def __init__(self, api_path, func):
        self.api_path = api_path
        self.func = func

    def dispatch_request(self) -> ResponseReturnValue:
        now = time.time()
        logging.info(f'开始时间：{util.time2str(now)}')
        required_id = str(int(now*1000)) + ''.join([str(random.randint(1, 10)) for _ in range(6)])
        g_call = g_args('call')
        g_call['required_id'] = required_id
        try:
            logic.before_call(self.api_path, request)
            if request.is_json:
                req_dic = request.get_json(force=True)
            else:
                req_dic = request.get_data().decode()
            respond = logic.call(self.api_path, self.func, request, req_dic)
            respond = logic.after_call(request, req_dic, self.api_path, respond)
        except Exception as e:
            logging.exception(e)
            respond = gen_response.error_response()
        finally:
            logging.info(f'结束时间：{util.time2str()}')
            return respond


# 全局g参数
def g_args(args):
    value = flask.g.get(args, None)
    if value is None:
        setattr(flask.g, args, {})
    return getattr(flask.g, args)


@app.before_request
def before_call():
    if request.path not in ('/user/register', '/user/login'):
        # 与全局变量中加入用户对象
        token = session.get('token', None)
        if token is None:
            return gen_response.error_response('请重新登录')
        uid = User.load_user_redis(token)
        if uid is None:
            return gen_response.error_response('请重新登录')
        user = User.User(uid)
        user_info = g_args('user_info')
        user_info['user'] = user


@app.after_request
def after_call(response):
    db.close_db()
    return response


# 注册路由
def api_route(api_path, **api_kwargs):
    def reg_api(func):
        reg_api_path = f'/{api_path}'
        methods = api_kwargs.get('methods', None)
        if not methods:
            methods = ['POST']
        elif isinstance(methods, str):
            methods = [methods]
        else:
            pass
        app.add_url_rule(reg_api_path,
                         view_func=TemplateView.as_view(api_path,
                                                        api_path=api_path,
                                                        func=func),
                         methods=methods)
        logging.info(f'reg api: {reg_api_path}, methods: {methods}, func: {func.__name__}')
        @wraps(func)
        def reg_log(*args, **kwargs):
            logging.info(f'call api: {reg_api_path}, func: {func.__name__}')
            return func(*args, **kwargs)
        return reg_log
    return reg_api
