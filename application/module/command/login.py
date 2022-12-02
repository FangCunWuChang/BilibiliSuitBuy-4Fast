from application.module.decoration import (
    application_error, application_thread
)


from application.utils import parse_cookies
from application.net.utils import login_verify

from application.message import askyesno, showwarning, showinfo

import webbrowser


def get_login_device(_) -> None:
    if askyesno("提示", "是否获取新登陆器"):
        webbrowser.open("https://github.com/lllk140/BilibiliLogin")


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
