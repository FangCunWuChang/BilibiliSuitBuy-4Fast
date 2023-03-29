import time
import tkinter

from application.apps.utils import TopWindow
from application.items import (
    AppConfig,
)
from application.message import (
    showinfo,
    showwarning
)
from application.config import (
    config_controls_ItemsSearch_listbox,
    config_controls_CouponSearch_listbox
)
from application.net.utils import get_sale_time

class DeviceSettingWindow(TopWindow):
    """ 设备信息窗口 """
    def __init__(self, config: AppConfig):
        super(DeviceSettingWindow, self).__init__(config)


class BaseSettingWindow(TopWindow):
    """ 基础信息窗口 """
    def __init__(self, config: AppConfig):
        super(BaseSettingWindow, self).__init__(config)

class ItemsSearchWindow(TopWindow):
    """ 装扮搜索窗口 """
    def __init__(self, main_app_root, config: AppConfig):
        super(ItemsSearchWindow, self).__init__(config)

        self.item_id_dict = dict()

        self.main_app_root = main_app_root

        self.loadListBox("list_box", config_controls_ItemsSearch_listbox)
        self['list_box'].bind("<Double-Button-1>", self.func)

    def func(self, _):
        number = self["list_box"].curselection()
        item_id = self.item_id_dict[number[0]]

        try:
            sale_time = get_sale_time(item_id)
        except Exception as err:
            showwarning("警告", "获取开售时间失败")
        else:
            self.main_app_root["ItemId_entry"].writer(item_id)
            data = self.main_app_root["ItemId_entry"].value()

            self.main_app_root["StartT_entry"].writer(str(sale_time))
            self.main_app_root["DelayT_entry"].writer(str(0))

            self.main_app_root["SaleT_entry"].config(state = 'normal')
            self.main_app_root["SaleT_entry"].writer(str(sale_time))
            self.main_app_root["SaleT_entry"].config(state = 'readonly')

            if data == item_id:
                showinfo("提示", "选择成功")
            else:
                showwarning("警告", "选择失败")


class CouponSearchWindow(TopWindow):
    """ 优惠券选择窗口 """
    def __init__(self, main_app_root, coupon_list: list, config: AppConfig):
        super(CouponSearchWindow, self).__init__(config)

        self.main_app_root = main_app_root
        self.coupon_token_dict = dict()

        self.loadListBox("list_box", config_controls_CouponSearch_listbox)
        for number, coupon in enumerate(coupon_list):
            self.coupon_token_dict[number] = coupon["coupon_token"]
            expire = time.localtime(float(coupon["expire_time"]))
            expire_time_text = time.strftime("%Y-%m-%d %H:%M:%S", expire)
            text = f"{coupon['title']}[{expire_time_text}到期]"
            self["list_box"].insert(tkinter.END, text)
        self["list_box"].bind("<Double-Button-1>", self.func)

    def func(self, _):
        number = self["list_box"].curselection()
        item_id = self.coupon_token_dict[number[0]]
        self.main_app_root["Coupon_entry"].writer(item_id)
        data = self.main_app_root["Coupon_entry"].value()
        if data == item_id:
            showinfo("提示", "选择成功")
        else:
            showwarning("警告", "选择失败")
