@echo off

cd %~dp0

pyinstaller -F main.py

pause
