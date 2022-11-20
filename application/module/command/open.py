from application.module.decoration import (
    application_error, application_thread
)

from application.utils import reader, parse_cookies, ReaderMode_Content

from application.message import askopenfilename, showinfo

from urllib.parse import urlsplit
from urllib.parse import unquote
import re


@application_thread
@application_error
def open_login(master) -> None:
    file_path = askopenfilename("导入登录标识", [("json", "*.json")], "login_qr.json")
    login_content = reader(file_path)
    master["Value_cookie"] = login_content["cookie"]
    master["Value_accessKey"] = login_content["accessKey"]


@application_thread
@application_error
def open_message(master) -> None:
    file_path = askopenfilename("导入报文", [("text", "*.txt")], "message.txt")
    content = reader(file_path, ReaderMode_Content)
    message_content: list = content.split(b"\r\n")
    request: list = message_content[0].split(b" ")
    url_query: bytes = urlsplit(request[1]).query
    p = [i.split(b"=") for i in url_query.split(b"&")]
    p2 = [[ii.decode() for ii in i] for i in p]
    params = {unquote(i[0]): unquote(i[1]) for i in p2}
    headers_content = message_content[1:len(message_content) - 2]
    h = [i.split(b": ") for i in headers_content]
    h2h = [i if len(i) == 2 else [i[0], b""] for i in h]
    h3 = [[ii.decode() for ii in i] for i in h2h]
    headers = {unquote(i[0]).lower(): i[1] for i in h3}
    user_agent = headers["user-agent"]

    android_model_list = re.findall(r"model/.+? ", user_agent)
    android_model = android_model_list[0][6:][:-1]
    android_build_list = re.findall(r"osVer/.+? ", user_agent)
    android_build = android_build_list[0][6:][:-1]
    app_code_list = re.findall(r"build/.+? ", user_agent)
    version_code = app_code_list[0][6:][:-1]
    app_name_list = re.findall(r"disable_rcmd/0 .+? ", user_agent)
    version_name = app_name_list[0].split(" ")[1]
    cookies = parse_cookies(headers["cookie"])

    master["Device_Buvid"] = cookies["Buvid"]
    master["Device_AndroidModel"] = android_model
    master["Device_AndroidBuild"] = android_build
    master["Data_versionCode"] = version_code
    master["Data_versionName"] = version_name
    master["Value_cookie"] = headers["cookie"]
    master["Value_accessKey"] = params["access_key"]
    master["item_id_entry"].writer(params["item_id"])


@application_thread
@application_error
def open_setting(master) -> None:
    file_path = askopenfilename("导入配置", [("json", "*.json")], "setting.json")
    setting_content = reader(file_path)

    for key, value in setting_content["entry"].items():
        master[f"{key}_entry"].writer(str(value))

    for key, value in setting_content["device"].items():
        master[f"Device_{key}"] = str(value)

    for key, value in setting_content["value"].items():
        master[f"Value_{key}"] = str(value)

    for key, value in setting_content["data"].items():
        master[f"Data_{key}"] = str(value)

    showinfo("提示", "操作完成")
