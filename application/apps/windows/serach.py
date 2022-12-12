from application.apps.windows.app import TopWindow

from application.module.controls import (
    TkinterEntry, TkinterButton, TkinterListBox
)

from application.config import (
    search1_settings, search2_settings
)

from application.module.decoration import application_error
from application.message import showinfo, showwarning

from application.net.utils import search_suit

from functools import partial
import tkinter
import time


@application_error
def search1_bind(top, master, _):
    number = top.list_box.curselection()
    item_id = top.item_id_dict[number[0]]
    master["item_id_entry"].writer(item_id)
    data = master["item_id_entry"].value(False)
    if data == item_id:
        showinfo("提示", "选择成功")
    else:
        showwarning("警告", "选择失败")


@application_error
def search2_bind(top, master, _):
    number = top.list_box.curselection()
    item_id = top.coupon_token_dict[number[0]]
    master["coupon_entry"].writer(item_id)
    data = master["coupon_entry"].value(False)
    if data == item_id:
        showinfo("提示", "选择成功")
    else:
        showwarning("警告", "选择失败")


@application_error
def search1(master):
    """ 搜索 """
    master.list_box.delete("0", tkinter.END)
    master.item_id_dict = dict()
    item_id_list = search_suit(master.entry.value("未填写关键字"))
    for number, item in enumerate(item_id_list):
        master.item_id_dict[number] = str(item["item_id"])
        sale = float(item["properties"]["sale_time_begin"])
        sale_time = time.localtime(sale)
        time_text = time.strftime("%Y-%m-%d %H:%M:%S", sale_time)
        master.list_box.insert(tkinter.END, f"[{time_text}]{item['name']}")
    if not item_id_list:
        showinfo("提示", "无搜索结果")


search1_bind_func_list = [
    (search1_bind, "list_box")
]

search2_bind_func_list = [
    (search2_bind, "list_box")
]

search1_func_list = [
    (search1, "search")
]


class ItemsListWindow(TopWindow):
    def __init__(self, master):
        """ 装扮搜索窗口 """
        super(ItemsListWindow, self).__init__("装扮搜索/选择", "500x600")

        for key, entry_config in search1_settings["entry"].items():
            self[key] = TkinterEntry(self, entry_config)

        for func, name in search1_bind_func_list:
            self[name] = TkinterListBox(self, search1_settings["list"][name])
            self[name].bind("<Double-Button-1>", partial(func, self, master))

        for func, name in search1_func_list:
            button_config = search1_settings["button"][name]
            TkinterButton(self, button_config, partial(func, self))

        self.item_id_dict = dict()


class CouponListWindow(TopWindow):
    def __init__(self, master, coupon_list: list):
        """ 优惠券显示 """
        super(CouponListWindow, self).__init__("优惠券选择", "600x600")

        for func, name in search2_bind_func_list:
            self[name] = TkinterListBox(self, search2_settings["list"][name])
            self[name].bind("<Double-Button-1>", partial(func, self, master))

        self.coupon_token_dict = dict()
        for number, coupon in enumerate(coupon_list):
            self.coupon_token_dict[number] = coupon["coupon_token"]
            expire = time.localtime(float(coupon["expire_time"]))
            expire_time_text = time.strftime("%Y-%m-%d %H:%M:%S", expire)
            text = f"{coupon['title']}[{expire_time_text}到期]"
            self["list_box"].insert(tkinter.END, text)
