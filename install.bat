@echo off

cd %~dp0

pyinstaller -F main.py -i ./icon/logo1.ico

pause
