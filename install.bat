@echo off

cd %~dp0

pip install -r requirements.txt

pyinstaller -F main.py

pause
