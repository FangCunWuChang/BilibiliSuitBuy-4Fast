from application.apps.windows.app import TopWindow

from application.module.decoration import application_error
from application.module.controls import TkinterListBox

from application.message import showinfo

from functools import partial
import subprocess
import tkinter
import os


class StartWindow(TopWindow):
    def __init__(self, http_dict: dict, file: str):
        """ 启动选项 """
        super(StartWindow, self).__init__("启动选择", "300x300")

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
