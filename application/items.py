import tkinter


class AppConfig(object):
    """ ui基础设置 """
    def __init__(self, title: str, bg: str, resizable: bool, geometry: str):
        self.title, self.bg, self.geometry = title, bg, geometry
        self.resizable = (resizable, resizable)


class Place(object):
    """ 位置 """
    def __init__(self, w: int, h: int, x: int, y: int):
        super(Place, self).__init__()
        self.width, self.height, self.x, self.y = w, h, x, y


class ButtonConfig(object):
    """ 按钮设置 """
    def __init__(self, text: str, font: tuple[str, int], **kwargs):
        super(ButtonConfig, self).__init__()

        self.place = Place(**kwargs).__dict__
        self.text, self.font = text, font

    @property
    def content(self):
        return {"text": self.text, "font": self.font}


class EntryConfig(object):
    """ 输入框设置 """
    def __init__(self, default: str | None, font: tuple[str, int], state: str, **kwargs):
        super(EntryConfig, self).__init__()

        self.state = state
        self.place = Place(**kwargs).__dict__
        self.default, self.font = default, font

    @property
    def content(self):
        return {"font": self.font, "state": self.state}


class LabelConfig(object):
    """ 标签设置 """
    def __init__(self, text: str, font: tuple[str, int], **kwargs):
        super(LabelConfig, self).__init__()

        self.place = Place(**kwargs).__dict__
        self.text, self.font = text, font

    @property
    def content(self):
        return {"text": self.text, "font": self.font}


class ListBoxConfig(object):
    """  """
    def __init__(self, font: tuple[str, int], **kwargs):
        super(ListBoxConfig, self).__init__()

        self.place = Place(**kwargs).__dict__
        self.font = font

    @property
    def content(self):
        return {"font": self.font}


class TkinterEntry(tkinter.Entry):
    """ 输入框 """
    def __init__(self, root, config: EntryConfig):
        super(TkinterEntry, self).__init__(root, **config.content)
        self.insert(0, config.default or "")
        self.place(**config.place)

    def writer(self, text: str):
        """ 显示 """
        self.delete(0, tkinter.END)
        self.insert(0, text or str())

    def value(self) -> str:
        """ 获取内容 string """
        return str(self.get())

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
    def __init__(self, root, config: LabelConfig):
        super(TkinterLabel, self).__init__(root, **config.content)
        self.place(**config.place)


class TkinterButton(tkinter.Button):
    """ 按钮 """
    def __init__(self, root, config: ButtonConfig, func: any):
        root_config = config.content
        root_config.update({"command": func})
        super(TkinterButton, self).__init__(root, **root_config)
        self.place(**config.place)


class TkinterListBox(tkinter.Listbox):
    """ 列表 """
    def __init__(self, root, config: ListBoxConfig):
        super(TkinterListBox, self).__init__(root, **config.content)
        self.place(**config.place)
