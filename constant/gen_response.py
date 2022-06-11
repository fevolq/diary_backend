#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 20:04
# Filename:

from flask import g

SUCCESS_CODE = 200
ERROR_CODE = 404
FAIL_CODE = 500


def success_response():
    return_response = {
        'code': SUCCESS_CODE,
    }
    if g.get('call', {}).get('required_id'):
        return_response['required_id'] = g.call['required_id']
    return return_response


def error_response(msg=''):
    return_response = {
        'code': ERROR_CODE,
    }
    if g.get('call', {}).get('required_id'):
        return_response['required_id'] = g.call['required_id']
    if msg:
        return_response['message_content'] = msg
    return return_response


def failure_response():
    return_response = {
        'code': FAIL_CODE,
    }
    if g.get('call', {}).get('required_id'):
        return_response['required_id'] = g.call['required_id']
    return return_response
