from application.utils import reader, ReaderMode_Content


app_settings = reader("./settings/controls/app_ui.json")

device_info_settings = reader("./settings/controls/device_info_ui.json")
from_data_info_settings = reader("./settings/controls/from_data_info_ui.json")

search1_settings = reader("./settings/controls/search_suit_ui.json")
search2_settings = reader("./settings/controls/search_coupon_ui.json")

net_session_config = reader("./settings/net/setting.json")

user_agent_format = reader("./settings/content/user_agent.json")
form_data_format = reader("./settings/content/form_data.json")
buy_setting = reader("./settings/content/buy_setting.json")


help_content = reader("./settings/content/help.txt", mode=ReaderMode_Content)
