import base64
import binascii
import datetime
import hmac
import random
import sys
import uuid
import time
import os
import hashlib
import copy
import json
import logging
import logging.handlers
import typing
import functools
import platform
from xml.etree import ElementTree
import urllib.parse

import pandas as pd
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from utils import logging_conf


def aes_encrypt(key: typing.Union[str, bytes], data: bytes, iv: typing.Union[str, bytes] = b"") -> bytes:
    """AES加密
    """
    assert len(key) == 16

    if isinstance(key, str):
        key = key.encode()
    if isinstance(iv, str):
        iv = iv.encode()

    padder = padding.PKCS7(128).padder()
    data = padder.update(data) + padder.finalize()

    encryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv) if iv else modes.ECB(),
        backend=default_backend()).encryptor()
    return encryptor.update(data) + encryptor.finalize()


def aes_decrypt(key: typing.Union[str, bytes], data: bytes, iv: typing.Union[str, bytes] = b"") -> bytes:
    """AES解密
    """
    assert len(key) == 16

    if isinstance(key, str):
        key = key.encode()
    if isinstance(iv, str):
        iv = iv.encode()

    decryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv) if iv else modes.ECB(),
        backend=default_backend()).decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(decrypted_data) + unpadder.finalize()


def random_string(length: int, choices: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') -> str:
    """随机字符串"""
    return ''.join(random.choice(choices) for _ in range(length))


def ip2int(ip: str) -> int:
    """IP地址转整数"""
    return functools.reduce(lambda a, b: a * 256 + b, map(int, ip.split(".")))


def int2ip(ip_int: int) -> str:
    """整数转IP地址"""
    return "%s.%s.%s.%s" % (
        (ip_int >> 24) & 0xFF,
        (ip_int >> 16) & 0xFF,
        (ip_int >> 8) & 0xFF,
        (ip_int >> 0) & 0xFF,
    )


def is_local_ip(ip: str) -> bool:
    """ip是否是局域网或者本机地址"""
    ip_int = ip2int(ip)
    return \
        ip2int("127.0.0.0") <= ip_int <= ip2int("127.255.255.255") or \
        ip2int("10.0.0.0") <= ip_int <= ip2int("10.255.255.255") or \
        ip2int("172.16.0.0") <= ip_int <= ip2int("172.31.255.255") or \
        ip2int("192.168.0.0") <= ip_int <= ip2int("192.168.255.255")


def crc32(s: typing.Union[str, bytes]):
    """crc32"""
    if isinstance(s, str):
        s = s.encode()
    return binascii.crc32(s)


def md5(s: typing.Union[str, bytes]) -> str:
    """md5
    """
    if isinstance(s, str):
        s = s.encode()
    return hashlib.md5(s).hexdigest()


def hmacSHA256(msg: str, key: str) -> str:
    """计算签名摘要函数"""
    return hmac.new(
        key.encode("utf-8"),
        msg.encode("utf-8"),
        hashlib.sha256
    ).hexdigest().upper()


def base64_decode(s):
    return base64.b64decode(s)


def base64_encode(s):
    return base64.b64encode(s).decode()


def file_bytes(filepath):
    """读取文件二进制内容"""
    with open(filepath, "rb") as f:
        return f.read()


def file_base64(filepath):
    """输出文件二进制内容的base64字符串"""
    return base64_encode(file_bytes(filepath))


def timestamp() -> int:
    """时间戳"""
    return int(time.time())


def current_date() -> datetime.date:
    return (datetime.datetime.now()).date()


def time2str(t=None, fmt="%Y-%m-%d %H:%M:%S"):
    """时间timestamp转字符串
    """
    t = time.time() if t is None else t
    return time.strftime(fmt, time.localtime(t))


def make_dirs(path):
    """创建目录"""
    if not os.path.exists(path):
        os.makedirs(path)


def make_file_dirs(filepath):
    """为文件创建目录"""
    if os.path.split(filepath)[0]:
        make_dirs(os.path.split(filepath)[0])


def gen_uuid() -> str:
    """生成id"""
    return str(uuid.uuid4())


def shorten(d: dict, max_len: int = 256, level=0) -> dict:
    """将字典内过长的字符串/字节缩短"""
    if level <= 0:
        d = copy.deepcopy(d)
    for k, v in d.items():
        if isinstance(v, (str, bytes)) and len(v) > max_len:
            d[k] = v[:max_len]
        elif isinstance(v, dict):
            d[k] = shorten(v, max_len, level + 1)
    return d


def pretty_dumps(d, sort_keys=True, indent=4, ensure_ascii=True):
    """打印字典"""
    return json.dumps(d, sort_keys=sort_keys, indent=indent, ensure_ascii=ensure_ascii)


def is_linux():
    """是否linux系统"""
    return platform.system() in ('Linux', 'Darwin')


# 颜色
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(30, 38)


# 加颜色函数
def colorfy(bold, color, target):
    return "\033[%d;%dm%s\033[0m" % (bold, color, target)


def red(target):
    return colorfy(1, RED, target)


def yellow(target):
    return colorfy(1, YELLOW, target)


def magenta(target):
    return colorfy(1, MAGENTA, target)


def init_logging(log_filename,
                 log_filelevel=logging.DEBUG,
                 log_errorlevel=logging.ERROR,
                 log_streamlevel=logging.DEBUG,
                 daily=True,
                 datefmt='%H:%M:%S'):
    """日志初始化"""
    logging.basicConfig(level=log_streamlevel,
                        format='%(asctime)s.%(msecs)03d %(levelname)s : %(message)s',
                        datefmt=datefmt)
    # 日志文件设置
    if log_filename:
        if os.path.split(log_filename)[0]:
            make_dirs(os.path.split(log_filename)[0])
        if daily:
            file_handler = logging.handlers.TimedRotatingFileHandler(log_filename, when='MIDNIGHT')
        else:
            file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(log_filelevel)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s : %(message)s', datefmt=datefmt)
        )
        logging.getLogger().addHandler(file_handler)

        if log_errorlevel:
            if daily:
                errorfile_handler = logging.handlers.TimedRotatingFileHandler(log_filename + ".ERROR", when='MIDNIGHT')
            else:
                errorfile_handler = logging.FileHandler(log_filename + ".ERROR")
            errorfile_handler.setLevel(log_errorlevel)
            errorfile_handler.setFormatter(
                logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s : %(message)s', datefmt=datefmt)
            )
            logging.getLogger().addHandler(errorfile_handler)


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    """
    do the UNIX double-fork magic, see Stevens' "Advanced
    Programming in the UNIX Environment" for details (ISBN 0201563177)
    http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
    """
    sys.stdout.write("daemonizing...\n")
    if not is_linux():
        return
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)

    # decouple from parent environment
    # os.chdir("/")     # 不需要
    os.setsid()
    # os.umask(0)       # 不需要

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)

    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def xml2dict(xml_text: str) -> dict:
    """xml转字典"""

    # noinspection PyMissingConstructor
    class XmlListConfig(list):
        def __init__(self, aList):
            for element in aList:
                if element:
                    # treat like dict
                    if len(element) == 1 or element[0].tag != element[1].tag:
                        self.append(XmlDictConfig(element))
                    # treat like list
                    elif element[0].tag == element[1].tag:
                        self.append(XmlListConfig(element))
                elif element.text:
                    text = element.text.strip()
                    if text:
                        self.append(text)

    # noinspection PyMissingConstructor
    class XmlDictConfig(dict):
        def __init__(self, parent_element):
            if parent_element.items():
                self.update(dict(parent_element.items()))
            for element in parent_element:
                if element:
                    # treat like dict - we assume that if the first two tags
                    # in a series are different, then they are all different.
                    if len(element) == 1 or element[0].tag != element[1].tag:
                        aDict = XmlDictConfig(element)
                    # treat like list - we assume that if the first two tags
                    # in a series are the same, then the rest are the same.
                    else:
                        # here, we put the list in dictionary; the key is the
                        # tag name the list elements all share in common, and
                        # the value is the list itself
                        aDict = {element[0].tag: XmlListConfig(element)}
                    # if the tag has attributes, add those to the dict
                    if element.items():
                        aDict.update(dict(element.items()))
                    self.update({element.tag: aDict})
                # this assumes that if you've got an attribute in a tag,
                # you won't be having any text. This may or may not be a
                # good idea -- time will tell. It works for the way we are
                # currently doing XML configuration files...
                elif element.items():
                    self.update({element.tag: dict(element.items())})
                # finally, if there are no child tags and no attributes, extract
                # the text
                else:
                    self.update({element.tag: element.text})

    return XmlDictConfig(ElementTree.XML(xml_text))


def url_quote(url: str) -> str:
    """url安全转义"""
    return urllib.parse.quote(url, safe="")


def timeit(func):
    """执行函数打印时间"""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        hash_ = "" # hash(str(args)+str(kwargs))
        print_str = "===start %s %s , kwargs:%s."%(func.__name__,  hash_, kwargs)
        # print_str = "===start %s %s args:%s, kwargs:%s."%(func.__name__,  hash_, args, kwargs)
        logging_conf.important_log(print_str)
        start = time.time()

        ret = func(*args, **kwargs)

        ms = 1000 * (time.time() - start)
        print_str = "===end %s %s %.3fms, kwargs:%s."%(func.__name__, hash_, ms, kwargs)
        # print_str = "===end %s %s %.3fms, args:%s, kwargs:%s."%(func.__name__, hash_, ms, args, kwargs)
        logging_conf.important_log(print_str)

        return ret

    return new_func


def get_df(df=None):
    res = df if df is not None else pd.DataFrame
    return res


def is_empty_df(df=None):
    return df is None or df.empty


if __name__ == "__main__":
    print(pretty_dumps({"hello": "world"}))
    print(md5("helloworld"))
    print(md5(b"helloworld"))
    print(random_string(123))

    appkey = "yarUW6Eq"
    appkey_md5 = md5(appkey)
    aes_key, aes_iv = appkey_md5[:16], appkey_md5[16:]
    encrypted = "60CB76BA488A29553EB1129159C03C7C"
    encrypted_bytes = bytes.fromhex(encrypted)
    decrypted_bytes = aes_decrypt(aes_key, encrypted_bytes, aes_iv)
    print(decrypted_bytes)
    encrypted_bytes2 = aes_encrypt(aes_key, decrypted_bytes, aes_iv)
    print(encrypted_bytes2)
    print(encrypted_bytes2 == encrypted_bytes)

    print(xml2dict("<xml><a>abc</a></xml>"))

    print(url_quote('http://a.b.c/api/wxpay/order_return?order_id=xxxxxxxxxxxxxxx'))
