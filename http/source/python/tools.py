import json
import sys
import os


class Tool(object):
    @staticmethod
    def ReaderSetting(file_path) -> tuple[dict, int, int, str, str]:
        """ 读取文件 """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        f.close()

        headers = data["headers"]
        form_data = data["form_data"]
        start_time = data["setting"]["start_time"]
        delay_time = data["setting"]["delay_time"]
        old_or_new = data["old_or_new"]

        print(f"启用老接口:[{'是' if old_or_new else '否'}]")
        print(f"装扮id:[{data['setting']['item_id']}]")
        print(f"启动时间:[{start_time}]")
        print(f"延时:[{delay_time}ms]")

        if old_or_new is True:
            path = "/x/garb/v2/trade/create"
        else:
            path = "/xlive/revenue/v2/order/createOrder"
        return headers, start_time, delay_time, form_data, path

    @staticmethod
    def GetSettingFilePath():
        """ 获取文件 """
        if len(sys.argv) == 1:
            file_path = "./setting.json"
        else:
            file_path = sys.argv[-1]
        if not os.path.exists(file_path):
            sys.exit(f"[{file_path}]不存在")
        print(f"配置文件:[{file_path}]")
        return file_path
