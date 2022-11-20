from application.utils import reader


kk = {"key": hex(258727790135055252770750870592824059967)[2:], "crypto": True}

label_settings = reader("./settings/controls/label.cjson", **kk)
entry_settings = reader("./settings/controls/entry.cjson", **kk)
button_settings = reader("./settings/controls/button.cjson", **kk)

device_info_label_settings = reader("./settings/controls/device_info/label.cjson", **kk)
device_info_entry_settings = reader("./settings/controls/device_info/entry.cjson", **kk)

from_data_info_label_settings = reader("./settings/controls/from_data_info/label.cjson", **kk)
from_data_info_entry_settings = reader("./settings/controls/from_data_info/entry.cjson", **kk)

net_session_config = reader("./settings/net/setting.json")
login_config_qr = reader("./settings/net/login_qr.json")
login_config_sms = reader("./settings/net/login_sms.json")

user_agent_format = reader("./settings/content/user_agent.json")
form_data_format = reader("./settings/content/form_data.json")
buy_setting = reader("./settings/content/buy_setting.json")
