from application.module.controls import (
    TkinterEntry,
    TkinterLabel,
    TkinterButton,
    TkinterListBox
)

from application.errors import GuiValueError
from application.module.decoration import application_error

from application.net.utils import search_suit, search_coupon
from application.net.login import LoginQrcode, LoginSms

from application.utils import (
    parse_cookies, get_all_value, writer
)

from application.message import (
    showinfo, showwarning
)

from application.config import (
    device_info_label_settings,
    device_info_entry_settings,
    from_data_info_label_settings,
    from_data_info_entry_settings
)

from functools import partial
from PIL import ImageTk
import subprocess
import tkinter
import qrcode
import time
import os


class TopWindow(tkinter.Toplevel):
    def __init__(self, title, geometry):
        super(TopWindow, self).__init__()
        self.title(title)
        self.geometry(geometry)
        self.configure(background="#f0f0f0")
        self.resizable(False, False)

    def __setitem__(self, key: str, value) -> any:
        """ 设置 """
        return setattr(self, str(key), value)

    def __getitem__(self, item: str):
        """ 取得 """
        value = getattr(self, str(item), None)
        if value is None:
            raise GuiValueError(f"不存在{item}")
        return value


class AppWindow(tkinter.Tk):
    def __init__(self):
        """ 主窗口 """
        super(AppWindow, self).__init__()

        self.title("理塘最強伝説と絶兇の猛虎!純真丁一郎です")
        self.configure(background="#f0f0f0")
        self.resizable(False, False)
        self.geometry("800x250")


class ItemsListWindow(TopWindow):
    def __init__(self, master):
        """ 装扮搜索窗口 """
        super(ItemsListWindow, self).__init__("装扮搜索/选择", "500x600")

        self.list_box = TkinterListBox(self, {
            "self": {"font": ("Microsoft YaHei", 14)},
            "place": {"width": 480, "height": 540, "x": 10, "y": 50}
        })

        self.list_box.bind("<Double-Button-1>", partial(self.bind_mod, master))

        self.entry = TkinterEntry(self, {
            "default": None, "self": {"font": ("Microsoft YaHei", 14)},
            "place": {"width": 420, "height": 30, "x": 10, "y": 10}
        })

        TkinterButton(self, {
            "self": {"text": "搜索", "font": ("Microsoft YaHei", 12)},
            "place": {"width": 50, "height": 30, "x": 440, "y": 10}
        }, self.search)

        self.item_id_dict = dict()

    @application_error
    def bind_mod(self, master, _):
        """ 显示到主页面 """
        number = self.list_box.curselection()
        item_id = self.item_id_dict[number[0]]
        master["item_id_entry"].writer(item_id)
        data = master["item_id_entry"].value(False)
        if data == item_id:
            showinfo("提示", "选择成功")
        else:
            showwarning("警告", "选择失败")

    @application_error
    def search(self):
        """ 搜索 """
        self.list_box.delete("0", tkinter.END)
        self.item_id_dict = dict()
        item_id_list = search_suit(self.entry.value("未填写关键字"))
        for number, item in enumerate(item_id_list):
            self.item_id_dict[number] = str(item["item_id"])
            sale = float(item["properties"]["sale_time_begin"])
            sale_time = time.localtime(sale)
            time_text = time.strftime("%Y-%m-%d %H:%M:%S", sale_time)
            self.list_box.insert(tkinter.END, f"[{time_text}]{item['name']}")
        if not item_id_list:
            showinfo("提示", "无搜索结果")


class CouponListWindow(TopWindow):
    def __init__(self, master):
        """ 优惠券显示 """
        super(CouponListWindow, self).__init__("优惠券选择", "600x600")

        self.list_box = TkinterListBox(self, {
            "self": {"font": ("Microsoft YaHei", 12)},
            "place": {"width": 580, "height": 580, "x": 10, "y": 10}
        })

        cookie_value = getattr(master, "Value_cookie", None)
        if cookie_value is None:
            showinfo("提示", "未登录")
            return
        item_id = master["item_id_entry"].value("未填写装扮标识")
        coupon_list = search_coupon(item_id, parse_cookies(cookie_value))
        if not coupon_list:
            showinfo("提示", "未搜索到可用优惠券")

        self.coupon_token_dict = dict()
        for number, coupon in enumerate(coupon_list):
            self.coupon_token_dict[number] = coupon["coupon_token"]
            expire = time.localtime(float(coupon["expire_time"]))
            expire_time_text = time.strftime("%Y-%m-%d %H:%M:%S", expire)
            text = f"{coupon['title']}[{expire_time_text}到期]"
            self.list_box.insert(tkinter.END, text)

        self.list_box.bind("<Double-Button-1>", partial(self.bind_mod, master))

    @application_error
    def bind_mod(self, master, _):
        """ 显示到主页面 """
        number = self.list_box.curselection()
        item_id = self.coupon_token_dict[number[0]]
        master["coupon_entry"].writer(item_id)
        data = master["coupon_entry"].value(False)
        if data == item_id:
            showinfo("提示", "选择成功")
        else:
            showwarning("警告", "选择失败")


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


class StartWindow(tkinter.Toplevel):
    def __init__(self, http_dict: dict, file: str):
        """ 启动选项 """
        super(StartWindow, self).__init__()

        self.title("启动选择")
        self.configure(background="#f0f0f0")
        self.resizable(False, False)
        self.geometry("300x300")

        self.list_box = TkinterListBox(self, {
            "self": {"font": ("Microsoft YaHei", 14)},
            "place": {"width": 280, "height": 280, "x": 10, "y": 10}
        })

        self.http_dict = http_dict
        for http in list(http_dict.keys()):
            self.list_box.insert(tkinter.END, http)

        self.bind("<Double-Button-1>", partial(self.bind_mod, file))

    @application_error
    def bind_mod(self, file, _):
        number = self.list_box.curselection()
        name = self.list_box.get(number)
        kw = {"creationflags": subprocess.CREATE_NEW_CONSOLE}
        http_start_file = os.path.abspath(self.http_dict[name])
        start_text = f"{http_start_file} {file}"
        subprocess.Popen(start_text, **kw)
        showinfo("提示", "已尝试启动")


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
        """ 扫码登陆 """
        super(SmsLoginWindow, self).__init__("短信登陆", "500x500")
