@echo off
echo Launching remote terminal...
cd /d %~dp0
python tools\RemoteControlTerminalUI.py
pause
