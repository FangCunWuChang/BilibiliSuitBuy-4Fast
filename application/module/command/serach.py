from application.module.decoration import (
    application_error, application_thread
)


from application.apps.windows.serach import (
    ItemsListWindow,
    CouponListWindow
)

from application.errors import LoginWarning

from application.message import showinfo

from application.net.utils import search_coupon, login_verify
from application.utils import parse_cookies


@application_thread
@application_error
def item_id_search(master) -> None:
    ItemsListWindow(master)


@application_thread
@application_error
def coupon_search(master) -> None:
    cookie = getattr(master, "Value_cookie", None)
    access_key = getattr(master, "Value_accessKey", None)
    if not all([cookie, access_key]):
        raise LoginWarning("未导入登陆标识")

    mid = login_verify(parse_cookies(cookie), access_key)
    if mid is False:
        raise LoginWarning("登录标识验证失败")

    item_id = master["item_id_entry"].value("未填写装扮标识")

    coupon_list = search_coupon(item_id, parse_cookies(cookie))
    if not coupon_list:
        return showinfo("提示", "未搜索到可用优惠券")

    CouponListWindow(master, coupon_list)
