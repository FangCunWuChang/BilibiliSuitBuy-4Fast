import tkinter.messagebox
import tkinter.filedialog

from application.errors import GuiFileAskWarning


def showinfo(title: str, message: any):
    """ 提示 """
    tkinter.messagebox.showinfo(title, message)


def showwarning(title: str, message: any):
    """ 警告 """
    tkinter.messagebox.showwarning(title, message)


def showerror(title: str, message: any):
    """ 错误 """
    tkinter.messagebox.showerror(title, message)


def askopenfilename(title, types, initialfile=None) -> str:
    """ 打开文件框，选择打开位置 """
    kwargs = {"title": title, "filetypes": types}
    if initialfile and isinstance(initialfile, str):
        kwargs.update({"initialfile": initialfile})
    file_ack = tkinter.filedialog.askopenfilename(**kwargs)
    if not file_ack:
        raise GuiFileAskWarning("...")
    return file_ack
