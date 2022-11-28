from application.errors import GuiEntryIndexWarning
import tkinter


class TkinterEntry(tkinter.Entry):
    """ 输入框 """
    def __init__(self, master, config: dict):
        super(TkinterEntry, self).__init__(master, **config["self"])
        self.insert(0, config["default"] or str())
        self.place(**config["place"])

    def writer(self, text: str):
        """ 显示 """
        self.delete(0, tkinter.END)
        self.insert(0, text or str())

    def value(self, err=False):
        """ 获取内容 string err 不存在则抛出异常 """
        value = str(self.get())
        if not value and err:
            raise GuiEntryIndexWarning(err)
        return value

    def number(self, f=True) -> float | int:
        """ 获取内容 !f = int """
        value = self.value()
        if not value:
            return 0. if f else 0
        negative = False
        if value[:1] == "-":
            negative = True
            value = value[1:]
        if value.isdigit():
            number = float(value)
            res = number if f else round(number)
            return res * -1 if negative else res
        s = value.split(".")
        if 0 < len(s) <= 2:
            while "" in s:
                s.remove("")
            if all([i.isdigit() for i in s]):
                number = float(value)
                res = number if f else round(number)
                return res * -1 if negative else res
        return 0. if f else 0


class TkinterLabel(tkinter.Label):
    """ 标签 """
    def __init__(self, master, config: dict):
        super(TkinterLabel, self).__init__(master, **config["self"])
        self.place(**config["place"])


class TkinterButton(tkinter.Button):
    """ 按钮 """
    def __init__(self, master, config: dict, command: any):
        config["self"]["command"] = command
        super(TkinterButton, self).__init__(master, **config["self"])
        self.place(**config["place"])


class TkinterListBox(tkinter.Listbox):
    """ 列表 """
    def __init__(self, master, config: dict):
        super(TkinterListBox, self).__init__(master, **config["self"])
        self.place(**config["place"])
