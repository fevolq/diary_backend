#!-*-coding:utf-8 -*-
# python3.7
# @Author:fuq666@qq.com
# Create time: 2022/6/4 20:15
# Filename:

from .db import get_db


def mysql_execute(sql: str, args: list = [], db_name='diary'):
    """
    :param sql:
    :param args:
    :param db_name:
    :return:
    """
    conn = get_db(db_name, db_type='mysql')
    cursor = conn.cursor()
    try:
        sql = sql.replace('\'%s\'', '%s').strip()
        if sql.startswith('SELECT'):
            cursor.execute(sql, args)
            result = cursor.fetchall()
        else:
            if not args:
                result = cursor.execute(sql, args)
            elif isinstance(args[0], (list, tuple)):
                result = cursor.executemany(sql, args)
            else:
                result = cursor.execute(sql, args)
        conn.commit()
        res = {'result': result}
    except Exception as e:
        conn.rollback()
        res = {'error': str(e)}
    return res


def mysql_execute_sqls(sql_with_args_list: list, db_name='diary'):
    """
    :param sql_with_args_list: [{'sql': sql_str, 'args': args_list}, ]
    :param db_name: 指定数据库
    :return:
    """
    conn = get_db(db_name, db_type='mysql')
    cursor = conn.cursor()
    try:
        result_list = [[]] * len(sql_with_args_list)
        res = {'result': result_list}
        for sql_with_args in sql_with_args_list:
            sql = sql_with_args['sql'].replace('\'%s\'', '%s').strip()
            args_list = sql_with_args.get('args', [])
            if sql.startswith('SELECT'):
                cursor.execute(sql, args_list)
                result = cursor.fetchall()
                result_list[sql_with_args_list.index(sql_with_args)] = result
            else:
                if not args_list:
                    res_line = cursor.execute(sql, args_list)
                elif isinstance(args_list[0], (list, tuple)):
                    res_line = cursor.executemany(sql, args_list)
                else:
                    res_line = cursor.execute(sql, args_list)
                result_list[sql_with_args_list.index(sql_with_args)] = res_line
        if len(sql_with_args_list) == 1:
            res['result'] = result_list.copy()[0]
        conn.commit()
    except Exception as e:
        conn.rollback()
        res = {'error': str(e)}
    return res
