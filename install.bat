@echo off

echo install requirements.txt

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo install app

cd %~dp0

pyinstaller main.py -F

cd dist

move main.exe %~dp0

cd %~dp0

rd /s /q build

rd /s /q dist

del /f /s /q *.spec

pause
