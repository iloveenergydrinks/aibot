@echo off
echo ========================================
echo KEEP ALIVE SCRIPT
echo ========================================
echo.
echo This script will:
echo 1. Keep VoiceMeeter running
echo 2. Auto-restart bot if it crashes
echo 3. Prevent session timeout
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

:loop
REM Check if VoiceMeeter is running
tasklist /FI "IMAGENAME eq voicemeeter.exe" 2>NUL | find /I /N "voicemeeter.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo VoiceMeeter not running, starting it...
    start "" "C:\Program Files (x86)\VB\Voicemeeter\voicemeeter.exe"
    timeout /t 5 /nobreak >nul
)

REM Check if bot is running
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo Bot crashed! Restarting in 10 seconds...
    timeout /t 10 /nobreak
    cd /d "C:\Users\miningofficer\Desktop\aibot-main"
    start "Twitter Bot" python -u twitter_autonomous.py
)

REM Wait 60 seconds before checking again
timeout /t 60 /nobreak >nul
goto loop







