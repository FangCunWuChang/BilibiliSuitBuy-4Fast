# BilibiliSuitBuy [b站装扮购买]

**B站装扮购买模拟（98%）【兼容新接口】**

[登陆](https://github.com/lllk140/bilibili-login)

登陆保存的文件通用的，导入就行

------------------------------------------------

启动时间留空就是自动获取装扮开售时间

退回旧版本

启动时跟上 ```--old``` 启动旧版本

例 ```python main.py --old```

------------------------------------------------

------------------------------------------------

[抓包教程](https://www.bilibili.com/video/BV1Re411g7f5/)

锁定url为 ```/x/garb/v2/mall/suit/detail``` 的包, 选中后点击 ```Raw```

```ctrl+a```全选```ctrl+c```复制, 然后创建一个文本文件```ctrl+v```粘贴进去 最后```ctrl+s```保存
保存的文件就是http报文的文件, Fiddler Everywhere需要开启HTTP2才能抓HTTP2, Classic只有HTTP1.1

------------------------------------------------

**参考：**

[github.com/python-hyper/h2](https://github.com/python-hyper/h2)

[github.com/kuresaru/geetest-validator](https://github.com/kuresaru/geetest-validator)

[plain-sockets-example.html](https://python-hyper.org/projects/h2/en/stable/plain-sockets-example.html)

------------------------------------------------

你问我为什么不开，我没钱，我没账号，我没设备，我没渠道，我啥都没有，我开个✓8
