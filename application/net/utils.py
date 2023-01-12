from application.errors import LoginWarning, GuiValueError, ResponseError
from application.net.session import Session


MobiAPP_TV: str = "android_tv_yst"
MobiAPP_ANDROID: str = "android"


def get_versions(mod: str = MobiAPP_ANDROID) -> tuple[str, str]:
    url = f"https://app.bilibili.com/x/v2/version"
    with Session() as session:
        res = session.request("GET", url, params={"mobi_app": mod})
    build = str(res.json()["data"][0]["build"])
    version = str(res.json()["data"][0]["version"])
    return build, version


def get_sale_time(item_id: str) -> int:
    """ 获取开售时间 """
    try:
        url = f"https://api.bilibili.com/x/garb/v2/mall/suit/detail"
        with Session() as session:
            res = session.request("GET", url, params={"item_id": item_id})
    except Exception as err:
        raise GuiValueError("不正确的装扮标识或他错误", err)
    else:
        return int(res.json()["data"]["properties"]["sale_time_begin"])


def search_suit(key: str) -> list:
    """ 搜索装扮 """
    url = "https://api.bilibili.com/x/garb/v2/mall/home/search"
    with Session() as session:
        res = session.request("GET", url, params={"key_word": key})
    return res.json()["data"]["list"] or list()


def search_coupon(item_id: str, cookie: dict) -> list:
    """ 优惠劵查找 """
    url = "https://api.bilibili.com/x/garb/coupon/usable?item_id=11"
    with Session() as session:
        kk = {"params": {"item_id": item_id}, "cookies": cookie}
        res = session.request("GET", url, **kk)
    if res.json()["code"] == -101:
        raise LoginWarning("账号未登录")
    return res.json()["data"] or list()


def login_verify(cookie: dict, access_key: str) -> bool | str:
    """ 验证登录 """
    # url = "http://api.bilibili.com/x/member/web/account"
    # with Session() as session:
    #     params = {"access_key": access_key}
    #     res1 = session.request("GET", url, params=params)
    #     res2 = session.request("GET", url, cookies=cookie)
    # if res1.json()["code"] == res2.json()["code"] == 0:
    #     return str(res1.json()["data"]["mid"])
    # return False
    return "0"


def get_pay_bp(item_id: str) -> str:
    url = "https://api.bilibili.com/x/garb/v2/mall/suit/detail"
    with Session() as session:
        res = session.request("GET", url, params={"item_id": item_id})
    if res.json()["data"]["suit_items"] is None:
        raise ResponseError(f"[{item_id}]没有此装扮")
    number = int(res.json()["data"]["properties"]["sale_bp_forever_raw"])
    return str(number * 10)
