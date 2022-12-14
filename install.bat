@echo off

echo install app

install-http

cd %~dp0

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

pyinstaller main.py -F

cd dist

move main.exe %~dp0

cd %~dp0

rd /s /q build

rd /s /q dist

del /f /s /q *.spec

pause
