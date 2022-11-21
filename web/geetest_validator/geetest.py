from application.module.decoration import (
    application_error, application_thread
)

from application.utils import urlQuerySplit

from flask import Flask, render_template, redirect, request
from urllib.parse import urlsplit
import webview
import base64
import json
import time
import os


def flask_app(gee_gt, gee_challenge):
    template = os.path.abspath("./web/geetest_validator/template")
    static = os.path.abspath("./web/geetest_validator/static")
    app = Flask(__name__, template_folder=template, static_folder=static)

    @app.route("/")
    def index():
        if len(request.args) == 0:
            return redirect(f"/?gt={gee_gt}&challenge={gee_challenge}")
        return render_template("index.html")

    @app.route("/finish")
    def quit_flask():
        return "完成登陆, 等待跳转"

    return app


class GeeTest(object):
    def __init__(self, gt, challenge):
        super(GeeTest, self).__init__()
        app = flask_app(gt, challenge)

        self.verify_data = "/"

        self.web = webview.create_window("人机验证", app)
        self._GetGeeVerifyData()

    @application_thread
    @application_error
    def _GetGeeVerifyData(self) -> None:
        self.verify_data = self.web.get_current_url()
        while urlsplit(self.verify_data).path == "/":
            self.verify_data = self.web.get_current_url()
            time.sleep(3)
        self.web.destroy()

    def waitFinishing(self) -> dict:
        """ 获取到极验证数据 """
        while urlsplit(self.verify_data).path == "/":
            time.sleep(3)
        query_dict = urlQuerySplit(self.verify_data)
        debase64 = base64.b64decode(query_dict["data"]).decode()
        return json.loads(debase64)

