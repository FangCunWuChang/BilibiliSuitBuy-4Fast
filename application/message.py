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


def askyesno(title: str, message: any) -> bool:
    """ 选择框 """
    return tkinter.messagebox.askyesno(title, message)


def asksaveasfile(title, types, initialfile="setting.json") -> str:
    """ 打开文件框，选择保存位置 """
    kwargs = {"title": title, "filetypes": types}
    if initialfile:
        kwargs.update({"initialfile": initialfile})
    file_ack = tkinter.filedialog.asksaveasfile(**kwargs)
    if not file_ack:
        raise GuiFileAskWarning("文件会话框未选择")
    return file_ack.name


def askopenfilename(title, types, initialfile=None) -> str:
    """ 打开文件框，选择打开位置 """
    kwargs = {"title": title, "filetypes": types}
    if initialfile and isinstance(initialfile, str):
        kwargs.update({"initialfile": initialfile})
    file_ack = tkinter.filedialog.askopenfilename(**kwargs)
    return file_ack
