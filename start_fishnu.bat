@echo off
title Lord Fishnu Sermon
color 0E

echo.
echo  ========================================================
echo    LORD FISHNU - SERMON SYSTEM
echo  ========================================================
echo.

REM Check VoiceMeeter
tasklist /FI "IMAGENAME eq voicemeeter.exe" 2>NUL | find /I /N "voicemeeter.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo Starting VoiceMeeter...
    start "" "C:\Program Files (x86)\VB\Voicemeeter\voicemeeter.exe"
    timeout /t 3 /nobreak >nul
)

echo.
echo  Dashboard: http://localhost:5001
echo  Press Ctrl+C to stop
echo.
echo  ========================================================
echo.

cd /d %~dp0
python -u run_sermon.py

pause

