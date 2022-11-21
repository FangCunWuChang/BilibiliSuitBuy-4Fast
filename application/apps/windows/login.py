from application.apps.windows.app import TopWindow

from application.utils import get_all_value, urlQuerySplit
from application.net.login import LoginQrcode, LoginSms

from application.module.controls import (
    TkinterEntry, TkinterButton, TkinterLabel
)

from application.message import showinfo

from application.errors import ResponseError
from application.module.decoration import (
    application_error, application_thread
)

from web.geetest_validator.geetest import GeeTest

from application.config import login_config_sms

from functools import partial
from PIL import ImageTk
import tkinter
import qrcode


class QrcodeLoginWindow(TopWindow):
    def __init__(self, master):
        """ 扫码登陆 """
        super(QrcodeLoginWindow, self).__init__("扫码登陆", "370x370")

        device_dict = get_all_value(master, "Device_", [])
        device_dict = {k.lower(): v for k, v in device_dict.items()}
        self.login = LoginQrcode(**device_dict)

        login_url, self.auth_code = self.login.GetUrlAndAuthCode()
        image = qrcode.make(login_url).get_image()
        self._photo = ImageTk.PhotoImage(image)
        tkinter.Label(self, image=self._photo).pack()


class SmsLoginWindow(TopWindow):
    def __init__(self, master):
        """ 短信登陆 """
        super(SmsLoginWindow, self).__init__("短信登陆", "300x130")

        ver_data = get_all_value(master, "Data_", ["versionName", "versionCode"], True)
        versions = tuple((ver_data["versionCode"], ver_data["versionName"]))
        devices_data = get_all_value(master, "Device_", [])
        model_build = (devices_data["AndroidModel"], devices_data["AndroidBuild"])

        for label_config in [
            {
                "self": {"text": "手机号", "font": ["Microsoft YaHei", 18]},
                "place": {"width": 75, "height": 30, "x": 10, "y": 10}
            },
            {
                "self": {"text": "验证码", "font": ["Microsoft YaHei", 18]},
                "place": {"width": 75, "height": 30, "x": 10, "y": 50}
            },
            {
                "self": {"text": "地区号", "font": ["Microsoft YaHei", 18]},
                "place": {"width": 75, "height": 30, "x": 10, "y": 90}
            }
        ]:
            TkinterLabel(self, label_config)

        self.tel_number_entry = TkinterEntry(self, {
            "default": None, "self": {"font": ["Microsoft YaHei", 16]},
            "place": {"width": 185, "height": 30, "x": 100, "y": 10}
        })

        self.verify_code_entry = TkinterEntry(self, {
            "default": None, "self": {"font": ["Microsoft YaHei", 16]},
            "place": {"width": 105, "height": 30, "x": 100, "y": 50}
        })

        self.cid_entry = TkinterEntry(self, {
            "default": str(login_config_sms["cid"]),
            "self": {"font": ["Microsoft YaHei", 16]},
            "place": {"width": 50, "height": 30, "x": 100, "y": 90}
        })

        TkinterButton(self, {
            "self": {"text": "发送", "font": ["Microsoft YaHei", 16]},
            "place": {"width": 65, "height": 30, "x": 220, "y": 50}
        }, self.send_verify_code)

        TkinterButton(self, {
            "self": {"text": "登陆", "font": ["Microsoft YaHei", 16]},
            "place": {"width": 125, "height": 30, "x": 160, "y": 90}
        },  partial(self.login_login, master))

        self.login = LoginSms(versions, *model_build, devices_data["Buvid"])

        self.captcha_key = None
        self.login_ok = False

    @application_thread
    @application_error
    def send_verify_code(self) -> None:
        tel_number = self.tel_number_entry.value("未输入手机号")
        cid = self.cid_entry.value("未输入区号")
        res_data = self.login.SendSmsCode(tel_number, cid)
        if res_data["code"] != 0:
            raise ResponseError(res_data["message"])
        if not res_data["data"]["captcha_key"]:
            query_dict = urlQuerySplit(res_data["data"]["recaptcha_url"])
            args = (query_dict["gee_gt"], query_dict["gee_challenge"])
            gee_test_window = GeeTest(*args)
            gee_verify_dict = gee_test_window.waitFinishing()
            gee_form_data = {
                "gee_challenge": gee_verify_dict["geetest_challenge"],
                "gee_seccode": gee_verify_dict["geetest_seccode"],
                "gee_validate": gee_verify_dict["geetest_validate"],
                "recaptcha_token": query_dict["recaptcha_token"],
            }
            res_data = self.login.SendSmsCode(tel_number, cid, **gee_form_data)
        showinfo("提示", "验证码已发送")
        self.captcha_key = res_data["data"]["captcha_key"]

    @application_thread
    @application_error
    def login_login(self, master) -> None:
        tel_number = self.tel_number_entry.value("未输入手机号")
        cid = self.cid_entry.value("未输入区号")
        code = self.verify_code_entry.value("未输入验证码")
        res = self.login.Login(self.captcha_key, tel_number, cid, code)
        if res["code"] != 0:
            raise ResponseError(res["message"])
        access_key, cookie_text = self.login.Extract(res)
        master["Value_cookie"] = cookie_text
        master["Value_accessKey"] = access_key
        self.login_ok = True
