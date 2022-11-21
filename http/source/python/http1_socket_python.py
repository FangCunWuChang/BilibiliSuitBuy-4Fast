from timer import BiliTimer
from tools import Tool
import socket
import time
import ssl


class SuitValue(Tool):
    def __init__(self):
        super(SuitValue, self).__init__()

        file_path = self.GetSettingFilePath()
        headers, start_time, delay_time, form_data = self.ReaderSetting(file_path)

        self.host = str(headers["host"])
        self.start_time = int(start_time)
        self.delay_time = int(delay_time)

        __message = self.BuildMessage(headers, form_data)

        self.message_header = __message[:-1]
        self.message_body = __message[-1:]

    @staticmethod
    def BuildMessage(headers: dict, form_data: str) -> bytes:
        message = "POST /xlive/revenue/v2/order/createOrder HTTP/1.1\r\n"
        message += f"native_api_from: {headers['native_api_from']}\r\n"
        message += f"Cookie: {headers['cookie']}\r\n"
        message += f"Accept: {headers['accept']}\r\n"
        message += f"Referer: {headers['referer']}\r\n"
        message += f"env: {headers['env']}\r\n"
        message += f"APP-KEY: {headers['app-key']}\r\n"
        message += f"Buvid: {headers['buvid']}\r\n"
        message += f"User-Agent: {headers['user-agent']}\r\n"
        message += f"x-bili-trace-id: {headers['x-bili-trace-id']}\r\n"
        message += f"x-bili-aurora-eid: {headers['x-bili-aurora-eid']}\r\n"
        message += f"x-bili-mid: {headers['x-bili-mid']}\r\n"
        message += f"x-bili-aurora-zone: {headers['x-bili-aurora-zone']}\r\n"
        message += f"Content-Type: application/x-www-form-urlencoded; charset=utf-8\r\n"
        message += f"Content-Length: {headers['content-length']}\r\n"
        message += f"Host: {headers['host']}\r\n"
        message += f"Connection: {headers['connection']}\r\n"
        message += f"Accept-Encoding: {headers['accept-encoding']}\r\n\r\n"
        return str(message + form_data).encode()


class SuitBuy(SuitValue):
    def __init__(self):
        super(SuitBuy, self).__init__()

    def CreateTlsConnection(self, port: int = 443, **kwargs) -> ssl.SSLSocket:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.purpose = ssl.Purpose.SERVER_AUTH
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_default_certs()
        _connection = socket.create_connection((self.host, port))
        kwargs.update({"server_hostname": self.host})
        connection = context.wrap_socket(_connection, **kwargs)
        return connection

    @staticmethod
    def ReceiveResponse(client: ssl.SSLSocket, length=4096) -> bytes:
        return client.recv(length)


def main():
    print("http1_socket_python")
    suit_buy = SuitBuy()

    bili_timer = BiliTimer(suit_buy.start_time, suit_buy.delay_time)
    bili_timer.WaitLocalTime(3)

    client = suit_buy.CreateTlsConnection()
    client.sendall(suit_buy.message_header)

    bili_timer.WaitSeverTime()

    s = time.time()
    client.sendall(suit_buy.message_body)
    res = suit_buy.ReceiveResponse(client, 1024)
    e = time.time()

    client.close()

    print("\n" + res.decode())
    print("耗时:", (e - s) * 1000, "ms")


if __name__ == '__main__':
    main()
