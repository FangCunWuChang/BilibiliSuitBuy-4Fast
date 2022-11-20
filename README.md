# BilibiliSuitBuy [b站装扮购买]

**B站装扮购买模拟（98%）【兼容新接口】**

坏消息，新接口已经不支持tv的鉴权了

扫码已经不能使用，抓包后使用导入报文

------------------------------------------------

退回旧版本

修改[./settings/content/buy_setting.json](./settings/content/buy_setting.json)里的host

修改[./settings/content/form_data.json](./settings/content/form_data.json)修改android_old为android

修改[./application/module/command/start.py](./application/module/command/start.py)注释部分代码

修改[./http/source/](./http/source/) /xlive/revenue/v2/order/createOrder 改为 /x/garb/v2/trade/create

修改[./application/module/command/login.py](./application/module/command/login.py) 把原先的code_login注释掉，把__code_login改成code_login

------------------------------------------------

------------------------------------------------

[抓包教程](https://www.bilibili.com/video/BV1Re411g7f5/)

锁定url为 ```/x/garb/v2/mall/suit/detail``` 的包, 选中后点击 ```Raw```

```ctrl+a```全选```ctrl+c```复制, 然后创建一个文本文件```ctrl+v```粘贴进去 最后```ctrl+s```保存
保存的文件就是http报文的文件, Fiddler Everywhere需要开启HTTP2才能抓HTTP2, Classic只有HTTP1.1

------------------------------------------------

**参考：**

[github.com/python-hyper/h2](https://github.com/python-hyper/h2)

[plain-sockets-example.html](https://python-hyper.org/projects/h2/en/stable/plain-sockets-example.html)

------------------------------------------------

你问我为什么不开，我没钱，我没账号，我没设备，我没渠道，我啥都没有，我开个✓8
