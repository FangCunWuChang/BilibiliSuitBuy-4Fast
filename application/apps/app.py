from application.errors import GuiValueError

from application.config import app_settings

from application.module.controls import (
    TkinterLabel, TkinterButton, TkinterEntry
)

from application.utils import (
    reader
)

from application.net.utils import (
    get_versions, MobiAPP_ANDROID
)

from functools import partial
import tkinter
import os


from application.module.command.serach import (
    item_id_search, coupon_search
)

from application.module.command.info import (
    device_info, from_data_info
)

from application.module.command.open import (
    open_login, open_message
)

from application.module.command.start import (
    start, app_help
)

main_func_list = [
    (item_id_search, "item_id_search"),
    (coupon_search, "coupon_search"),
    (device_info, "device_info"),
    (open_login, "open_login"),
    (from_data_info, "from_data_info"),
    (open_message, "open_message"),
    (start, "start"),
    (app_help, "help")
]


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
        self.geometry("470x210")

        AppFromDataInfo.__init__(self)
        AppDeviceInfo.__init__(self)
        AppLoginInfo.__init__(self)

        # 生成标签
        for label_config in app_settings["label"]:
            TkinterLabel(self, label_config)

        # 生成输入框
        for key, entry_config in app_settings["entry"].items():
            self[key + "_entry"] = TkinterEntry(self, entry_config)

        # 生成按钮
        for func, name in main_func_list:
            TkinterButton(self, app_settings["button"][name], partial(func, self))

        if os.path.exists("./app_device.json"):
            device_config = reader("./app_device.json")
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
