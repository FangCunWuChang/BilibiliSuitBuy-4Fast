import tkinter

from application.errors import GuiItemNotExist
from application.items import (
    AppConfig,
    ButtonConfig,
    EntryConfig,
    LabelConfig,
    ListBoxConfig
)
from application.items import (
    TkinterEntry,
    TkinterLabel,
    TkinterListBox
)


class TopWindow(tkinter.Toplevel):
    """ 子窗口 """
    def __init__(self, config: AppConfig):
        super(TopWindow, self).__init__()

        self.title(config.title)
        self.configure(background=config.bg)
        self.resizable(*config.resizable)
        self.geometry(config.geometry)

    def __setitem__(self, key: str, value) -> any:
        """ 设置 """
        return setattr(self, str(key), value)

    def __getitem__(self, item: str):
        """ 取得 """
        value = getattr(self, str(item), None)
        if value is None:
            raise GuiItemNotExist(f"找不到{item}")
        return value

    def loadButton(self, command: any, config: ButtonConfig, **kwargs):
        command(self, config, **kwargs)

    def loadEntry(self, item_name: str, config: EntryConfig):
        self[item_name] = TkinterEntry(self, config=config)

    def loadLabel(self, config: LabelConfig):
        TkinterLabel(self, config=config)

    def loadListBox(self, item_name: str, config: ListBoxConfig):
        self[item_name] = TkinterListBox(self, config=config)
