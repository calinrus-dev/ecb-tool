# Tests del Convertidor de Video 🎬

## 📋 Descripción

Suite completa de tests para el convertidor de video que verifica:

✅ **Conversión real con FFmpeg** - Usa FFmpeg para crear videos reales  
✅ **Sin borrado automático** - Verifica que los archivos fuente NO se borran  
✅ **Lógica de negocio completa** - Validación, errores, configuración  
✅ **Manejo de errores** - Archivos inválidos, faltantes, etc.  
✅ **Múltiples formatos** - MP3, WAV, FLAC, JPG, PNG, etc.

## 🗂️ Archivos de Test

### `test_converter_ffmpeg.py` (17 tests)
Tests de integración con FFmpeg real:

1. ✅ Verificación de FFmpeg disponible
2. ✅ Inicialización del convertidor
3. ✅ Detección de múltiples formatos de audio
4. ✅ Detección de múltiples formatos de imagen
5. ✅ Validación de creación de jobs
6. ✅ Creación de directorios de salida
7. ✅ **Conversión REAL con FFmpeg**
8. ✅ **Archivos fuente NO se borran** (CRÍTICO)
9. ✅ Auto-borrado de beats cuando está habilitado
10. ✅ Auto-borrado de covers cuando está habilitado
11. ✅ Manejo de archivos de audio inválidos
12. ✅ Manejo de archivos de imagen inválidos
13. ✅ Manejo de archivos faltantes
14. ✅ Parseo de resoluciones
15. ✅ Cleanup solo en trabajos completados
16. ✅ Múltiples conversiones secuenciales
17. ✅ Transiciones de estado del job

### `test_conversion_business_logic.py` (25 tests)
Tests de lógica de negocio:

- Validación de configuración (resolución, FPS, bitrates)
- Procesamiento por lotes (batch)
- Validación de existencia de archivos
- Validación de rutas de salida
- Manejo de archivos duplicados
- Lógica de cleanup parcial
- Validación de extensiones de archivos
- Exclusión de archivos ocultos
- Manejo de directorios vacíos/inexistentes
- Captura de mensajes de error
- Ordenamiento de archivos
- Matching de extensiones case-insensitive
- Inmutabilidad de configuración
- Tracking de progreso

## 🚀 Cómo Ejecutar

### Opción 1: Script Batch (Windows CMD)
```batch
run_converter_tests.bat
```

### Opción 2: Script PowerShell (Recomendado)
```powershell
.\run_converter_tests.ps1
```

### Opción 3: Pytest Directo

**Todos los tests:**
```bash
pytest tests/integration/test_converter_ffmpeg.py tests/integration/test_conversion_business_logic.py -v
```

**Solo tests de FFmpeg:**
```bash
pytest tests/integration/test_converter_ffmpeg.py -v
```

**Solo lógica de negocio:**
```bash
pytest tests/integration/test_conversion_business_logic.py -v
```

**Con reporte de cobertura:**
```bash
pytest tests/ -k "conversion" --cov=ecb_tool.features.conversion --cov-report=html
```

## 📦 Requisitos

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Dependencias de testing:
- `pytest` - Framework de testing
- `pytest-cov` - Reporte de cobertura
- `ffmpeg-python` - Wrapper de FFmpeg
- FFmpeg instalado en el sistema

### Verificar FFmpeg:
```bash
ffmpeg -version
```

## 🔍 Tests Clave

### Test de Conversión Real
```python
test_real_conversion_with_ffmpeg()
```
- Crea archivos de audio e imagen reales
- Ejecuta FFmpeg para generar video
- Verifica que el video se creó correctamente
- Valida que el archivo tiene contenido

### Test Sin Borrado (CRÍTICO)
```python
test_source_files_not_deleted()
```
- Configura `auto_delete_beats = False`
- Configura `auto_delete_covers = False`
- Ejecuta conversión
- Ejecuta cleanup
- **VERIFICA que los archivos originales aún existen**

### Test de Validación de Negocio
```python
test_validate_config_*()
```
- Valida formato de resolución (WIDTHxHEIGHT)
- Valida FPS positivo
- Valida formato de bitrates (K/M suffix)

## 📊 Reporte de Cobertura

Después de ejecutar los tests con coverage:
```bash
pytest tests/ --cov=ecb_tool.features.conversion --cov-report=html
```

Abrir en navegador:
```
htmlcov/index.html
```

## ✅ Resultados Esperados

Todos los tests deben pasar si:

✓ FFmpeg está instalado y en PATH  
✓ Todos los módulos de Python están instalados  
✓ El convertidor funciona correctamente  
✓ **Los archivos NO se borran cuando auto_delete = False**

## 🐛 Debugging

### FFmpeg no encontrado
```bash
# Windows
where ffmpeg

# Si no está, agregar a PATH o copiar a ffmpeg/bin/
```

### Tests fallan en conversión real
- Verificar que FFmpeg funciona: `ffmpeg -version`
- Revisar permisos de escritura en `workspace/`
- Verificar que hay espacio en disco

### ImportError de pytest
```bash
pip install pytest pytest-cov
```

## 📝 Agregar Nuevos Tests

Estructura de un test:
```python
def test_mi_nuevo_test(conversion_config_no_delete, real_audio_file, real_image_file):
    """Test: Descripción de lo que prueba."""
    # Arrange
    job = ConversionJob(...)
    converter = VideoConverter(conversion_config_no_delete)
    
    # Act
    result = converter.convert(job)
    
    # Assert
    assert result is True
    assert job.status == "completed"
```

## 🎯 Cobertura Objetivo

- **Líneas de código:** >80%
- **Branches:** >70%
- **Funciones:** 100%

## 📞 Soporte

Si algún test falla:
1. Leer el mensaje de error completo
2. Verificar que FFmpeg está instalado
3. Revisar logs en `logs/`
4. Ejecutar test individual con `-vv` para más detalle

---

**¡Happy Testing!** 🧪✨
