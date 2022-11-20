from application.apps.windows.app import TopWindow

from application.module.decoration import application_error

from application.module.controls import (
    TkinterLabel, TkinterButton, TkinterEntry
)

from application.utils import (
    writer, get_all_value
)

from application.config import (
    device_info_label_settings,
    device_info_entry_settings,
    from_data_info_entry_settings,
    from_data_info_label_settings
)

from application.message import showinfo

from functools import partial


class DeviceInfoWindow(TopWindow):
    def __init__(self, master):
        """ 设备信息 """
        super(DeviceInfoWindow, self).__init__("设备信息设置", "530x170")

        # 生成标签
        for label_config in device_info_label_settings:
            TkinterLabel(self, label_config)
        # 生成输入框
        for key, entry_config in device_info_entry_settings.items():
            self[key + "_entry"] = TkinterEntry(self, entry_config)

        TkinterButton(self, {
            "self": {"text": "保存/应用", "font": ("Microsoft YaHei", 14)},
            "place": {"width": "510", "height": 30, "x": 10, "y": 130}
        }, partial(self.save_button, master))

        device_config = get_all_value(master, "Device_", [], True)
        if all([v for _, v in device_config.items()]):
            self["buvid_entry"].writer(device_config["Buvid"])
            self["android_model_entry"].writer(device_config["AndroidModel"])
            self["android_build_entry"].writer(device_config["AndroidBuild"])

    @application_error
    def save_button(self, master):
        value_dict = get_all_value(self, "_entry", [])
        writer("./device_info/device.json", value_dict)
        master["Device_Buvid"] = value_dict["buvid"]
        master["Device_AndroidModel"] = value_dict["android_model"]
        master["Device_AndroidBuild"] = value_dict["android_build"]
        showinfo("提示", "操作完成")


class FromDataWindow(TopWindow):
    def __init__(self, master):
        """ 表单信息 """
        super(FromDataWindow, self).__init__("基础信息设置", "280x250")

        # 生成标签
        for label_config in from_data_info_label_settings:
            TkinterLabel(self, label_config)
        # 生成输入框
        for key, entry_config in from_data_info_entry_settings.items():
            self[key + "_entry"] = TkinterEntry(self, entry_config)

        TkinterButton(self, {
            "self": {"text": "应用", "font": ("Microsoft YaHei", 14)},
            "place": {"width": "260", "height": 30, "x": 10, "y": 210}
        }, partial(self.save_button, master))

        data_config = get_all_value(master, "Data_", [], True)

        for key, value in data_config.items():
            self[f"{key}_entry"].writer(value)

    @application_error
    def save_button(self, master):
        value_dict = get_all_value(self, "_entry", [""])
        for key, value in value_dict.items():
            master[f"Data_{key}"] = value
