# Script PowerShell para ejecutar tests del convertidor
# Ejecuta todos los tests de conversión con reporte detallado

Write-Host "================================================" -ForegroundColor Cyan
Write-Host " Tests del Convertidor de Video - ECB TOOL" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual si existe
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

# Test 1: Integration tests con FFmpeg real
Write-Host ""
Write-Host "[1/4] Ejecutando tests de integracion con FFmpeg..." -ForegroundColor Green
Write-Host "------------------------------------------------" -ForegroundColor Gray
pytest tests\integration\test_converter_ffmpeg.py -v --tb=short --color=yes -m "not slow"

# Test 2: Business logic tests
Write-Host ""
Write-Host "[2/4] Ejecutando tests de logica de negocio..." -ForegroundColor Green
Write-Host "------------------------------------------------" -ForegroundColor Gray
pytest tests\integration\test_conversion_business_logic.py -v --tb=short --color=yes

# Test 3: Unit tests
Write-Host ""
Write-Host "[3/4] Ejecutando tests unitarios..." -ForegroundColor Green
Write-Host "------------------------------------------------" -ForegroundColor Gray
pytest tests\unit\test_conversion.py -v --tb=short --color=yes

# Test 4: Coverage report
Write-Host ""
Write-Host "[4/4] Generando reporte de cobertura..." -ForegroundColor Green
Write-Host "------------------------------------------------" -ForegroundColor Gray
pytest tests\ -k "conversion" --cov=ecb_tool.features.conversion --cov-report=term-missing --cov-report=html

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " Tests completados" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ver el reporte de cobertura HTML, abre:" -ForegroundColor Yellow
Write-Host "  htmlcov\index.html" -ForegroundColor White
Write-Host ""

Read-Host "Presiona Enter para salir"
