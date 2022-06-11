import logging

from utils import color_func


def raise_exception(exception_str):
    raise Exception(logging.log(logging.ERROR, color_func.normal_magenta(exception_str)))


def important_log(important_str):
    logging.log(logging.INFO, color_func.normal_yellow(important_str))
