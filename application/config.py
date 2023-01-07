from application.utils import reader, ReaderMode_Content

from application.items import (
    AppConfig,
    ButtonConfig,
    LabelConfig,
    EntryConfig,
    ListBoxConfig
)

font_0 = ("Microsoft YaHei", 14)
font_1 = ("Microsoft YaHei", 16)
font_2 = ("Microsoft YaHei", 18)


# "主页面"基础样式
config_base_app = AppConfig("理塘最強伝説と絶兇の猛虎!純真丁一郎です", "#f0f0f0", False, "470x210")


# "启动窗口"基础样式
config_base_start = AppConfig("启动选择", "#f0f0f0", False, "300x300")
config_controls_Start_listbox = ListBoxConfig(font_0, w=280, h=280, x=10, y=10)


# "设备信息"基础样式
config_base_DeviceSetting = AppConfig("设备信息", "#f0f0f0", False, "500x170")


# "装扮搜索"基础样式
config_base_ItemsSearch = AppConfig("装扮搜索/选择", "#f0f0f0", False, "500x600")


# "基础信息"基础样式
config_base_BaseSetting = AppConfig("基础信息设置", "#f0f0f0", False, "280x170")

# "优惠券搜索"基础样式
config_base_CouponSearch = AppConfig("优惠券选择", "#f0f0f0", False, "600x600")


# "装扮搜索"页面样式
config_controls_ItemsSearch_listbox = ListBoxConfig(font_0, w=480, h=540, x=10, y=50)
config_controls_ItemsSearch_entry = EntryConfig(None, font_0, w=420, h=30, x=10, y=10)
config_controls_ItemsSearch_button = ButtonConfig("搜索", font_0, w=50, h=30, x=440, y=10)


# "基础信息"页面样式
config_controls_BaseSetting_addMonth_label = LabelConfig("购买时长", font_2, w=100, h=30, x=10, y=10)
config_controls_BaseSetting_fSource_label = LabelConfig("购买位置", font_2, w=100, h=30, x=10, y=50)
config_controls_BaseSetting_shopFrom_label = LabelConfig("购买来源", font_2, w=100, h=30, x=10, y=90)

config_controls_BaseSetting_addMonth_entry = EntryConfig(None, font_0, w=150, h=30, x=120, y=10)
config_controls_BaseSetting_fSource_entry = EntryConfig(None, font_0, w=150, h=30, x=120, y=50)
config_controls_BaseSetting_shopFrom_entry = EntryConfig(None, font_0, w=150, h=30, x=120, y=90)

config_controls_BaseSetting_apply_button = ButtonConfig("应用", font_0, w=260, h=30, x=10, y=130)


# "优惠券搜索"页面样式
config_controls_CouponSearch_listbox = ListBoxConfig(font_0, w=580, h=580, x=10, y=10)


# "设备信息设置"页面样式
config_controls_DeviceSetting_buvid_entry = EntryConfig(None, font_1, w=300, h=30, x=120, y=10)
config_controls_DeviceSetting_model_entry = EntryConfig(None, font_1, w=120, h=30, x=120, y=50)
config_controls_DeviceSetting_osver_entry = EntryConfig(None, font_1, w=120, h=30, x=360, y=50)
config_controls_DeviceSetting_name_entry = EntryConfig(None, font_1, w=120, h=30, x=120, y=90)
config_controls_DeviceSetting_code_entry = EntryConfig(None, font_1, w=120, h=30, x=360, y=90)

config_controls_DeviceSetting_random_button = ButtonConfig("随机", font_0, w=50, h=30, x=430, y=10)
config_controls_DeviceSetting_apply_button = ButtonConfig("应用/保存", font_0, w=460, h=30, x=20, y=130)

config_controls_DeviceSetting_buvid_label = LabelConfig("设备标识", font_2, w=100, h=25, x=10, y=10)
config_controls_DeviceSetting_model_label = LabelConfig("手机型号", font_2, w=100, h=25, x=10, y=50)
config_controls_DeviceSetting_osver_label = LabelConfig("系统版本", font_2, w=100, h=25, x=250, y=50)
config_controls_DeviceSetting_name_label = LabelConfig("应用名称", font_2, w=100, h=25, x=10, y=90)
config_controls_DeviceSetting_code_label = LabelConfig("应用版本", font_2, w=100, h=25, x=250, y=90)


# "主页面"页面样式
config_controls_app_BuyNum_label = LabelConfig("购买数量", font_2, w=100, h=30, x=10, y=10)
config_controls_app_ItemId_label = LabelConfig("装扮标识", font_2, w=100, h=30, x=210, y=10)
config_controls_app_Coupon_label = LabelConfig("优惠凭证", font_2, w=100, h=30, x=10, y=50)
config_controls_app_StartT_label = LabelConfig("启动时间", font_2, w=100, h=30, x=10, y=90)
config_controls_app_DelayT_label = LabelConfig("延迟时间", font_2, w=100, h=30, x=280, y=90)

config_controls_app_BuyNum_entry = EntryConfig("1", font_1, w=80, h=30, x=120, y=10)
config_controls_app_DelayT_entry = EntryConfig("0", font_1, w=70, h=30, x=390, y=90)
config_controls_app_ItemId_entry = EntryConfig(None, font_1, w=80, h=30, x=320, y=10)
config_controls_app_Coupon_entry = EntryConfig(None, font_1, w=280, h=30, x=120, y=50)
config_controls_app_StartT_entry = EntryConfig(None, font_1, w=150, h=30, x=120, y=90)

config_controls_app_ItemIdSearch_Button = ButtonConfig("搜索", font_0, w=50, h=30, x=410, y=10)
config_controls_app_CouponSearch_Button = ButtonConfig("搜索", font_0, w=50, h=30, x=410, y=50)
config_controls_app_ImportLogin_Button = ButtonConfig("导入登录", font_0, w=105, h=30, x=10, y=130)
config_controls_app_ImportMessage_Button = ButtonConfig("导入报文", font_0, w=105, h=30, x=125, y=130)
config_controls_app_DeviceSetting_Button = ButtonConfig("设备信息", font_0, w=105, h=30, x=240, y=130)
config_controls_app_BaseSetting_Button = ButtonConfig("基础信息", font_0, w=105, h=30, x=355, y=130)
config_controls_app_Start_Button = ButtonConfig("开始运行", font_0, w=390, h=30, x=10, y=170)
config_controls_app_Help_Button = ButtonConfig("帮助", font_0, w=50, h=30, x=410, y=170)


# 所需内容[user_agent]
user_agent_format = reader("./settings/content/user_agent.txt", ReaderMode_Content)
user_agent_format = user_agent_format.decode().replace("\n", "")

# 启动内容设置
buy_setting = reader("./settings/content/buy_setting.json")

# 网络设置
net_session_config = reader("./settings/net/setting.json")

# 所需密钥
SIGN_ANDROID = ("1d8b6e7d45233436", "560c52ccd288fed045859ed18bffd973")


# 帮助信息
help_content = reader("./settings/content/help.txt", mode=ReaderMode_Content)
help_content = help_content.decode()
