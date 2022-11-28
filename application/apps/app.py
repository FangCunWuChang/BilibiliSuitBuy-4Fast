from application.errors import GuiValueError

from application.config import (
    button_settings, label_settings, entry_settings
)

from application.module.controls import (
    TkinterLabel, TkinterButton, TkinterEntry
)

from application.utils import (
    reader
)

from application.net.utils import (
    get_versions, MobiAPP_ANDROID
)

from application.module.com import func_list

from functools import partial
import tkinter
import os


class AppDeviceInfo(object):
    def __init__(self):
        """ 设备信息 """
        super(AppDeviceInfo, self).__init__()
        self.Device_Buvid = None
        self.Device_AndroidModel = None
        self.Device_AndroidBuild = None


class AppLoginInfo(object):
    def __init__(self):
        """ 报文里的一些默认值 """
        super(AppLoginInfo, self).__init__()
        self.Value_cookie = None
        self.Value_accessKey = None


class AppFromDataInfo(object):
    def __init__(self):
        """ 报文里的一些默认值 """
        super(AppFromDataInfo, self).__init__()
        self.Data_addMonth: str = "-1"
        self.Data_fSource: str = "shop"
        self.Data_shopFrom: str = "feed.card"

        code, name = get_versions(MobiAPP_ANDROID)

        self.Data_versionName: str = str(name)
        self.Data_versionCode: str = str(code)


class App(tkinter.Tk, AppDeviceInfo, AppFromDataInfo, AppLoginInfo):
    def __init__(self):
        super(App, self).__init__()

        self.title("理塘最強伝説と絶兇の猛虎!純真丁一郎です")
        self.configure(background="#f0f0f0")
        self.resizable(False, False)
        self.geometry("800x250")

        AppFromDataInfo.__init__(self)
        AppDeviceInfo.__init__(self)
        AppLoginInfo.__init__(self)

        # 生成标签
        for label_config in label_settings:
            TkinterLabel(self, label_config)

        # 生成输入框
        for key, entry_config in entry_settings.items():
            self[key + "_entry"] = TkinterEntry(self, entry_config)

        # 生成按钮
        for func, name in func_list:
            TkinterButton(self, button_settings[name], partial(func, self))

        if os.path.exists("./device_info/device.json"):
            device_config = reader("./device_info/device.json")
            self.Device_Buvid = device_config["buvid"]
            self.Device_AndroidModel = device_config["android_model"]
            self.Device_AndroidBuild = device_config["android_build"]

    def __setitem__(self, key: str, value) -> any:
        """ 设置 """
        return setattr(self, str(key), value)

    def __getitem__(self, item: str):
        """ 取得 """
        value = getattr(self, str(item), None)
        if value is None:
            raise GuiValueError(f"不存在{item}")
        return value
