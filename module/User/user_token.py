#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 21:10
# Filename: 生成与校验token
import hashlib
import secrets

SALT_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.!?[]%#@&*"
salt_length = 16


def gen_salt() -> str:
    """Generate a random string of SALT_CHARS with specified ``length``."""
    if salt_length <= 0:
        raise ValueError("Salt length must be positive")

    return "".join(secrets.choice(SALT_CHARS) for _ in range(salt_length))


def gen_token(password, salt) -> str:
    if salt[-1].isdigit():
        result = hashlib.md5(str(salt+password).encode("utf8"))
    else:
        result = hashlib.sha1(str(salt+password).encode("utf8"))
    return result.hexdigest()


def check_token(password, salt_record, token_record):
    token = gen_token(password, salt_record)
    return token == token_record
