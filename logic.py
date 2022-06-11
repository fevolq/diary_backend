#!-*-coding:utf-8 -*-
# python3.7
# @Author: F___Q
# Create time: 2022/6/11 17:15
# Filename:

from diary.module.DiaryLogic.DiaryLogic import DiaryLogic


class Logic:

    def __init__(self):
        self._diary = DiaryLogic()

    def call(self, api_path: str, func, request, req_dic):
        return func(self._diary, request, req_dic)

    def before_call(self, api_path, request):
        pass

    def after_call(self, request, req_obj, api_path, respond):
        return respond
