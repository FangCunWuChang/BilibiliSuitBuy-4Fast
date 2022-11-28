from application.module.command.serach import (
    item_id_search, coupon_search
)

from application.module.command.info import (
    device_info, from_data_info
)

from application.module.command.login import (
    verify_login,
    get_login_device
)

from application.module.command.save import (
    save_login, save_setting
)

from application.module.command.open import (
    open_login, open_message, open_setting
)

from application.module.command.start import (
    start
)

func_list = [
    (item_id_search, "item_id_search"),
    (coupon_search, "coupon_search"),
    (device_info, "device_info"),
    (verify_login, "verify_login"),
    (get_login_device, "get_login_device"),
    (save_login, "save_login"),
    (open_login, "open_login"),
    (from_data_info, "from_data_info"),
    (open_message, "open_message"),
    (save_setting, "save_setting"),
    (open_setting, "open_setting"),
    (start, "start")
]
