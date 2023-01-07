from urllib.parse import urlencode
import hashlib


from application.errors import (
    GuiDeviceValueNotExist,
    GuiBaseValueNotExist,
    GuiLoginValueNotExist
)
from application.items import (
    TkinterButton,
    ButtonConfig
)


class FormData(dict):
    """ 表单 """
    def __init__(self, *args, **kwargs):
        super(FormData, self).__init__(*args, **kwargs)

    @property
    def sorted(self):
        """ 排序 """
        return {k: self[k] for k in sorted(self)}

    def toSign(self, app: tuple[str, str]):
        """ 计算sign """
        appkey, appsec = app
        self.update({"appkey": appkey})
        form_data = self.sorted
        text = urlencode(form_data) + appsec
        hashlib_md5 = hashlib.md5()
        hashlib_md5.update(text.encode())
        sign = hashlib_md5.hexdigest()
        form_data.update({"sign": sign})
        return form_data


class ButtonCommand(object):
    """ 按钮绑定事件 """
    def __init__(self, root, config: ButtonConfig, **kwargs):
        super(ButtonCommand, self).__init__()

        self.root = root
        TkinterButton(self.root, config, func=self.func)

    def func(self):
        """ 事件 """
        ...


def get_all_device_value(root, error: bool = True) -> dict:
    """ 获取设备信息 """
    device_values = dict({
        "BilibiliBuvid": root["Device_BilibiliBuvid"],
        "AndroidModel": root["Device_AndroidModel"],
        "AndroidBuild": root["Device_AndroidBuild"],
        "VersionName": root["Device_VersionName"],
        "VersionCode": root["Device_VersionCode"]
    })
    if not all(device_values.values()) and error:
        raise GuiDeviceValueNotExist("设备信息未填写/全")
    return device_values


def get_all_base_value(root, error: bool = True) -> dict:
    """ 获取基础信息 """
    base_values = dict({
        "addMonth": root["Base_addMonth"],
        "fSource": root["Base_fSource"],
        "shopFrom": root["Base_shopFrom"],
    })
    if not all(base_values.values()) and error:
        raise GuiBaseValueNotExist("基本信息未填写/全")
    return base_values


def get_all_login_value(root, error: bool = True) -> dict:
    """ 获取登陆信息 """
    login_values = dict({
        "accessKey": root["Login_accessKey"],
        "cookie": root["Login_cookie"]
    })
    if not all(login_values.values()) and error:
        raise GuiLoginValueNotExist("基本信息未填写/全")
    return login_values
