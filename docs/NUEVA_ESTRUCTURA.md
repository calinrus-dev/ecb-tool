# ECB Tool - Nueva Estructura Alpha

## 🎯 Estructura Refactorizada (Feature-First)

```
ECB TOOL/
├── ecb_tool/                    # 📦 Main package
│   ├── __init__.py             # Package initialization
│   ├── main.py                 # Application entry point
│   │
│   ├── core/                   # 🔧 Core utilities
│   │   ├── __init__.py
│   │   ├── paths.py           # ✨ Centralized path management
│   │   └── config.py          # Configuration manager
│   │
│   └── features/               # 📁 Feature-based modules
│       ├── conversion/         # Video conversion feature
│       │   ├── __init__.py
│       │   ├── models.py      # Data models
│       │   └── converter.py   # Conversion logic
│       │
│       ├── upload/            # YouTube upload feature
│       │   ├── __init__.py
│       │   ├── models.py      # Data models
│       │   └── uploader.py    # Upload logic
│       │
│       ├── settings/          # Settings management
│       │   ├── __init__.py
│       │   └── manager.py     # Settings manager
│       │
│       └── ui/                # UI components (to be migrated)
│           └── __init__.py
│
├── tests/                      # 🧪 Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── unit/                  # Unit tests
│   │   ├── test_paths.py
│   │   ├── test_config.py
│   │   └── test_conversion.py
│   └── integration/           # Integration tests
│       └── test_conversion_workflow.py
│
├── workspace/                  # 📁 Working directories
│   ├── beats/                 # Audio input files
│   ├── covers/                # Image input files
│   ├── videos/                # Generated videos
│   ├── uploaded/              # Uploaded videos
│   ├── processed/             # Processed files
│   ├── temp/                  # Temporary files
│   └── trash/                 # Deleted files
│
├── config/                     # ⚙️ Configuration files
│   ├── orden.json
│   ├── ajustes_conversion.json
│   ├── ajustes_subida.json
│   └── ...
│
├── data/                       # 📊 Data files
│   ├── titles.txt
│   ├── description.txt
│   ├── conversion_state.csv
│   └── app.log
│
├── pyproject.toml             # 📦 Modern Python project config
├── requirements.txt           # Dependencies (legacy)
├── README.md                  # Documentation
└── main.py                    # Legacy entry point (redirects)
```

## ✨ Mejoras Principales

### 1. **Sistema de Rutas Centralizado**

Antes tenías rutas duplicadas en múltiples archivos. Ahora TODO está en:
```python
from ecb_tool.core.paths import get_paths

paths = get_paths()
print(paths.beats)      # Path to workspace/beats
print(paths.videos)     # Path to workspace/videos
print(paths.app_log)    # Path to data/app.log
```

**Ventajas:**
- ✅ Cambias una carpeta en UN solo lugar
- ✅ No más `os.path.join` por todos lados
- ✅ Type hints completos (IDE autocomplete)
- ✅ Paths como objetos Path (no strings)

### 2. **Arquitectura por Features**

```python
# Antes (mezclado)
from core.converter import ...
from utilities.apply_settings import ...
from shared.paths import ...

# Ahora (organizado por feature)
from ecb_tool.features.conversion import VideoConverter
from ecb_tool.features.upload import VideoUploader
from ecb_tool.features.settings import SettingsManager
```

### 3. **Tests Profesionales**

```bash
# Ejecutar todos los tests
pytest

# Solo unit tests
pytest tests/unit

# Con coverage
pytest --cov=ecb_tool

# Excluir integration tests
pytest -m "not integration"
```

### 4. **Configuración Moderna**

`pyproject.toml` es el estándar moderno de Python (PEP 518):
- Reemplaza setup.py, setup.cfg, requirements.txt
- Configuración de herramientas en un solo lugar
- Compatible con pip, poetry, hatch, etc.

## 🚀 Cómo Usar la Nueva Estructura

### Desarrollo

```bash
# Instalar en modo desarrollo
pip install -e .

# Con dependencias de desarrollo
pip install -e ".[dev]"

# Ejecutar aplicación
python -m ecb_tool.main
# O simplemente:
ecb-tool
```

### Testing

```bash
# Instalar pytest
pip install pytest pytest-qt pytest-cov

# Run tests
pytest

# With coverage report
pytest --cov=ecb_tool --cov-report=html
```

### Imports Limpios

```python
# Core utilities
from ecb_tool.core import get_paths, ConfigManager

# Features
from ecb_tool.features.conversion import VideoConverter, ConversionConfig
from ecb_tool.features.upload import VideoUploader, UploadConfig
from ecb_tool.features.settings import SettingsManager

# Example usage
paths = get_paths()
settings = SettingsManager()

converter = VideoConverter(
    ConversionConfig(
        beats_dir=paths.beats,
        covers_dir=paths.covers,
        videos_dir=paths.videos,
    )
)
```

## 📦 Packages vs Modules

### Package (con `__init__.py`)
- Es una carpeta con `__init__.py`
- Puede importar: `from ecb_tool.features.conversion import ...`
- Exports limpios en `__init__.py`

### Module (archivo .py)
- Es un archivo Python
- Importación: `from ecb_tool.core.paths import ...`

## 🔄 Migración desde Estructura Antigua

### Paths

```python
# ❌ ANTES (duplicado en múltiples archivos)
ROOT_DIR = find_root_dir()
BEATS_DIR = os.path.join(ROOT_DIR, "beats")
VIDEOS_DIR = os.path.join(ROOT_DIR, "videos")

# ✅ AHORA (centralizado)
from ecb_tool.core.paths import get_paths
paths = get_paths()
# paths.beats, paths.videos, etc.
```

### Config

```python
# ❌ ANTES
from utilities.apply_settings import ConfigManager

# ✅ AHORA
from ecb_tool.core.config import ConfigManager
```

### Features

```python
# ❌ ANTES
from core.converter import convert_beat_to_video
from core.uploader import upload_video

# ✅ AHORA
from ecb_tool.features.conversion import VideoConverter
from ecb_tool.features.upload import VideoUploader
```

## 🎨 Convenciones de Nomenclatura

### Archivos y Carpetas
- `snake_case` para archivos: `video_converter.py`
- `lowercase` para packages: `conversion/`, `upload/`

### Código
- `PascalCase` para clases: `VideoConverter`, `UploadConfig`
- `snake_case` para funciones: `get_paths()`, `convert_video()`
- `UPPERCASE` para constantes: `DEFAULT_FPS = 30`

### Variables
- Descriptivas en inglés: `beat_file`, `cover_image`
- No abreviaturas: `configuration` en vez de `cfg`
- Type hints siempre: `def convert(job: ConversionJob) -> bool`

## 🧪 Testing Strategy

### Unit Tests
```python
# tests/unit/test_paths.py
def test_get_project_paths():
    paths = get_project_paths()
    assert paths.root.exists()
    assert paths.beats.name == "beats"
```

### Integration Tests
```python
# tests/integration/test_conversion_workflow.py
@pytest.mark.integration
def test_full_conversion(sample_beat, sample_cover):
    converter = VideoConverter(config)
    result = converter.convert(job)
    assert result is True
```

## 📝 Siguiente Paso

1. Migrar UI components de `ui/` a `ecb_tool/features/ui/`
2. Actualizar imports en archivos legacy
3. Deprecar archivos antiguos gradualmente
4. Agregar más tests

## 🎯 Beneficios de esta Estructura

- ✅ **Mantenible**: Features aislados, fácil de modificar
- ✅ **Testeable**: Tests organizados, fixtures reutilizables  
- ✅ **Escalable**: Agregar features sin romper existentes
- ✅ **Profesional**: Estándar de la industria
- ✅ **Type-safe**: Type hints en todo el código
- ✅ **DRY**: Sin duplicación (especialmente paths)

---

**Versión**: 1.0.0-alpha  
**Fecha**: Enero 2026
