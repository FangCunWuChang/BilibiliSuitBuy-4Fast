import uuid

from application.module.decoration import (
    application_error,
    application_thread
)
from application.module.utils import ButtonCommand
from application.config import help_content
from application.message import showinfo
from application.utils import writer


class DeviceSettingCommandRandom(ButtonCommand):
    """ 设备信息设置---随机buvid """
    def __init__(self, *args, **kwargs):
        super(DeviceSettingCommandRandom, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        random_text = str(uuid.uuid4()).replace("-", "")
        while len(random_text) < 35:
            random_text += str(uuid.uuid4()).replace("-", "")
        fake_buvid = str("XY" + random_text[:35]).upper()
        self.root["BilibiliBuvid_entry"].writer(fake_buvid)


class DeviceSettingCommandApply(ButtonCommand):
    """ 设备信息设置---应用并保存设备信息 """
    def __init__(self, *args, **kwargs):
        super(DeviceSettingCommandApply, self).__init__(*args, **kwargs)
        self.main_app_root = kwargs.get("main_app_root")

    @application_thread
    @application_error
    def func(self):
        device_content = dict({
            "BilibiliBuvid": self.root["BilibiliBuvid_entry"].value(),
            "AndroidModel": self.root["AndroidModel_entry"].value(),
            "AndroidBuild": self.root["AndroidBuild_entry"].value(),
            "VersionName": self.root["VersionName_entry"].value(),
            "VersionCode": self.root["VersionCode_entry"].value(),
        })
        for li in device_content:
            self.main_app_root[f"Device_{li}"] = device_content[li]

        writer("./device.json", device_content)
        showinfo("提示", "操作完成")


class BaseSettingCommandApply(ButtonCommand):
    def __init__(self, *args, **kwargs):
        super(BaseSettingCommandApply, self).__init__(*args, **kwargs)
        self.main_app_root = kwargs.get("main_app_root")

    @application_thread
    @application_error
    def func(self):
        add_month = self.root["addMonth_entry"].value()
        f_source = self.root["fSource_entry"].value()
        shop_from = self.root["shopFrom_entry"].value()

        self.main_app_root["Base_addMonth"] = add_month
        self.main_app_root["Base_fSource"] = f_source
        self.main_app_root["Base_shopFrom"] = shop_from
