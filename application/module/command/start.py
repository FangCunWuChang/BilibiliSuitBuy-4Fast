from application.module.decoration import (
    application_error, application_thread
)

from application.utils import (
    get_all_value, parse_cookies,
    build_x_bili_aurora_eid,
    build_x_bili_trace_id,
    get_sdk_int, buildSign,
    SIGN_ANDROID, writer
)

from application.message import askyesno

from application.config import (
    form_data_format, user_agent_format, buy_setting
)

from application.apps.windows.start import StartWindow
from application.net.utils import get_sale_time, get_pay_bp

from urllib.parse import quote
import json
import glob
import time
import uuid
import os


@application_thread
@application_error
def start(master) -> None:
    http_dict = dict()
    for li in glob.glob("./http/*.bat"):
        name = os.path.splitext(os.path.split(li)[1])[0]
        http_dict[str(name)] = li

    entry_data = get_all_value(master, "_entry", ["coupon", "start_time"])
    device_data = get_all_value(master, "Device_", [])
    value_data = get_all_value(master, "Value_", [])
    data_data = get_all_value(master, "Data_", [])

    entry_data.update({"delay_time": master["delay_time_entry"].number(False)})

    start_time = master["start_time_entry"].number(False)
    if start_time == -1:
        master["start_time_entry"].writer(str(round(time.time()) + 60))

    if not start_time:
        start_time = get_sale_time(entry_data["item_id"])
        master["start_time_entry"].writer(str(start_time))

    start_time = master["start_time_entry"].number(False)
    if time.time() >= start_time:
        if not askyesno("确认", "启动时间小于当前时间, 是否继续"):
            return

    entry_data.update({"start_time": start_time})

    __statistics = '{"appId":1,"platform":3,"version":"__ver__","abtest":""}'
    __statistics = __statistics.replace("__ver__", data_data["versionName"])
    __cookie = parse_cookies(value_data["cookie"])
    __eid = build_x_bili_aurora_eid(__cookie["DedeUserID"])
    __trace_id = build_x_bili_trace_id(entry_data["start_time"])

    # 新版本
    # ./setting/content/form_data.json 短一点的，中间那个，键改名为android启用
    # ./setting/content/buy_setting.json 键host的值改为api.live.bilibili.com启用
    biz_extra = json.dumps({
        "add_month": int(data_data["addMonth"]),
        "coupon_token": entry_data["coupon"],
        "m_source": "",
        "f_source": data_data["fSource"],
        "from": data_data["shopFrom"],
        "from_id": ""
    }, separators=(",", ":"))

    form_data_text = form_data_format["android"].format(
        ACCESS_KEY=value_data["accessKey"],
        BIZ_EXTRA=quote(biz_extra),
        ITEM_ID=entry_data["item_id"],
        CSRF=__cookie["bili_jct"],
        BUY_NUM=entry_data["buy_num"],
        PAY_BP=get_pay_bp(entry_data["item_id"]),
        STATISTICS=quote(__statistics),
        TS=str(entry_data["start_time"])
    )
    # ---------------------------------------------------------

    # 旧版本支持
    # ./setting/content/form_data.json 长一点的，最上面那个，键改名为android启用
    # ./setting/content/buy_setting.json 键host的值改为api.bilibili.com启用
    # form_data_text = form_data_format["android"].format(
    #     ACCESS_KEY=value_data["accessKey"],
    #     ADD_MONTH=data_data["addMonth"],
    #     BUY_NUM=entry_data["buy_num"],
    #     COUPON_TOKEN=entry_data["coupon"],
    #     CSRF=__cookie["bili_jct"],
    #     F_SOURCE=data_data["fSource"],
    #     SHOP_FROM=data_data["shopFrom"],
    #     ITEM_ID=entry_data["item_id"],
    #     STATISTICS=quote(__statistics),
    #     TS=str(entry_data["start_time"])
    # )
    # ---------------------------------------------------------

    user_agent = user_agent_format["android"].format(
        ANDROID_BUILD=device_data["AndroidModel"],
        ANDROID_MODEL=device_data["AndroidBuild"],
        ANDROID_BUILD_M=buy_setting["build_m"],
        BUVID=device_data["Buvid"],
        SDK_INT=get_sdk_int(device_data["AndroidBuild"]),
        VERSION_CODE=data_data["versionCode"],
        CHANNEL=buy_setting["channel"],
        SESSION_ID=str(uuid.uuid4()).replace("-", "")[:8],
        VERSION_NAME=data_data["versionName"]
    )

    __referer = buy_setting["referer"].format(
        F_SOURCE=data_data["fSource"],
        SHOP_FROM=data_data["shopFrom"],
        ID=entry_data["item_id"]
    )

    sign = buildSign(form_data_text, SIGN_ANDROID)
    form_data = form_data_text + f"&sign={sign}"

    headers: dict = buy_setting["headers"]
    headers.update({"content-length": str(len(form_data))})
    headers.update({"cookie": value_data["cookie"]})
    headers.update({"buvid": device_data["Buvid"]})
    headers.update({"x-bili-aurora-eid": __eid})
    headers.update({"x-bili-mid": __cookie["DedeUserID"]})
    headers.update({"x-bili-trace-id": __trace_id})
    headers.update({"referer": __referer})
    headers.update({"host": buy_setting["host"]})
    headers.update({"user-agent": user_agent})

    setting = {
        "start_time": entry_data["start_time"],
        "delay_time": entry_data["delay_time"],
        "item_id": entry_data["item_id"]
    }

    data = {
        "setting": setting,
        "form_data": form_data,
        "headers": headers,
    }

    file_name = buildSign(json.dumps(data), str()) + ".json"
    StartWindow(http_dict, writer(f"./start-data/{file_name}", data))
