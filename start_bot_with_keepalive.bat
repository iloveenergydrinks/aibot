@echo off
echo ================================================================
echo Starting Michael Saylor Bot with VoiceMeeter Auto-Restart
echo ================================================================
echo.

REM Start VoiceMeeter if not running
tasklist /FI "IMAGENAME eq voicemeeter.exe" 2>NUL | find /I /N "voicemeeter.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo Starting VoiceMeeter...
    start "" "C:\Program Files (x86)\VB\Voicemeeter\voicemeeter.exe"
    timeout /t 5 /nobreak >nul
)

REM Start VoiceMeeter keepalive in a new window
echo Starting VoiceMeeter Auto-Restart...
start "VoiceMeeter KeepAlive" cmd /k "cd /d %~dp0 && python voicemeeter_keepalive.py"

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start the bot in main window
echo.
echo Starting Michael Saylor Bot...
echo.
python -u twitter_autonomous.py

REM When bot stops, this continues
echo.
echo Bot stopped. VoiceMeeter KeepAlive is still running in separate window.
echo Close the KeepAlive window manually if needed.
pause








