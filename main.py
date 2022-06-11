#!-*-coding:utf-8 -*-
# python3.7
# @Author: F___Q
# Create time: 2022/6/11 16:51
# Filename:

import flask_app

from logic import Logic
from conf import base_conf


def app_init():
    flask_app.logic = Logic()


app = flask_app.app
app_init()


if __name__ == '__main__':
    app.run(
        host=base_conf.HOST,
        port=base_conf.PORT,
        threaded=base_conf.USE_THREAD
    )
