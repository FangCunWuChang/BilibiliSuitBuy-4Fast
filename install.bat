@echo off

cd %~dp0

echo install requirements.txt

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo install python-http

cd %~dp0

cd http/source/python

pyinstaller http1_socket_python.py -F

pyinstaller http2_socket_python.py -F

echo set golang GOPROXY

go env -w GO111MODULE=on

go env -w GOPROXY=https://goproxy.cn,direct

echo install golang mod

cd %~dp0

cd http/source/golang

go get golang.org/x/net/http2

go get github.com/lllk140/gh2

echo install golang-http

go build http1_socket_golang.go timer.go tools.go 

go build http2_socket_golang.go timer.go tools.go

echo install app

cd %~dp0

pyinstaller main.py -F

echo move and delete

python install.py

pause
