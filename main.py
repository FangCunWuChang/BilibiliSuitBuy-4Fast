from application.apps.app import App

from application.message import showinfo

if __name__ == '__main__':
    app = App()
    showinfo("提示", "原登陆方法已弃用，使用新登陆器[导入登陆]已继续")
    app.mainloop()
