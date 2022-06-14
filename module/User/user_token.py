#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 21:10
# Filename: 生成与校验token
import hashlib
import secrets

import bcrypt

CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.!?[]%#@&*"
SALT_LENGTH = 16
SECRET_KEY = 'F___Q'


def gen_salt() -> str:
    # """生成随机固定字符串"""
    # if SALT_LENGTH <= 0:
    #     raise ValueError("Salt length must be positive")
    #
    # return "".join(secrets.choice(CHARS) for _ in range(SALT_LENGTH))
    return bcrypt.gensalt(rounds=SALT_LENGTH).decode()


def bcrypt_pwd(password) -> str:
    """
    对明文密码初次加密
    :param password: 明文密码
    :return:
    """
    result = hashlib.sha1(str(SECRET_KEY + password).encode("utf8")).hexdigest()
    return result


def gen_bcrypt_str(password, salt) -> str:
    result = bcrypt_pwd(password)
    bcrypt_str = bcrypt.hashpw(result.encode(), salt.encode()).decode()
    return bcrypt_str


def check_pwd(password, salt_record, bcrypt_str_record):
    bcrypt_str = gen_bcrypt_str(password, salt_record)
    return bcrypt_str == bcrypt_str_record


def gen_token() -> str:
    token = "".join(secrets.choice(CHARS) for _ in range(32))
    return token
