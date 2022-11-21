from timer import BiliTimer
from tools import Tool
import h2.connection
import h2.events
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

        self.h2connection = self.BuildFrames(headers, form_data)
        __message = self.h2connection.data_to_send()
        self.message_header = __message[:-1]
        self.message_body = __message[-1:]

    def BuildFrames(self, headers: dict, form_data: str) -> h2.connection.H2Connection:
        h2connection = h2.connection.H2Connection()
        h2connection.initiate_connection()
        __headers = [
            (":method", "POST"),
            (":path", "/xlive/revenue/v2/order/createOrder"),
            (":authority", self.host),
            (":scheme", "https"),
            ("native_api_from", headers["native_api_from"]),
            ("buvid", headers["buvid"]),
            ("accept", headers["accept"]),
            ("referer", headers["referer"]),
            ("env", headers["env"]),
            ("app-key", headers["app-key"]),
            ("user-agent", headers["user-agent"]),
            ("x-bili-trace-id", headers["x-bili-trace-id"]),
            ("x-bili-aurora-eid", headers["x-bili-aurora-eid"]),
            ("x-bili-mid", headers["x-bili-mid"]),
            ("x-bili-aurora-zone", headers["x-bili-aurora-zone"]),
            ("content-type", headers["content-type"]),
            ("content-length", headers["content-length"]),
            ("accept-encoding", headers["accept-encoding"]),
            ("cookie", headers["cookie"]),
        ]
        h2connection.send_headers(1, __headers)
        h2connection.send_data(1, form_data.encode(), end_stream=True)
        return h2connection


class SuitBuy(SuitValue):
    def __init__(self):
        super(SuitBuy, self).__init__()

    def CreateTlsConnection(self, port: int = 443, **kwargs) -> ssl.SSLSocket:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.purpose = ssl.Purpose.SERVER_AUTH
        context.verify_mode = ssl.CERT_REQUIRED
        context.set_alpn_protocols(["h2"])
        context.check_hostname = True
        context.load_default_certs()
        _connection = socket.create_connection((self.host, port))
        kwargs.update({"server_hostname": self.host})
        connection = context.wrap_socket(_connection, **kwargs)
        return connection

    def ReceiveResponse(self, client: ssl.SSLSocket, length=8192) -> bytes:
        response = bytes()
        recv_data = client.recv(length)
        while recv_data:
            events = self.h2connection.receive_data(recv_data)
            for event in events:
                if isinstance(event, h2.events.DataReceived):
                    response += event.data
                if isinstance(event, h2.events.StreamEnded):
                    client.sendall(self.h2connection.data_to_send())
                    return response
            client.sendall(self.h2connection.data_to_send())
            recv_data = client.recv(length)
        return response

    def CloseH2(self, client: ssl.SSLSocket):
        self.h2connection.close_connection()
        client.sendall(self.h2connection.data_to_send())


def main():
    print("http2_socket_python")
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

    suit_buy.CloseH2(client)
    client.close()

    print("\n" + res.decode())
    print("耗时:", (e - s) * 1000, "ms")


if __name__ == '__main__':
    main()
