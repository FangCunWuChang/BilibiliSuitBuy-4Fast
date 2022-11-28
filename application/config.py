from application.utils import reader
import sys

label_settings = reader("./settings/controls/label.json")
entry_settings = reader("./settings/controls/entry.json")
button_settings = reader("./settings/controls/button.json")

device_info_label_settings = reader("./settings/controls/device_info/label.json")
device_info_entry_settings = reader("./settings/controls/device_info/entry.json")

from_data_info_label_settings = reader("./settings/controls/from_data_info/label.json")
from_data_info_entry_settings = reader("./settings/controls/from_data_info/entry.json")

net_session_config = reader("./settings/net/setting.json")

user_agent_format = reader("./settings/content/user_agent.json")
form_data_format = reader("./settings/content/form_data.json")
buy_setting = reader("./settings/content/buy_setting.json")

if sys.argv[-1] == "--old":
    buy_setting["host"] = buy_setting["old_host"]
else:
    buy_setting["host"] = buy_setting["new_host"]
