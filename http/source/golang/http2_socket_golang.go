package main

import (
	"bytes"
	"crypto/tls"
	"fmt"
	"github.com/lllk140/gh2/GH2"
	"time"
)

// BuildFrames
// 生成帧
func BuildFrames(headers map[string]string, formData string) *GH2.H2Connection {
	var h2connection = new(GH2.H2Connection)
	h2connection.InitiateConnection()
	h2connection.SendSettings(0, nil, 0)
	var __headers = GH2.HEADERS{
		{Name: ":method", Value: "POST"},
		{Name: ":path", Value: "/xlive/revenue/v2/order/createOrder"},
		{Name: ":authority", Value: headers["host"]},
		{Name: ":scheme", Value: "https"},
		{Name: "native_api_from", Value: headers["native_api_from"]},
		{Name: "buvid", Value: headers["buvid"]},
		{Name: "accept", Value: headers["accept"]},
		{Name: "env", Value: headers["env"]},
		{Name: "app-key", Value: headers["app-key"]},
		{Name: "user-agent", Value: headers["user-agent"]},
		{Name: "x-bili-trace-id", Value: headers["x-bili-trace-id"]},
		{Name: "x-bili-mid", Value: headers["x-bili-mid"]},
		{Name: "x-bili-aurora-zone", Value: headers["x-bili-aurora-zone"]},
		{Name: "content-type", Value: headers["content-type"]},
		{Name: "content-length", Value: headers["content-length"]},
		{Name: "accept-encoding", Value: headers["accept-encoding"]},
		{Name: "cookie", Value: headers["cookie"]},
	}
	h2connection.SendHeaders(1, __headers, 4)
	h2connection.SendData(1, []byte(formData), 1)
	return h2connection
}

// H2CreateTlsConnection
// 创建连接
func H2CreateTlsConnection(BuyHost string) *tls.Conn {
	var adder = fmt.Sprintf("%v:443", BuyHost)
	var client, _ = tls.Dial("tcp", adder, &tls.Config{
		InsecureSkipVerify: false,
		ServerName:         BuyHost,
		NextProtos:         []string{"h2"},
		MinVersion:         tls.VersionTLS12,
		MaxVersion:         tls.VersionTLS12,
		ClientAuth:         tls.RequireAndVerifyClientCert,
	})
	return client
}

// H2SendMessage
// 发送请求
func H2SendMessage(client *tls.Conn, body []byte) {
	_, _ = client.Write(body)
}

// H2ReceiveResponse
// 接收响应
func H2ReceiveResponse(client *tls.Conn, th2 *GH2.H2Connection) ([]byte, GH2.HEADERS) {
	var result []byte
	var headers GH2.HEADERS

	var data = make([]byte, 8196)
	var length, _ = client.Read(data)

	for len(data[:length]) > 0 {
		var events = th2.ReceiveData(data[:length])
		for _, event := range events {
			if value, ok := event.(*GH2.HeadersFrame); ok == true {
				headers = value.Headers
			}
			if value, ok := event.(*GH2.DataFrame); ok == true {
				result = bytes.Join([][]byte{result, value.Body}, []byte(""))
			}
			if _, ok := event.(*GH2.EndStream); ok == true {
				return result, headers
			}
		}
		data = make([]byte, 8196)
		length, _ = client.Read(data)
	}
	return result, headers
}

func CloseH2(client *tls.Conn, th2 *GH2.H2Connection) {
	th2.CloseConnection(1, 0, 0)
	_, _ = client.Write(th2.DataToSend())
}

func main() {
	var filePath = GetSettingFilePath()
	var headers, startTime, delayTime, formData = ReaderSetting(filePath)
	var SleepTimeNumber = float64(delayTime) * float64(time.Second)

	var h2connection = BuildFrames(headers, formData)
	var __message = h2connection.DataToSend()
	var MessageHeader = __message[:len(__message)-1]
	var MessageBody = __message[len(__message)-1:]

	WaitLocalBiliTimer(startTime, 3)

	var client = H2CreateTlsConnection(headers["host"])
	H2SendMessage(client, MessageHeader)

	WaitServerBiliTimer(startTime, 4)

	time.Sleep(time.Duration(SleepTimeNumber))

	var s = time.Now().UnixNano() / 1e6
	H2SendMessage(client, MessageBody)
	var res, _ = H2ReceiveResponse(client, h2connection)
	var e = time.Now().UnixNano() / 1e6

	CloseH2(client, h2connection)
	_ = client.Close()

	fmt.Printf("%v\n", string(res))
	fmt.Printf("耗时%vms\n", e-s)
}
