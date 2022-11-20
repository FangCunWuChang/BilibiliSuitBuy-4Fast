from application.apps.windows.app import TopWindow

from application.module.controls import (
    TkinterEntry, TkinterButton, TkinterListBox
)

from application.module.decoration import application_error
from application.message import showinfo, showwarning

from application.net.utils import search_suit, search_coupon
from application.utils import parse_cookies

from functools import partial
import tkinter
import time


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
