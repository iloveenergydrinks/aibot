@echo off
title Lord Fishnu - Stop Script
color 0C

echo.
echo  ========================================================
echo    STOPPING LORD FISHNU
echo  ========================================================
echo.

echo [1/3] Stopping Python processes...
taskkill /F /IM python.exe 2>nul
if "%ERRORLEVEL%"=="0" (
    echo       Python processes stopped!
) else (
    echo       No Python processes found.
)
echo.

echo [2/3] Webapp and bot stopped.
echo.

echo [3/3] VoiceMeeter left running (close manually if needed)
echo.

echo  ========================================================
echo    ALL FISHNU SERVICES STOPPED
echo  ========================================================
echo.
echo    VoiceMeeter is still running for other uses.
echo    To stop VoiceMeeter: taskkill /F /IM voicemeeter.exe
echo.
pause


