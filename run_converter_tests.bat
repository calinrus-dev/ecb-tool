@echo off
REM Script para ejecutar los tests del convertidor
REM Ejecuta todos los tests de conversión con FFmpeg

echo ================================================
echo  Tests del Convertidor de Video - ECB TOOL
echo ================================================
echo.

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
)

echo.
echo [1/3] Ejecutando tests de integracion de FFmpeg...
echo ------------------------------------------------
pytest tests\integration\test_converter_ffmpeg.py -v --tb=short --color=yes

echo.
echo [2/3] Ejecutando tests de logica de negocio...
echo ------------------------------------------------
pytest tests\integration\test_conversion_business_logic.py -v --tb=short --color=yes

echo.
echo [3/3] Ejecutando todos los tests unitarios de conversion...
echo ------------------------------------------------
pytest tests\unit\test_conversion.py -v --tb=short --color=yes

echo.
echo ================================================
echo  Tests completados
echo ================================================
echo.

pause
