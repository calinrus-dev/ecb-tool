@echo off
echo ============================================
echo ECB TOOL - Professional Beat Converter
echo ============================================
echo.

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtualenv no encontrado
    echo Ejecuta primero: python -m venv .venv
    pause
    exit /b 1
)

echo [*] Iniciando aplicacion...
echo.

.venv\Scripts\python.exe -m ecb_tool.main

if errorlevel 1 (
    echo.
    echo [ERROR] La aplicacion fallo
    echo Ver logs en: data\app.log
    pause
)

