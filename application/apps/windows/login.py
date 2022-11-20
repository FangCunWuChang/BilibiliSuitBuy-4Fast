from application.apps.windows.app import TopWindow

from application.utils import get_all_value
from application.net.login import LoginQrcode


from PIL import ImageTk
import tkinter
import qrcode


class QrcodeLoginWindow(TopWindow):
    def __init__(self, master):
        """ 扫码登陆 """
        super(QrcodeLoginWindow, self).__init__("扫码登陆", "370x370")

        device_dict = get_all_value(master, "Device_", [])
        device_dict = {k.lower(): v for k, v in device_dict.items()}
        self.login = LoginQrcode(**device_dict)

        login_url, self.auth_code = self.login.GetUrlAndAuthCode()
        image = qrcode.make(login_url).get_image()
        self._photo = ImageTk.PhotoImage(image)
        tkinter.Label(self, image=self._photo).pack()


class SmsLoginWindow(TopWindow):
    def __init__(self, master):
        """ 短信登陆 """
        super(SmsLoginWindow, self).__init__("短信登陆", "500x500")
