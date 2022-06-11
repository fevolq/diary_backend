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
    """生成随机固定字符串"""
    if SALT_LENGTH <= 0:
        raise ValueError("Salt length must be positive")

    return "".join(secrets.choice(CHARS) for _ in range(SALT_LENGTH))


def bcrypt_pwd(password) -> str:
    """
    对明文密码初次加密
    :param password: 明文密码
    :return:
    """
    bcrypt_str = bcrypt.hashpw(password.encode(), SECRET_KEY.encode())
    return bcrypt_str.decode()


def gen_bcrypt_str(password, salt) -> str:
    bcrypt_str = bcrypt_pwd(password)
    if salt[-1].isdigit():
        result = hashlib.md5(str(salt + bcrypt_str).encode("utf8"))
    else:
        result = hashlib.sha1(str(salt + bcrypt_str).encode("utf8"))
    return result.hexdigest()


def check_pwd(password, salt_record, bcrypt_str_record):
    bcrypt_str = gen_bcrypt_str(password, salt_record)
    return bcrypt_str == bcrypt_str_record


def gen_token() -> str:
    token = "".join(secrets.choice(CHARS) for _ in range(32))
    return token
