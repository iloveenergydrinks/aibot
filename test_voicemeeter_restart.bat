@echo off
echo ================================================================
echo Testing VoiceMeeter Audio Engine Restart
echo ================================================================
echo.
echo This will test if the VoiceMeeter restart command works.
echo You should hear/see VoiceMeeter audio engine restart.
echo.
pause

python -c "from voicemeeter_keepalive import restart_audio_engine; restart_audio_engine()"

echo.
echo ================================================================
echo Test Complete
echo ================================================================
echo.
echo Did you see a success message?
echo If yes, the VoiceMeeter restart is working correctly!
echo.
pause






