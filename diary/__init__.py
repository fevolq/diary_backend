#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 18:50
# Filename:

import os
import datetime
import time
import random
import logging

from flask import Flask, g

from conf import base_conf, reg_route


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_mapping(
        SECRET_KEY='dev',
    )

    @flask_app.route('/')
    def hello():
        return 'Hello World!!!'

    # 注册蓝图
    for bp in reg_route.bp_route:
        flask_app.register_blueprint(bp)

    return flask_app


app = None

# @app.before_request
# def before_call():
#     now = time.time()
#     required_id = str(int(now)) + ''.join([random.randint(1, 10) for _ in range(6)])
#     call = {
#         'start': str(datetime.datetime.fromtimestamp(now)),
#         'start_time': now,
#         'required_id': required_id
#     }
#         g.call = call
#
#
# @app.after_request
# def after_call(response):
#     start_time = g.call['start_time']
#     now = time.time()
#     logging.log(logging.INFO, f'耗费时间：{int(now) - int(start_time)}')


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=base_conf.HOST,
        port=base_conf.PORT,
        # env=base_conf.ENV
    )
