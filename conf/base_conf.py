#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 22:30
# Filename: 应用配置

from constant import env_code

HOST = '0.0.0.0'
PORT = 9527
ENV = env_code.DEV

USE_THREAD = False

NOT_CHECK_API = ['/', '/user/register', '/user/login']
