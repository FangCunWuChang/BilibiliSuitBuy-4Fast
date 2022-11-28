from application.module.decoration import (
    application_error, application_thread
)

from application.apps.windows.login import (
    QrcodeLoginWindow, SmsLoginWindow
)

from application.utils import get_all_value, parse_cookies
from application.net.utils import login_verify

from application.message import askyesno, showwarning, showinfo

import webbrowser
import time


@application_thread
@application_error
def sms_code_login(master) -> None:
    if askyesno("提示", "是否获取新登陆器"):
        webbrowser.open("https://github.com/lllk140/bilibili-login")
    else:
        sms_box = SmsLoginWindow(master)
        while sms_box.login_ok is False and sms_box.winfo_exists():
            time.sleep(0.5)
        if sms_box.login_ok is True:
            sms_box.destroy()
            showinfo("提示", "操作完成")


@application_thread
@application_error
def qr_code_login(master) -> None:
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
        time.sleep(1)
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
