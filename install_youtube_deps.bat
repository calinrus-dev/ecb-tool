@echo off
echo Instalando dependencias de YouTube API...
".venv\Scripts\pip.exe" install google-auth google-auth-oauthlib google-api-python-client
echo.
echo Dependencias instaladas correctamente.
echo.
pause
