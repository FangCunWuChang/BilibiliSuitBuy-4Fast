from application.errors import GuiFileAskWarning
from application.message import showerror
import threading


def application_thread(func):
    """ 多线程 """
    def wrapper(*args, **kwargs):
        thread_kwargs = {
            "target": func,
            "args": args,
            "kwargs": kwargs
        }
        t = threading.Thread(**thread_kwargs)
        t.start()
        return t
    return wrapper


def application_error(func):
    """ 报错弹窗 """
    def wrapper(*args, **kwargs):
        try:
            results = func(*args, **kwargs)
        except Exception as e:
            if e.__class__ == GuiFileAskWarning:
                return None
            showerror(getattr(e, "title", "错误"), e)
        else:
            return results
    return wrapper
