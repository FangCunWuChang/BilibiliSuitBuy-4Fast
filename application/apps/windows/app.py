import tkinter
from application.errors import GuiValueError


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
