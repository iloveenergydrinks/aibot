@echo off
title Lord Fishnu - Keep Alive Monitor
color 0A

echo.
echo  ========================================================
echo    LORD FISHNU - KEEP ALIVE MONITOR
echo  ========================================================
echo.
echo    This script monitors and auto-restarts:
echo    - VoiceMeeter
echo    - Sermon Manager Webapp
echo    - Twitter Bot
echo.
echo    Press Ctrl+C to stop monitoring
echo  ========================================================
echo.

set BOT_DIR=%~dp0
set WEBAPP_PORT=5001
set BOT_PORT=5000

:loop
echo [%time%] Checking services...

REM Check VoiceMeeter
tasklist /FI "IMAGENAME eq voicemeeter.exe" 2>NUL | find /I /N "voicemeeter.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo [%time%] VoiceMeeter not running! Starting...
    start "" "C:\Program Files (x86)\VB\Voicemeeter\voicemeeter.exe"
    timeout /t 5 /nobreak >nul
)

REM Check webapp by trying to connect to port 5001
powershell -Command "try { $null = Invoke-WebRequest -Uri 'http://localhost:5001/health' -UseBasicParsing -TimeoutSec 2; exit 0 } catch { exit 1 }" 2>nul
if "%ERRORLEVEL%"=="1" (
    echo [%time%] Webapp not responding! Starting...
    start "Sermon Manager" /MIN cmd /c "cd /d %BOT_DIR% && python sermon_webapp.py"
    timeout /t 3 /nobreak >nul
)

REM Check if twitter_autonomous.py is running
wmic process where "name='python.exe'" get commandline 2>nul | find /I "twitter_autonomous">NUL
if "%ERRORLEVEL%"=="1" (
    echo [%time%] Bot not running! Starting in 10 seconds...
    timeout /t 10 /nobreak >nul
    start "Lord Fishnu Bot" cmd /c "cd /d %BOT_DIR% && python -u twitter_autonomous.py --headless"
)

REM Wait 30 seconds before next check
timeout /t 30 /nobreak >nul
goto loop

