from application.module.decoration import (
    application_error, application_thread
)

from application.apps.windows.info import (
    DeviceInfoWindow, FromDataWindow
)


@application_thread
@application_error
def device_info(master) -> None:
    DeviceInfoWindow(master)


@application_thread
@application_error
def from_data_info(master) -> None:
    FromDataWindow(master)
