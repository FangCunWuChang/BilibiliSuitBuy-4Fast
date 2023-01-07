import tkinter
import time

from application.module.decoration import (
    application_error,
    application_thread
)
from application.module.utils import ButtonCommand
from application.net.utils import search_suit
from application.message import showinfo


class ItemIdSearchCommandSearch(ButtonCommand):
    def __init__(self, *args, **kwargs):
        super(ItemIdSearchCommandSearch, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        self.root["list_box"].delete("0", tkinter.END)
        self.root.item_id_dict = dict()

        item_id = self.root["ItemId_entry"].value()
        if not item_id:
            return showinfo("提示", "未填写关键字")
        item_id_list = search_suit(item_id)
        for number, item in enumerate(item_id_list):
            self.root.item_id_dict[number] = str(item["item_id"])
            sale = float(item["properties"]["sale_time_begin"])
            sale_time = time.localtime(sale)
            time_text = time.strftime("%Y-%m-%d %H:%M:%S", sale_time)
            suit_text = f"[{time_text}]{item['name']}"
            self.root["list_box"].insert(tkinter.END, suit_text)
        if not item_id_list:
            showinfo("提示", "无搜索结果")
