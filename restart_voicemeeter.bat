@echo off
echo Restarting VoiceMeeter...
taskkill /F /IM voicemeeter.exe 2>nul
timeout /t 2 /nobreak >nul
start "" "C:\Program Files (x86)\VB\Voicemeeter\voicemeeter.exe"
echo VoiceMeeter restarted! Wait 5 seconds then run your bot.
timeout /t 5 /nobreak







