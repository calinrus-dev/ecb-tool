@echo off
REM Test rápido - Solo el test crítico de NO borrado de archivos

echo ================================================
echo  TEST CRITICO: Verificar NO borrado de archivos
echo ================================================
echo.

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo Ejecutando test critico...
echo.

pytest tests\integration\test_converter_ffmpeg.py::TestVideoConverterFFmpeg::test_source_files_not_deleted -v --tb=short

echo.
echo ================================================
if %ERRORLEVEL% EQU 0 (
    echo  ✓ TEST PASADO - Los archivos NO se borran
) else (
    echo  ✗ TEST FALLADO - Revisar configuracion
)
echo ================================================
echo.

pause
