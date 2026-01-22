# Guía Rápida de Migración

## 🔄 Pasos para Migrar a la Nueva Estructura

### 1. Actualizar Imports

Busca y reemplaza en todos tus archivos:

```python
# ❌ OLD
from shared.paths import ROOT_DIR, CONFIG_DIR, DATA_DIR
from utilities.apply_settings import ConfigManager
from core.converter import ...

# ✅ NEW
from ecb_tool.core.paths import get_paths
from ecb_tool.core.config import ConfigManager
from ecb_tool.features.conversion import VideoConverter
```

### 2. Usar get_paths() Singleton

```python
# ❌ OLD
ROOT_DIR = find_root_dir()
BEATS_DIR = os.path.join(ROOT_DIR, "beats")

# ✅ NEW
from ecb_tool.core.paths import get_paths
paths = get_paths()
# Acceso directo: paths.beats, paths.videos, etc.
```

### 3. Ejecutar Tests

```bash
# Instalar pytest
pip install pytest pytest-qt

# Ejecutar tests
pytest tests/

# Con coverage
pytest --cov=ecb_tool
```

### 4. Actualizar UI (Próximamente)

Los componentes UI se migrarán gradualmente a `ecb_tool/features/ui/`

## 📋 Checklist

- [ ] Actualizar imports en archivos existentes
- [ ] Probar que la aplicación arranca: `python main_new.py`
- [ ] Ejecutar tests: `pytest`
- [ ] Migrar configuraciones personalizadas
- [ ] Actualizar documentación local

## 🆘 Problemas Comunes

### "ModuleNotFoundError: No module named 'ecb_tool'"

```bash
# Asegúrate de estar en el directorio raíz
cd "C:\Users\calin\Desktop\ECB TOOL"

# Reinstala en modo desarrollo
pip install -e .
```

### "Paths no encontrados"

La nueva estructura usa `pathlib.Path` en vez de strings:

```python
# ❌ Mal
beat_path = str(paths.beats) + "/beat.mp3"

# ✅ Bien
beat_path = paths.beats / "beat.mp3"
```

### Tests fallan

```bash
# Verifica que estás usando el venv correcto
.venv\Scripts\activate

# Reinstala dependencias de test
pip install pytest pytest-qt pytest-cov
```

## 🎯 Siguiente: Migrar UI

1. Mover `ui/` a `ecb_tool/features/ui/`
2. Actualizar imports en screens y components
3. Mantener compatibilidad con main.py legacy

---

¿Dudas? Revisa `NUEVA_ESTRUCTURA.md` para detalles completos.
