# Arquitectura ECB TOOL v2.0

## 🎯 Principio Fundamental

**CERO DEPENDENCIAS DE ALPHA/**

La nueva versión es 100% autónoma. El folder `alpha/` es solo backup histórico.

## 📁 Estructura

```
ecb_tool/
├── core/
│   ├── config.py          # ConfigManager (settings JSON)
│   ├── paths.py           # ProjectPaths (todos los paths del proyecto)
│   ├── legacy.py          # StateManager (compatibilidad con core antiguo)
│   └── shared/            # Utilidades compartidas
│       ├── theme_manager.py    # 6 temas con estilos completos
│       ├── screen_utils.py     # Adaptación de pantalla
│       ├── navigation.py       # Sistema de navegación
│       ├── paths.py            # Paths legacy
│       └── validators.py       # Validaciones
│
├── features/
│   ├── conversion/        # Feature de conversión de videos
│   ├── upload/            # Feature de subida a YouTube
│   └── ui/                # Feature de interfaz gráfica
│       ├── blocks/        # Componentes UI medianos (paneles)
│       ├── pieces/        # Componentes UI pequeños (botones, texto)
│       │   └── svg/       # ✨ ASSETS: Iconos SVG
│       ├── screens/       # Pantallas completas
│       └── legacy_src/    # Lógica de dominio/aplicación
│           ├── domain/
│           ├── application/
│           ├── infrastructure/
│           └── presentation/
│
└── main.py                # Entry point
```

## 🔄 Sistema de Imports

### ✅ CORRECTO

```python
from ecb_tool.core.config import ConfigManager
from ecb_tool.core.paths import get_paths
from ecb_tool.core.shared.theme_manager import get_theme_manager
from ecb_tool.features.ui.blocks.modules_panel import ModulesPanel
from ecb_tool.features.ui.pieces.buttons import icon_button
```

### ❌ INCORRECTO (dependencias de alpha/)

```python
from shared.theme_manager import ...  # ❌
from ui.blocks.modules_panel import ... # ❌
from src.domain.entities import ...     # ❌
from core.core import StateManager      # ❌
```

## 🎨 Sistema de Temas

6 temas completos con:
- Colores base
- Gradientes
- Estilos de hover
- Estilos de scroll (barras personalizadas)
- Estilos de botones
- Transiciones

**Archivo**: `ecb_tool/core/shared/theme_manager.py`

Temas: `azul`, `rojo`, `verde`, `amarillo`, `morado`, `oscuro`

## 🖼️ Sistema de Assets

SVGs ubicados en: `ecb_tool/features/ui/pieces/svg/`

Archivos:
- `archivo.svg` - Icono de archivo
- `carpeta.svg` - Icono de carpeta
- `check.svg` - Checkmark
- `modulo_activo.svg` - Módulo en ejecución
- `modulo_seleccionado.svg` - Módulo seleccionado
- `papelera.svg` - Icono de papelera
- `x.svg` - Icono de cerrar

## 🔧 Configuración

Todos los JSON de configuración están en `config/`:
- `ajustes_conversion.json`
- `ajustes_subida.json`
- `language.json`
- `nombres.json`
- `orden.json`
- `rutas.json`
- `theme.json`

Acceso mediante:
```python
from ecb_tool.core.config import ConfigManager
config = ConfigManager()
valor = config.get('ajustes_conversion', 'clave')
```

## 📦 Paths

Sistema centralizado en `ecb_tool/core/paths.py`:

```python
from ecb_tool.core.paths import get_paths
paths = get_paths()

# Ejemplos
paths.root              # Raíz del proyecto
paths.workspace_videos  # Carpeta de videos
paths.ffmpeg_bin        # Ejecutable de FFmpeg
paths.config_theme      # JSON de tema
```

## 🚀 Entry Point

Archivo: `ecb_tool/main.py`

```python
from ecb_tool.features.ui import MainWindow
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
```

## 📝 Notas de Migración

1. **Todos los imports actualizados**: Los archivos en `ecb_tool/features/ui/` ya NO importan de `alpha/`
2. **Assets copiados**: SVGs están en `ecb_tool/features/ui/pieces/svg/`
3. **Shared completo**: Todo `shared/` está en `ecb_tool/core/shared/`
4. **Temas funcionando**: Sistema completo de theming con hover/scroll
5. **Config unificado**: ConfigManager en `ecb_tool/core/config.py`

## ⚠️ Regla de Oro

**NUNCA agregar `import` de `alpha/` en archivos de `ecb_tool/`**

Si necesitas algo de alpha/, primero **copialo** a ecb_tool/ y **actualiza los imports**.

## 🎯 Testing

```bash
# Test de import
python -c "from ecb_tool.features.ui import MainWindow; print('✓ OK')"

# Test de ejecución
python -m ecb_tool.main

# Tests unitarios
pytest tests/
```

---

**Fecha**: 22 de enero de 2026  
**Versión**: 2.0 - Arquitectura Feature-First Autónoma
