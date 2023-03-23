import uuid

from urllib.parse import urlencode

from application.module.utils import (
    ButtonCommand,
    get_all_device_value,
    get_all_login_value,
    get_all_base_value,
    FormData
)
from application.module.decoration import (
    application_thread,
    application_error
)
from application.message import (
    askopenfilename,
    asksavefilename,
    showinfo
)
from application.utils import (
    reader, writer,
    parse_cookies,
    build_x_bili_aurora_eid,
    build_x_bili_trace_id,
    get_sdk_int
)
from application.errors import (
    ItemIdFormatError,
    DelayTimeFormatError,
    LoginWarning
)
from application.net.utils import (
    get_pay_bp,
    get_versions,
    login_verify,
    search_coupon
)
from application.config import (
    config_base_DeviceSetting,
    config_base_BaseSetting,
    config_base_ItemsSearch,
    config_base_CouponSearch
)
from application.config import (
    SIGN_ANDROID,
    user_agent_format,
    buy_setting,
    help_content
)
from application.apps.windows import (
    DeviceSettingWindow,
    BaseSettingWindow,
    ItemsSearchWindow,
    CouponSearchWindow
)
from application.config import (
    config_controls_DeviceSetting_apply_button,
    config_controls_DeviceSetting_random_button,

    config_controls_DeviceSetting_buvid_entry,
    config_controls_DeviceSetting_code_entry,
    config_controls_DeviceSetting_name_entry,
    config_controls_DeviceSetting_model_entry,
    config_controls_DeviceSetting_osver_entry,

    config_controls_DeviceSetting_buvid_label,
    config_controls_DeviceSetting_code_label,
    config_controls_DeviceSetting_name_label,
    config_controls_DeviceSetting_model_label,
    config_controls_DeviceSetting_osver_label,
)
from application.config import (
    config_controls_BaseSetting_apply_button,

    config_controls_BaseSetting_addMonth_entry,
    config_controls_BaseSetting_fSource_entry,
    config_controls_BaseSetting_shopFrom_entry,

    config_controls_BaseSetting_addMonth_label,
    config_controls_BaseSetting_fSource_label,
    config_controls_BaseSetting_shopFrom_label
)
from application.config import (
    config_controls_ItemsSearch_entry,
    config_controls_ItemsSearch_button
)
from application.module.command.setting import (
    DeviceSettingCommandRandom,
    DeviceSettingCommandApply,
    BaseSettingCommandApply
)
from application.module.command.serach import (
    ItemIdSearchCommandSearch
)


class AppCommandHelp(ButtonCommand):
    """ 帮助 """
    def __init__(self, *args, **kwargs):
        super(AppCommandHelp, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        showinfo("帮助", help_content)


class AppCommandCouponSearch(ButtonCommand):
    """ 优惠券搜索 """
    def __init__(self, *args, **kwargs):
        super(AppCommandCouponSearch, self).__init__(*args, **kwargs)
        self.main_app_root = kwargs["main_app_root"]

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        login = get_all_login_value(self.root, True)
        access_key, cookie = login["accessKey"], login["cookie"]
        mid = login_verify(parse_cookies(cookie), access_key)

        if mid is False:
            raise LoginWarning("登录标识验证失败")

        item_id = self.root["ItemId_entry"].value()
        if not item_id:
            return showinfo("提示", "未填写装扮标识")

        coupon_list = search_coupon(item_id, parse_cookies(cookie))
        if not coupon_list:
            return showinfo("提示", "未搜索到可用优惠券")

        CouponSearchWindow(self.root, coupon_list, config_base_CouponSearch)


class AppCommandItemIdSearch(ButtonCommand):
    """ 装扮标识搜索 """
    def __init__(self, *args, **kwargs):
        super(AppCommandItemIdSearch, self).__init__(*args, **kwargs)
        self.main_app_root = kwargs["main_app_root"]

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        app = ItemsSearchWindow(self.root, config_base_ItemsSearch)

        app.loadEntry("ItemId_entry", config_controls_ItemsSearch_entry)
        app.loadButton(ItemIdSearchCommandSearch, config_controls_ItemsSearch_button)


class AppCommandBaseSetting(ButtonCommand):
    """ 基础信息设置 """
    def __init__(self, *args, **kwargs):
        super(AppCommandBaseSetting, self).__init__(*args, **kwargs)
        self.main_app_root = kwargs["main_app_root"]

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        app = BaseSettingWindow(config_base_BaseSetting)
        app.loadLabel(config_controls_BaseSetting_addMonth_label)
        app.loadLabel(config_controls_BaseSetting_fSource_label)
        app.loadLabel(config_controls_BaseSetting_shopFrom_label)
        app.loadEntry("addMonth_entry", config_controls_BaseSetting_addMonth_entry)
        app.loadEntry("fSource_entry", config_controls_BaseSetting_fSource_entry)
        app.loadEntry("shopFrom_entry", config_controls_BaseSetting_shopFrom_entry)
        aa = (BaseSettingCommandApply, config_controls_BaseSetting_apply_button)
        app.loadButton(*aa, main_app_root=self.root)

        base = get_all_base_value(self.root, False)
        for i in base:
            app[f"{i}_entry"].writer(str(base[i]))


class AppCommandDeviceSetting(ButtonCommand):
    """ 设备信息设置 """
    def __init__(self, *args, **kwargs):
        super(AppCommandDeviceSetting, self).__init__(*args, **kwargs)
        self.main_app_root = kwargs["main_app_root"]

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        app = DeviceSettingWindow(config_base_DeviceSetting)
        app.loadLabel(config_controls_DeviceSetting_buvid_label)
        app.loadLabel(config_controls_DeviceSetting_code_label)
        app.loadLabel(config_controls_DeviceSetting_name_label)
        app.loadLabel(config_controls_DeviceSetting_model_label)
        app.loadLabel(config_controls_DeviceSetting_osver_label)
        app.loadEntry("BilibiliBuvid_entry", config_controls_DeviceSetting_buvid_entry)
        app.loadEntry("AndroidModel_entry", config_controls_DeviceSetting_model_entry)
        app.loadEntry("AndroidBuild_entry", config_controls_DeviceSetting_osver_entry)
        app.loadEntry("VersionName_entry", config_controls_DeviceSetting_name_entry)
        app.loadEntry("VersionCode_entry", config_controls_DeviceSetting_code_entry)
        app.loadButton(DeviceSettingCommandRandom, config_controls_DeviceSetting_random_button)
        app_args = (DeviceSettingCommandApply, config_controls_DeviceSetting_apply_button)
        app.loadButton(*app_args, main_app_root=self.root)

        # 写入
        devices = get_all_device_value(self.root, False)
        for li in devices:
            app[f"{li}_entry"].writer(devices[li])

        # 自动获取
        if not devices["VersionName"] or not devices["VersionCode"]:
            code, name = get_versions("android")
            app["VersionCode_entry"].writer(str(code))
            app["VersionName_entry"].writer(str(name))


class AppCommandImportLogin(ButtonCommand):
    """ 导入登陆 """
    def __init__(self, *args, **kwargs):
        super(AppCommandImportLogin, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        args = ("导入登录标识", [("json", "*.json")], "login.json")
        login_content = reader(askopenfilename(*args))
        self.root["Login_cookie"] = login_content["cookie"]
        self.root["Login_accessKey"] = login_content["accessKey"]

class AppCommandStart(ButtonCommand):
    """ 启动 """
    def __init__(self, *args, **kwargs):
        super(AppCommandStart, self).__init__(*args, **kwargs)

    @staticmethod
    def build_user_agent(device: dict):
        user_agent = user_agent_format.format(
            ANDROID_BUILD=device["AndroidModel"],
            ANDROID_MODEL=device["AndroidBuild"],
            ANDROID_BUILD_M=buy_setting["build_m"],
            BUVID=device["BilibiliBuvid"],
            SDK_INT=get_sdk_int(device["AndroidBuild"]),
            VERSION_CODE=device["VersionCode"],
            CHANNEL=buy_setting["channel"],
            SESSION_ID=str(uuid.uuid4()).replace("-", "")[:8],
            VERSION_NAME=device["VersionName"]
        )
        return user_agent

    @staticmethod
    def build_biz_extra(base: dict, coupon_token_entry: str):
        biz = '{"add_month":%s,"coupon_token":"%s","m_source":"%s","f_source":"%s","from":"%s","from_id":"%s"}'
        biz_extra = biz % (base["addMonth"], coupon_token_entry, "", base["fSource"], base["shopFrom"], "")
        return biz_extra

    @staticmethod
    def build_pay_bp(item_id_entry: str, buy_number_entry: str):
        pay_bp_number = int(get_pay_bp(item_id_entry))
        return pay_bp_number * int(buy_number_entry)

    @staticmethod
    def build_statistics(device: dict):
        __statistics = '{"appId":1,"platform":3,"version":"%s","abtest":""}'
        __statistics = __statistics % (device["VersionName"],)
        return __statistics

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        device = get_all_device_value(self.root, True)
        login = get_all_login_value(self.root, True)
        base = get_all_base_value(self.root, True)

        coupon_token_entry = self.root["Coupon_entry"].value()

        # ---------------------------------------------------
        if not self.root["DelayT_entry"].value():
            self.root["DelayT_entry"].writer("0")

        if not self.root["BuyNum_entry"].value():
            self.root["BuyNum_entry"].writer("1")

        buy_number = self.root["BuyNum_entry"].number(False)
        if buy_number < 0 or buy_number > 10:
            buy_number = 1

        # ---------------------------------------------------
        item_id_entry = self.root["ItemId_entry"].value()
        if not item_id_entry.isdigit():
            raise ItemIdFormatError("装扮标识格式错误")
        
        start_time = self.root["StartT_entry"].number(False)
        
        delay_time = self.root["DelayT_entry"].number(False)
        if delay_time <= -1000 or delay_time >= 1000:
            raise DelayTimeFormatError("延迟时间格式错误")

        __cookie = parse_cookies(login["cookie"])

        form_data = urlencode(FormData({
            "access_key": login["accessKey"],
            "biz_extra": self.build_biz_extra(base, coupon_token_entry),
            "biz_id": item_id_entry,
            "biz_source": "1",
            "context_id": "0",
            "context_type": "102",
            "csrf": __cookie["bili_jct"],
            "disable_rcmd": "0",
            "goods_id": "195",
            "goods_num": str(buy_number),
            "pay_bp": self.build_pay_bp(item_id_entry, buy_number),
            "platform": "android",
            "statistics": self.build_statistics(device),
            "ts": start_time
        }).toSign(SIGN_ANDROID))

        __referer = buy_setting["referer"].format(
            F_SOURCE=base["fSource"],
            SHOP_FROM=base["shopFrom"],
            ID=item_id_entry
        )

        headers: dict = buy_setting["headers"]
        headers.update({"content-length": str(len(form_data))})
        headers.update({"cookie": login["cookie"]})
        headers.update({"buvid": device["BilibiliBuvid"]})
        headers.update({"x-bili-aurora-eid": build_x_bili_aurora_eid(__cookie["DedeUserID"])})
        headers.update({"x-bili-mid": __cookie["DedeUserID"]})
        headers.update({"x-bili-trace-id": build_x_bili_trace_id(start_time)})
        headers.update({"referer": __referer})
        headers.update({"host": buy_setting["host"]})
        headers.update({"user-agent": self.build_user_agent(device)})

        start_content = {
            "setting": {
                "start_time": start_time,
                "delay_time": delay_time,
                "item_id": item_id_entry
            },
            "form_data": form_data,
            "headers": headers,
        }

        args = ("保存启动设置", [("json", "*.json")], ".json")
        file_path = asksavefilename(*args)
        if not file_path.isspace():
            start_file = writer(file_path, start_content)

            showinfo("提示", "启动配置已保存于: " + start_file)
