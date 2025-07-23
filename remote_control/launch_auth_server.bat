@echo off
echo Launching remote auth server...
cd /d %~dp0
python auth\remote_auth_server.py
pause
