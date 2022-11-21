from urllib.parse import urlencode
import time

from application.utils import buildSign, SIGN_TV, SIGN_ANDROID_LOGIN

from application.net.session import Session
from application.net.utils import get_versions, MobiAPP_TV

from application.config import user_agent_format, login_config_qr, login_config_sms


class LoginSms(Session):
    def __init__(self, version: tuple, androidmodel: str, androidbuild: str, buvid: str):
        super(LoginSms, self).__init__()
        (self.code, self.name), self.buvid = version, buvid

        user_agent = user_agent_format["android_login"].format(
            VERSION_NAME=self.name, ANDROID_MODEL=androidmodel,
            VERSION_CODE=self.code, CHANNEL=login_config_sms["channel"],
            ANDROID_BUILD=androidbuild
        )

        self.headers.update(login_config_sms["headers"])
        self.headers.update({"User-Agent": user_agent})
        self.headers.update({"Buvid": str(self.buvid)})

        self.login_host = login_config_sms["host"]
        self.app_key = login_config_sms["appkey"]
        self.cid = login_config_sms["cid"]

    def SendSmsCode(self, tel_number: str, **kwargs):
        data = {"appkey": self.app_key, "cid": self.cid}
        data.update(kwargs if kwargs else dict())
        data.update({"tel": tel_number})
        data.update({"ts": str(round(time.time()))})
        form_data_text = urlencode(data)
        sign = buildSign(form_data_text, SIGN_ANDROID_LOGIN)
        form_data = form_data_text + f"&sign={sign}"
        # print(form_data)
        url = f"https://{self.login_host}/x/passport-login/sms/send"
        response = self.request("POST", url, **{"data": form_data})
        # print(response.text)
        return response.json()

    def Login(self, captcha_key: str, tel_number: str, code: str):
        data = {"appkey": self.app_key, "captcha_key": captcha_key, "cid": self.cid}
        data.update({"code": code, "tel": tel_number, "ts": str(round(time.time()))})
        form_data_text = urlencode(data)
        sign = buildSign(form_data_text, SIGN_ANDROID_LOGIN)
        form_data = form_data_text + f"&sign={sign}"
        url = f"https://{self.login_host}/x/passport-login/login/sms"
        response = self.request("POST", url, **{"data": form_data})
        # print(response.text)
        return response.json()

    def Extract(self, response_json: dict) -> tuple[str, str]:
        access_key = str(response_json["data"]["token_info"]["access_token"])
        cookie_list = response_json["data"]["cookie_info"]["cookies"]
        cookie_dict = {li["name"]: li["value"] for li in cookie_list}
        cookie_dict.update({"Buvid": str(self.buvid)})
        cookie_list = [f"{k}={v}" for k, v in cookie_dict.items()]
        return access_key, "; ".join(cookie_list)


class LoginQrcode(Session):
    def __init__(self, androidmodel: str, androidbuild: str, buvid: str):
        super(LoginQrcode, self).__init__()

        if login_config_qr["version"] == "auto":
            self.build, version = get_versions(MobiAPP_TV)
        else:
            self.build, version = tuple(login_config_qr["version"])

        user_agent = user_agent_format["tv"].format(
            TV_CODE=self.build, CHANNEL=login_config_qr["channel"],
            TV_NAME=version, ANDROID_MODEL=androidmodel,
            ANDROID_BUILD=androidbuild
        )

        self.short_url = login_config_qr["short_url"]
        self.login_host = login_config_qr["host"]
        self.app_key = login_config_qr["appkey"]
        self.buvid = buvid

        self.headers.update(login_config_qr["headers"])
        self.headers.update({"User-Agent": user_agent})
        self.headers.update({"Buvid": str(self.buvid)})

    def GetUrlAndAuthCode(self) -> tuple[str, str]:
        """ 获取登录链接加标识 """
        form_data = {
            "appkey": self.app_key,
            "local_id": str(self.buvid),
            "ts": str(round(time.time()))
        }
        if self.short_url:
            form_data.update({"build": self.build})
        sorted_key = sorted(form_data)
        form_data = {i: form_data[i] for i in sorted_key}
        form_data_text = urlencode(form_data)
        sign = buildSign(form_data_text, SIGN_TV)
        form_data = form_data_text + f"&sign={sign}"
        self.headers.update({"Content-Length": str(len(form_data))})
        url = f"https://{self.login_host}/x/passport-tv-login/qrcode/auth_code"
        response = self.request("POST", url, **{"data": form_data})
        auth_code = response.json()["data"]["auth_code"]
        login_url = response.json()["data"]["url"]
        return str(login_url), str(auth_code)

    def Verify(self, auth_code: str) -> tuple[dict, int]:
        form_data = urlencode({
            "appkey": self.app_key,
            "auth_code": str(auth_code),
            "local_id": str(self.buvid),
            "ts": str(round(time.time()))
        })
        form_data_sign = buildSign(form_data, SIGN_TV)
        form_data = form_data + f"&sign={form_data_sign}"
        self.headers.update({"Content-Length": str(len(form_data))})
        url = f"https://{self.login_host}/x/passport-tv-login/qrcode/poll"
        response = self.request("POST", url, **{"data": form_data})
        return response.json()["code"], response.json()

    def Extract(self, response_json: dict) -> tuple[str, str]:
        """ 提取cookie, access_key """
        access_key = str(response_json["data"]["access_token"])
        cookie_list = response_json["data"]["cookie_info"]["cookies"]
        cookie_dict = {li["name"]: li["value"] for li in cookie_list}
        cookie_dict.update({"Buvid": str(self.buvid)})
        cookie_list = [f"{k}={v}" for k, v in cookie_dict.items()]
        return access_key, "; ".join(cookie_list)
