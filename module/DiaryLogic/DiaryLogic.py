#!-*-coding:utf-8 -*-
# python3.7
# @Author: F___Q
# Create time: 2022/6/5 15:37
# Filename:
import flask

from flask_app import api_route
from constant import gen_response
from utils import sql_builder, sql_execute


class DiaryLogic:

    def __init__(self):
        pass

    @api_route('test', methods=['GET', 'POST'])
    def test(self, request, req_dic):
        resp = gen_response.success_response()
        resp.update({'meg': 'test'})
        return resp
