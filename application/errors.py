class GuiItemNotExist(Exception):
    """ [错误]GUI无法取得值 """
    def __init__(self, *args):
        super(GuiItemNotExist, self).__init__(*args)
        self.title = "GUI无法取得值"


class DidNotEnter(Warning):
    """ [警告]未输入内容 """
    def __init__(self, *args):
        super(DidNotEnter, self).__init__(*args)
        self.title = "[警告]未输入内容"


class GuiDeviceValueNotExist(Warning):
    """ [警告]设备信息未填写 """
    def __init__(self, *args):
        super(GuiDeviceValueNotExist, self).__init__(*args)
        self.title = "[警告]设备信息未填写"


class GuiBaseValueNotExist(Warning):
    """ [警告]基础信息未填写 """
    def __init__(self, *args):
        super(GuiBaseValueNotExist, self).__init__(*args)
        self.title = "[警告]基础信息未填写"


class GuiLoginValueNotExist(Warning):
    """ [警告]登陆信息未导入/获取 """
    def __init__(self, *args):
        super(GuiLoginValueNotExist, self).__init__(*args)
        self.title = "[警告]登陆信息未导入/获取"


class ItemIdFormatError(Warning):
    """ [警告]装扮标识格式错误 """
    def __init__(self, *args):
        super(ItemIdFormatError, self).__init__(*args)
        self.title = "[警告]装扮标识格式错误"


class ReaderError(Exception):
    """ [错误]无法读取 """
    def __init__(self, *args):
        super(ReaderError, self).__init__(*args)
        self.title = "[错误]无法读取"


class GuiFileAskWarning(Warning):
    """ [警告]未打开文件会话 """
    def __init__(self, *args: object):
        super(GuiFileAskWarning, self).__init__(*args)
        self.title = "[警告]未打开文件会话"


class LoginWarning(Warning):
    """ [警告]账号未登陆 """
    def __init__(self, *args: object):
        super(LoginWarning, self).__init__(*args)
        self.title = "[警告]账号未登陆"


class GuiValueError(Exception):
    """ [错误]无法获取值 """
    def __init__(self, *args: object):
        super(GuiValueError, self).__init__(*args)
        self.title = "[错误]无法获取值"


class GuiEntryIndexWarning(Warning):
    """ [警告]无法获取输入框的值 """
    def __init__(self, *args: object):
        super(GuiEntryIndexWarning, self).__init__(*args)
        self.title = "[警告]无法获取输入框的值"


class GuiValueIndexWarning(Warning):
    """ [警告]无法获取到值 """
    def __init__(self, *args: object):
        super(GuiValueIndexWarning, self).__init__(*args)
        self.title = "[警告]无法获取到值"


class SdkIntIndexError(Exception):
    def __init__(self, *args: object):
        """ [错误]无法找到对应的SdkInt"""
        super(SdkIntIndexError, self).__init__(*args)
        self.title = "[错误]无法找到对应的SdkInt"


class ResponseError(Exception):
    def __init__(self, *args: object):
        """ [错误]响应错误 """
        super(ResponseError, self).__init__(*args)
        self.title = "[错误]响应错误"


class FormatError(Exception):
    def __init__(self, *args: object):
        """ [错误]格式不正确 """
        super(FormatError, self).__init__(*args)
        self.title = "[错误]格式不正确"


class GuiStartWarning(Warning):
    """ [警告]无法启动 """
    def __init__(self, *args: object):
        super(GuiStartWarning, self).__init__(*args)
        self.title = "[警告]无法启动"
