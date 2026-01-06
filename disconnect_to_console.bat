@echo off
echo ========================================
echo Disconnecting RDP and moving to console session
echo Audio will keep working after disconnect
echo ========================================
echo.
echo WARNING: This will disconnect your RDP session!
echo Your bot will keep running with audio working.
echo.
pause

REM Get current session ID
for /f "tokens=3" %%a in ('query session %username% ^| find "%username%"') do set SESSIONID=%%a

echo Disconnecting session %SESSIONID% and reconnecting to console...
tscon %SESSIONID% /dest:console

REM This will disconnect you but keep the session on console with audio working







