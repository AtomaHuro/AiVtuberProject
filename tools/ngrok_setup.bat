@echo off
REM ngrok_setup.bat - Starts ngrok for port 8080 (EventSub)
start /min ngrok http 8080
echo [NGROK] Tunnel started on port 8080
pause
