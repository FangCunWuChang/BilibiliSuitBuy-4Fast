from application.errors import (
    ReaderError,
    GuiValueIndexWarning,
    SdkIntIndexError
)

from Crypto.Util.Padding import unpad, pad
from Crypto.Cipher import AES
import hashlib
import base64
import json
import uuid
import os

ReaderMode_Setting = "setting"
ReaderMode_Content = "content"

WriterMode_Setting = "setting"
WriterMode_Content = "content"

SIGN_TV: str = "59b43e04ad6965f34319062b478f83dd"
SIGN_ANDROID: str = "560c52ccd288fed045859ed18bffd973"
SIGN_ANDROID_LOGIN: str = "2653583c8873dea268ab9386918b1d65"


def reader(path: str, mode=ReaderMode_Setting, **kwargs) -> list | dict | bytes:
    """ 读取文件 """
    if not os.path.exists(path):
        ReaderError(f"无法打开{path}")
    with open(os.path.abspath(path), "rb") as file:
        file_data = file.read()
    file.close()
    if kwargs.get("crypto", False) is not False:
        key: str = kwargs.get("key", str())
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        file_data_de = cipher.decrypt(file_data)
        file_data = unpad(file_data_de, AES.block_size)
    if mode == ReaderMode_Setting:
        return json.loads(file_data.decode())
    if mode == ReaderMode_Content:
        return file_data


def writer(path: str, data: list | dict | bytes, **kwargs) -> str:
    """ 写入 """
    file_path, file = os.path.split(path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    write_data = data
    if isinstance(data, list) or isinstance(data, dict):
        write_data = json.dumps(data).encode()
    if kwargs.get("crypto", False) is not False:
        key: str = kwargs.get("key", str())
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        write_data = pad(write_data, AES.block_size)
        write_data = cipher.encrypt(write_data)
    with open(path, "wb") as w_file:
        w_file.write(write_data)
    w_file.close()
    return os.path.abspath(path)


def buildSign(form_data: str, app_sec=SIGN_ANDROID) -> str:
    """ 生成表单的sign """
    form_data_sec = f"{form_data}{app_sec}"
    md5_hashlib = hashlib.md5()
    md5_hashlib.update(form_data_sec.encode())
    return str(md5_hashlib.hexdigest())


def build_x_bili_aurora_eid(mid: str) -> str:
    """ 生成 x-bili-aurora-eid """
    length = mid.__len__()
    barr = bytearray(length)
    if length - 1 < 0:
        return ""
    for i in range(length):
        s = ord("ad1va46a7lza"[i % 12])
        barr[i] = ord(mid[i]) ^ s
    return base64.b64encode(barr).decode()


def build_x_bili_trace_id(sela_time: int) -> str:
    """ 生成 x-bili-trace-id """
    back6 = hex(round(sela_time / 256))
    front = str(uuid.uuid4()).replace("-", "")
    _data1 = front[6:] + back6[2:]
    _data2 = front[22:] + back6[2:]
    return f"{_data1}:{_data2}:0:0"


def parse_cookies(cookies_content: str) -> dict:
    """  把字符串格式的cookie转为dict格式 """
    c1: list = cookies_content.split("; ")
    c2 = [i.split("=") for i in c1]
    return {i[0]: i[1] for i in c2}


def get_all_value(master, wkey: str, no_items: list, reverse=False) -> dict:
    """
    获取所有内容
    no_items 不抛出异常的值
    reverse 反向选择 不抛出异常的值
    """
    entry_dict, return_dict = dict(), dict()
    for key, value in master.__dict__.items():
        if wkey in key:
            entry_dict[key.replace(wkey, "")] = value
    if reverse:
        reverse_no_items = list(entry_dict.keys())
        for li in no_items:
            reverse_no_items.remove(li)
        no_items = reverse_no_items
    for key, entry in entry_dict.items():
        err = False if key in no_items else f"{key}未填写"
        if "_entry" in wkey:
            return_dict[key] = entry.value(err)
        else:
            if entry is None and err:
                raise GuiValueIndexWarning(err)
            return_dict[key] = entry
    return return_dict


def get_sdk_int(build: str, sdk_int_file_path: str = None) -> str:
    """ 以系统版本获取sdk """
    if sdk_int_file_path:
        data = reader(sdk_int_file_path)
    else:
        data = reader("./settings/content/sdk_int.json")
    build_list = build.split(".")
    sdk_int = None
    for li in build_list:
        if li not in data:
            if sdk_int is not None:
                return str(sdk_int)
            raise SdkIntIndexError(f"未找到{build}的sdk_int")
        sdk_int = data[li]["value"]
        data = data[li]
    return str(sdk_int)
