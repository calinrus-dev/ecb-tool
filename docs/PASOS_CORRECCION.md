# 🔧 PASOS INMEDIATOS PARA HACER FUNCIONAR ECB TOOL

## ✅ ERRORES YA CORREGIDOS (hecho por mí)

### 1. ConfigManager.set() AttributeError ✅
- **Archivo:** `ui/blocks/upload_settings_dialog.py` línea 676
- **Archivo:** `ui/blocks/ffmpeg_settings_dialog.py` línea 620
- **Cambio:** `self.config.set()` → `self.config.config[...] = ...; self.config.save()`
- **Estado:** ✅ CORREGIDO

### 2. Archivos data/ vacíos ✅
- **Creado:** `data/titles.txt` con 10 títulos de ejemplo
- **Creado:** `data/description.txt` con template profesional
- **Estado:** ✅ CORREGIDO

---

## 🚨 TAREAS PENDIENTES PARA TI

### ⚠️ CRÍTICO - Hacer AHORA para que funcione

#### **PASO 1: Agregar archivos de prueba (5 minutos)**

```bash
# Necesitas al menos:
# 1. Un archivo de audio en workspace/beats/
# 2. Una imagen en workspace/covers/

# Ejemplo (Windows):
# Copia cualquier MP3 que tengas:
copy "C:\Users\TU_USUARIO\Music\cualquier_cancion.mp3" "workspace\beats\test_beat.mp3"

# Copia cualquier imagen:
copy "C:\Users\TU_USUARIO\Pictures\cualquier_foto.jpg" "workspace\covers\test_cover.jpg"
```

**¿Por qué es crítico?**
- Sin beats → No hay nada que convertir
- Sin covers → No se puede crear video
- Sin archivos → El programa no hace nada visible

---

#### **PASO 2: Verificar/reinstalar dependencias (2 minutos)**

```bash
cd "c:\Users\calin\Desktop\ECB TOOL"
.venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

**Verificar específicamente:**
```bash
pip show google-auth-oauthlib
pip show Pillow
```

Si no aparecen:
```bash
pip install google-auth-oauthlib Pillow
```

---

#### **PASO 3: Probar que funciona (3 minutos)**

```bash
# Ejecutar el programa
.venv\Scripts\python.exe main.py

# Debe abrir una ventana sin errores
```

**En la interfaz:**
1. Verifica que los contadores muestren:
   - Beats: 1 (o más)
   - Covers: 1 (o más)
   
2. Configurar:
   - Modo: **Convert**
   - BPV: **1**
   - Órdenes: **1**
   
3. Click **▶ INICIAR**

4. Esperar 10-30 segundos

5. Verificar `workspace\videos\` - debe tener un archivo `.mp4`

---

### 🟡 IMPORTANTE - Hacer después

#### **PASO 4: Implementar upload real a YouTube**

**Archivo:** `src/application/use_cases.py`

**Línea ~192:**
```python
# TODO: Aquí iría la llamada a YouTube API
```

**Agregar esta función:**

```python
def upload_video_to_youtube(
    video_path: str,
    title: str,
    description: str,
    privacy_status: str = "public",
    category_id: str = "10"  # Music
):
    """
    Sube un video a YouTube usando la API.
    
    Args:
        video_path: Ruta al archivo de video
        title: Título del video
        description: Descripción del video
        privacy_status: "public", "private", o "unlisted"
        category_id: ID de categoría (10 = Music)
    
    Returns:
        dict: Respuesta de la API con ID del video subido
    """
    from utilities.youtube_auth import get_youtube_service
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    import os
    
    # Validar que el archivo existe
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video no encontrado: {video_path}")
    
    # Obtener servicio autenticado
    try:
        youtube = get_youtube_service()
    except Exception as e:
        raise Exception(f"Error de autenticación: {e}")
    
    # Metadata del video
    body = {
        'snippet': {
            'title': title[:100],  # YouTube max 100 chars
            'description': description[:5000],  # Max 5000 chars
            'categoryId': category_id,
            'tags': ['beat', 'instrumental', 'music'],
        },
        'status': {
            'privacyStatus': privacy_status,
            'selfDeclaredMadeForKids': False,
        }
    }
    
    # Preparar upload
    media = MediaFileUpload(
        video_path,
        chunksize=1024*1024,  # 1MB chunks
        resumable=True,
        mimetype='video/mp4'
    )
    
    # Iniciar upload
    try:
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        # Upload con progress tracking
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"Upload: {progress}%")
        
        print(f"✅ Video subido! ID: {response['id']}")
        return response
        
    except HttpError as e:
        raise Exception(f"Error de YouTube API: {e}")
    except Exception as e:
        raise Exception(f"Error inesperado: {e}")
```

**Luego, en `core/uploader.py`, reemplazar el TODO:**

```python
# Línea ~250 (aproximadamente)
def upload_video(video_path, title, description, config):
    """Sube un video a YouTube."""
    
    privacy_map = {
        "publico": "public",
        "privado": "private",
        "no_listado": "unlisted"
    }
    
    privacy = privacy_map.get(
        config.get("estado", "publico"),
        "public"
    )
    
    try:
        # AQUÍ VA LA LLAMADA REAL
        from src.application.use_cases import upload_video_to_youtube
        
        response = upload_video_to_youtube(
            video_path=video_path,
            title=title,
            description=description,
            privacy_status=privacy
        )
        
        return response
        
    except Exception as e:
        print(f"❌ Error subiendo video: {e}")
        raise
```

---

#### **PASO 5: Agregar método set() a ConfigManager**

**Archivo:** `utilities/apply_settings.py`

**Agregar después del método `update()`:**

```python
def set(self, key: str, value: Any) -> None:
    """
    Actualiza una sección completa de configuración y guarda.
    Similar a update() pero para cualquier tipo de valor.
    
    Args:
        key: Clave de primer nivel a actualizar
        value: Nuevo valor (puede ser dict, list, str, etc.)
    
    Example:
        config.set("subida", {"modo": "programado", ...})
    """
    if key in self.schema:
        self.config[key] = value
        self.save()
    else:
        # Permitir claves nuevas pero advertir
        print(f"Warning: Clave '{key}' no está en schema, agregando de todos modos")
        self.config[key] = value
        self.save()
```

**Actualizar `__all__`:**
```python
__all__ = ["ConfigManager"]  # Ya está bien
```

---

#### **PASO 6: Tests básicos**

**Crear:** `tests/test_config_manager.py`

```python
"""Tests para ConfigManager."""
import pytest
import os
import json
import tempfile
from utilities.apply_settings import ConfigManager


def test_config_manager_load():
    """Test de carga de configuración."""
    schema = {"test": {"key": "value"}}
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(schema, f)
        config_path = f.name
    
    try:
        config = ConfigManager(config_path, schema)
        assert config.get("test") == {"key": "value"}
    finally:
        os.unlink(config_path)


def test_config_manager_set():
    """Test del nuevo método set()."""
    schema = {"section": {"old": "value"}}
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(schema, f)
        config_path = f.name
    
    try:
        config = ConfigManager(config_path, schema)
        
        # Probar set()
        new_data = {"new": "data"}
        config.set("section", new_data)
        
        # Verificar
        assert config.get("section") == new_data
        
        # Recargar y verificar persistencia
        config.reload()
        assert config.get("section") == new_data
        
    finally:
        os.unlink(config_path)
```

**Ejecutar:**
```bash
pip install pytest pytest-qt
pytest tests/test_config_manager.py -v
```

---

#### **PASO 7: Limpiar archivos legacy (opcional)**

**Verificar si existen carpetas viejas:**
```bash
dir interfaz\ /s 2>nul
dir nucleo\ /s 2>nul
dir utilidades\ /s 2>nul
```

Si **NO** existen (esperado), entonces son referencias fantasma.

**Limpiar configuración de Pylance:**
1. Cerrar VS Code
2. Eliminar `.vscode/` (si existe)
3. Reabrir VS Code
4. Pylance regenerará el índice

---

## 📋 CHECKLIST FINAL

Marca conforme completes:

### Crítico (para que funcione)
- [ ] Agregar al menos 1 beat en `workspace/beats/`
- [ ] Agregar al menos 1 cover en `workspace/covers/`
- [ ] Verificar dependencias instaladas
- [ ] Probar conversión básica

### Importante (para producción)
- [ ] Implementar upload real a YouTube
- [ ] Agregar método `set()` a ConfigManager
- [ ] Crear tests básicos
- [ ] Limpiar referencias legacy

### Opcional (mejoras)
- [ ] Logging estructurado
- [ ] Type checking con mypy
- [ ] Pre-commit hooks
- [ ] Documentation en código

---

## 🎯 RESULTADO ESPERADO

Después de completar los pasos críticos:

```bash
# 1. Ejecutar
.venv\Scripts\python.exe main.py

# 2. En la interfaz ver:
Beats: 1
Covers: 1
Videos: 0

# 3. Configurar:
Modo: Convert
BPV: 1
Órdenes: 1

# 4. Click INICIAR

# 5. Después de 10-30 segundos:
Beats: 0 (procesado)
Covers: 0 (procesado)
Videos: 1 (generado)

# 6. Verificar archivo:
dir workspace\videos\*.mp4
# Debe mostrar un archivo de video
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### "No se encontró FFmpeg"
```bash
# Verificar:
dir ffmpeg\bin\ffmpeg.exe

# Si existe:
# El programa debería detectarlo automáticamente
# Revisar data/app.log para ver el error específico
```

### "No se pueden convertir videos"
```bash
# Verificar:
1. ¿Hay archivos en workspace/beats/? 
2. ¿Hay archivos en workspace/covers/?
3. ¿FFmpeg existe?
4. Revisar data/conversion_state.csv para errores
```

### "Error al guardar configuración"
```bash
# Ya corregido en esta sesión
# Si persiste, verificar permisos de escritura en config/
```

### "Import error de google_auth_oauthlib"
```bash
pip install google-auth-oauthlib --upgrade
```

---

## 📞 CONTACTO

Si después de seguir estos pasos sigues teniendo problemas:

1. Revisa `data/app.log` - ahí se registran todos los errores
2. Revisa `data/conversion_state.csv` - estado de conversiones
3. Abre un issue en GitHub con:
   - El error específico
   - El contenido de app.log
   - Los pasos que seguiste

---

**¡Con estos pasos tu proyecto debería funcionar perfectamente!** 🚀

Última actualización: 22 de enero de 2026
