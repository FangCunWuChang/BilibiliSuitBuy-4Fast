from application.module.decoration import (
    application_error, application_thread
)


from application.apps.windows.serach import (
    ItemsListWindow,
    CouponListWindow
)


@application_thread
@application_error
def item_id_search(master) -> None:
    ItemsListWindow(master)


@application_thread
@application_error
def coupon_search(master) -> None:
    CouponListWindow(master)
