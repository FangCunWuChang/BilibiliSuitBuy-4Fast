import tkinter

from application.utils import read_device_content
from application.errors import GuiItemNotExist
from application.net.utils import (
    get_versions,
    MobiAPP_ANDROID
)
from application.items import (
    ButtonConfig,
    LabelConfig,
    AppConfig,
    EntryConfig
)
from application.items import (
    TkinterEntry,
    TkinterLabel
)
from application.config import (
    config_base_app,
    config_controls_app_Help_Button,
    config_controls_app_BaseSetting_Button,
    config_controls_app_Start_Button,
    config_controls_app_CouponSearch_Button,
    config_controls_app_DeviceSetting_Button,
    config_controls_app_ImportLogin_Button,
    config_controls_app_ItemIdSearch_Button
)
from application.config import (
    config_controls_app_Coupon_entry,
    config_controls_app_BuyNum_entry,
    config_controls_app_DelayT_entry,
    config_controls_app_StartT_entry,
    config_controls_app_ItemId_entry
)
from application.config import (
    config_controls_app_Coupon_label,
    config_controls_app_BuyNum_label,
    config_controls_app_DelayT_label,
    config_controls_app_ItemId_label,
    config_controls_app_StartT_label
)
from application.module.command.app import (
    AppCommandHelp,
    AppCommandBaseSetting,
    AppCommandStart,
    AppCommandCouponSearch,
    AppCommandDeviceSetting,
    AppCommandImportLogin,
    AppCommandItemIdSearch
)


class App(tkinter.Tk):
    def __init__(self, config: AppConfig):
        super(App, self).__init__()

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
        command(self, config=config, **kwargs)

    def loadEntry(self, item_name: str, config: EntryConfig):
        self[item_name] = TkinterEntry(self, config=config)

    def loadLabel(self, config: LabelConfig):
        TkinterLabel(self, config=config)


device_content = read_device_content()
code, name = get_versions(MobiAPP_ANDROID)

app = App(config_base_app)

app["Device_BilibiliBuvid"] = device_content.get("BilibiliBuvid", "")
app["Device_AndroidModel"] = device_content.get("AndroidModel", "")
app["Device_AndroidBuild"] = device_content.get("AndroidBuild", "")
app["Device_VersionName"] = device_content.get("VersionName", str(name))
app["Device_VersionCode"] = device_content.get("VersionCode", str(code))

app["Base_addMonth"] = "-1"
app["Base_fSource"] = "shop"
app["Base_shopFrom"] = "feed.card"

app["Login_accessKey"] = None
app["Login_cookie"] = None


app.loadLabel(config_controls_app_Coupon_label)
app.loadLabel(config_controls_app_BuyNum_label)
app.loadLabel(config_controls_app_DelayT_label)
app.loadLabel(config_controls_app_ItemId_label)
app.loadLabel(config_controls_app_StartT_label)

app.loadEntry("Coupon_entry", config_controls_app_Coupon_entry)
app.loadEntry("BuyNum_entry", config_controls_app_BuyNum_entry)
app.loadEntry("DelayT_entry", config_controls_app_DelayT_entry)
app.loadEntry("StartT_entry", config_controls_app_StartT_entry)
app.loadEntry("ItemId_entry", config_controls_app_ItemId_entry)

app.loadButton(AppCommandHelp, config_controls_app_Help_Button)
app.loadButton(AppCommandStart, config_controls_app_Start_Button)
app.loadButton(AppCommandImportLogin, config_controls_app_ImportLogin_Button)
app.loadButton(AppCommandBaseSetting, config_controls_app_BaseSetting_Button, main_app_root=app)
app.loadButton(AppCommandCouponSearch, config_controls_app_CouponSearch_Button, main_app_root=app)
app.loadButton(AppCommandDeviceSetting, config_controls_app_DeviceSetting_Button, main_app_root=app)
app.loadButton(AppCommandItemIdSearch, config_controls_app_ItemIdSearch_Button, main_app_root=app)

