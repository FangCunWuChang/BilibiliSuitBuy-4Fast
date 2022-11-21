@echo off

cd %~dp0

go build http1_socket_golang.go timer.go tools.go

go build http2_socket_golang.go timer.go tools.go

pause
