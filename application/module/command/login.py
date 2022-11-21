from application.module.decoration import (
    application_error, application_thread
)

from application.utils import get_all_value, parse_cookies, urlQuerySplit
from application.net.utils import login_verify

from application.apps.windows.login import QrcodeLoginWindow

from application.message import askyesno, showwarning, showinfo

from application.net.login import LoginSms

from web.geetest_validator.geetest import GeeTest

import time


@application_thread
@application_error
def code_login(master) -> None:
    value = get_all_value(master, "Value_", [], True)
    if all([v for _, v in value.items()]):
        if askyesno("确认", "已存在登录数据是否继续") is False:
            return

    ver_data = get_all_value(master, "Data_", ["versionName", "versionCode"], True)
    versions = tuple((ver_data["versionCode"], ver_data["versionName"]))
    devices_data = get_all_value(master, "Device_", [])
    model_build = (devices_data["AndroidModel"], devices_data["AndroidBuild"])

    login = LoginSms(versions, *model_build, devices_data["Buvid"])

    tel_number = input("手机号:")

    res_data = login.SendSmsCode(tel_number)

    if not res_data["captcha_key"]:
        query_dict = urlQuerySplit(res_data["recaptcha_url"])
        args = (query_dict["gee_gt"], query_dict["gee_challenge"])
        gee_test_window = GeeTest(*args)
        gee_verify_dict = gee_test_window.waitFinishing()
        gee_form_data = {
            "gee_challenge": gee_verify_dict["geetest_challenge"],
            "gee_seccode": gee_verify_dict["geetest_seccode"],
            "gee_validate": gee_verify_dict["geetest_validate"]
        }
        res_data = login.SendSmsCode(tel_number, **gee_form_data)

    captcha_key = res_data["captcha_key"]
    verify_code = input("发送成功, 输入验证码:")
    res = login.Login(captcha_key, tel_number, verify_code)
    access_key, cookie_text = login.Extract(res)
    master["Value_cookie"] = cookie_text
    master["Value_accessKey"] = access_key
    showinfo("提示", "操作完成")


@application_thread
@application_error
def _code_login_1(master) -> None:
    showwarning("警告", "扫码登录已弃用, 短信登录在找人给我抓包(, 还在测试, 我还是没自己抓到足够的样本来分析")
    showinfo("提示", "注意控制台, 手机号还有验证码在控制台输入")
    # login = LoginSms(("7060200", "7.6.0"), "SM-G955N", "9", master.Device_Buvid)
    login = LoginSms(("7060200", "7.6.0"), "OPPO A77t", "7", "XUBB9EEBCE80B0696BFADF677D89092CF6A68")
    tel_number = input("输入手机号:")
    captcha_key = login.SendSmsCode(tel_number)
    if not captcha_key:
        showwarning("警告", "发送失败, 应该是卡验证码了")
        return
    verify_code = input("发送成功, 输入验证码:")
    res = login.Login(captcha_key, tel_number, verify_code)
    access_key, cookie_text = login.Extract(res)
    master["Value_cookie"] = cookie_text
    master["Value_accessKey"] = access_key
    showinfo("提示", "操作完成")


@application_thread
@application_error
def __code_login(master) -> None:
    value = get_all_value(master, "Value_", [], True)
    if all([v for _, v in value.items()]):
        if askyesno("确认", "已存在登录数据是否继续") is False:
            return
    login_box = QrcodeLoginWindow(master)
    while master.winfo_exists() and login_box.winfo_exists():
        code, data = login_box.login.Verify(login_box.auth_code)
        if code == 0:
            access_key, cookie_text = login_box.login.Extract(data)
            master["Value_cookie"] = cookie_text
            master["Value_accessKey"] = access_key
            break
        if code == 86038:
            raise Exception("二维码已失效")
        time.sleep(3)
    login_box.destroy()


@application_thread
@application_error
def verify_login(master) -> None:
    cookie = getattr(master, "Value_cookie", None)
    access_key = getattr(master, "Value_accessKey", None)
    if not all([cookie, access_key]):
        showwarning("警告", "登陆信息为空")
        return
    mid = login_verify(parse_cookies(cookie), access_key)
    if mid is False:
        showwarning("警告", "验证失败")
    else:
        showinfo("提示", f"验证成功[UID:{mid}]")
