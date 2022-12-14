@echo off

echo install python-http

cd %~dp0http\source\python

pyinstaller http1_socket_python.py -F

pyinstaller http2_socket_python.py -F

cd dist

move http1_socket_python.exe %~dp0http\exe

move http2_socket_python.exe %~dp0http\exe

cd %~dp0http\source\python

rd /s /q build

rd /s /q dist

del /f /s /q *.spec

echo install golang-http

cd %~dp0http\source\golang

go build http1_socket_golang.go timer.go tools.go

go build http2_socket_golang.go timer.go tools.go

move http1_socket_golang.exe %~dp0http\exe

move http2_socket_golang.exe %~dp0http\exe

pause

exit
