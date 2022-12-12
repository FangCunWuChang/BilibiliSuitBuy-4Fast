from timer import BiliTimer
from tools import Tool
import socket
import time
import ssl


class SuitValue(Tool):
    def __init__(self):
        super(SuitValue, self).__init__()

        file_path = self.GetStartFilePath()
        headers, start_time, delay_time, form_data = self.ReaderSetting(file_path)

        self.host = str(headers["host"])
        self.start_time = int(start_time)
        self.delay_time = int(delay_time)

        __message = self.BuildMessage(headers, form_data)

        self.message_header = __message[:-1]
        self.message_body = __message[-1:]

    @staticmethod
    def BuildMessage(headers: dict, form_data: str) -> bytes:
        message = f"POST /xlive/revenue/v2/order/createOrder HTTP/1.1\r\n"

        for li in headers.items():
            message += ": ".join(list(li)) + "\r\n"

        return str(message + "\r\n" + form_data).encode()


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
