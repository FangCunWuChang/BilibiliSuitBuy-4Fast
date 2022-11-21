

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
