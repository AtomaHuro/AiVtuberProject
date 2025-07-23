@echo off
REM ffmpeg_router.bat - Routes TTS audio to Voicemeeter or stream
set AUDIO_FILE=tts_audio\response.wav
start /min ffplay -nodisp -autoexit "%AUDIO_FILE%"
echo [FFMPEG] Played TTS audio through default route
pause
