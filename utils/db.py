#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 19:05
# Filename:数据库的连接
import pymysql
import redis as redis
from flask import g

from conf import db_conf


def get_db(db_name: str, db_type: str = 'mysql'):
    """

    :param db_name: 数据库名
    :param db_type: 数据库类型
    :return: 数据库的连接
    """
    dbs = g.setdefault('dbs', {})
    db_name = db_name.lower()
    db_type = db_type.lower()
    if not dbs.get(db_type, {}):
        if db_type.lower() == 'mysql':
            conn = mysql_conn(db_name)
            dbs[db_type][db_name] = conn
        elif db_type.lower() == 'redis':
            conn = redis_conn(db_name)
            dbs[db_type][db_name] = conn
        else:
            raise Exception(f'没有{db_type}数据库类型')
    else:
        conn = dbs[db_type][db_name]
    return conn


def close_db():
    dbs = g.pop('dbs', {})
    for db_type in dbs:
        for db in dbs[db_type]:
            dbs[db_type][db].close()


def mysql_conn(db_name):
    conn = None
    if db_name == 'diary':
        conn = pymysql.connect(host=db_conf.MYSQL_HOST,
                               port=db_conf.MYSQL_PORT,
                               user=db_conf.MYSQL_USER,
                               passwd=db_conf.MYSQL_PWD,
                               db=db_conf.MYSQL_DB,
                               connect_timeout=15.0,
                               charset='utf8',
                               autocommit=True,
                               cursorclass=pymysql.cursors.DictCursor
                               )
    else:
        raise Exception(f'Mysql中没有 {db_name} 实例')
    return conn


def postgres_conn(db_name):
    conn = None
    if db_name == 'diary':
        pass
        # conn = pymysql.connect(host=conf.MYSQL_HOST,
        #                        port=conf.MYSQL_PORT,
        #                        user=conf.MYSQL_USER,
        #                        passwd=conf.MYSQL_PWD,
        #                        db=conf.MYSQL_DB,
        #                        connect_timeout=15.0,
        #                        charset='utf8',
        #                        autocommit=True,
        #                        cursorclass=pymysql.cursors.DictCursor
        #                        )
    else:
        raise Exception(f'Postgres中没有 {db_name} 实例')
    return conn


def redis_conn(db_name):
    if db_name in db_conf.REDIS_DB:
        conn = redis.StrictRedis(host=db_conf.REDIS_HOST,
                                 port=db_conf.REDIS_PORT,
                                 username=db_conf.REDIS_USER,
                                 password=db_conf.REDIS_PWD,
                                 db=db_conf.REDIS_DB[db_name])
    else:
        raise Exception(f'Redis中没有 {db_name} 实例')
    return conn
