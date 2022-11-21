@echo off

cd %~dp0

pyinstaller -F http1_socket_python.py

pyinstaller -F http2_socket_python.py

pause
