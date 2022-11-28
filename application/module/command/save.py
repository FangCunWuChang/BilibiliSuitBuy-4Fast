from application.module.decoration import (
    application_error, application_thread
)

from application.utils import (
    get_all_value, parse_cookies, writer
)

from application.message import (
    asksaveasfile, showinfo
)


@application_thread
@application_error
def save_login(master) -> None:
    login_data = get_all_value(master, "Value_", [], False)
    mid_f = str(parse_cookies(login_data["cookie"])["DedeUserID"]) + ".json"
    file_path = asksaveasfile("保存登录标识", [("json", "*.json")], mid_f)
    writer(file_path, login_data)
    showinfo("提示", "操作完成")


@application_thread
@application_error
def save_setting(master) -> None:
    entry_data = get_all_value(master, "_entry", ["coupon"])
    device_data = get_all_value(master, "Device_", [])
    value_data = get_all_value(master, "Value_", [])
    data_data = get_all_value(master, "Data_", [])

    entry_data.update({"delay_time": master["delay_time_entry"].number(False)})
    entry_data.update({"start_time": master["start_time_entry"].number(False)})

    data_dict = {"entry": entry_data}
    data_dict.update({"device": device_data})
    data_dict.update({"value": value_data})
    data_dict.update({"data": data_data})

    file_path = asksaveasfile("保存配置", [("json", "*.json")], "setting.json")

    writer(file_path, data_dict)
    showinfo("提示", "操作完成")
