# ECB TOOL - Arquitectura del Proyecto

## 🏗️ Patrón Arquitectónico: Clean Architecture Simplificada

### Estructura de Capas

```
ECB TOOL/
│
├── main.py                    # Entry point único
├── shared/                    # ⚙️ Infraestructura compartida
│   ├── paths.py              # Gestión centralizada de rutas
│   └── validators.py         # Validación de configuraciones
│
├── core/                      # 💼 Lógica de negocio central
│   ├── core.py               # Orquestador principal + StateManager
│   ├── converter.py          # Conversión de videos (FFmpeg)
│   └── uploader.py           # Subida de videos
│
├── src/                       # 📦 Arquitectura en capas
│   ├── domain/               # Entidades y modelos (futuro)
│   ├── application/          # Casos de uso
│   │   └── process_controller.py
│   ├── infrastructure/       # Servicios externos (futuro: YouTube API)
│   └── presentation/         # Capa de presentación
│       ├── main_window.py
│       └── widgets/          # Wrappers para UI components
│
├── ui/                        # 🎨 Componentes UI reutilizables
│   ├── blocks/               # Componentes compuestos (paneles, módulos)
│   │   ├── modules_panel.py
│   │   ├── status_panel.py
│   │   ├── counters_panel.py
│   │   ├── counter_widget.py
│   │   └── top_bar.py
│   └── pieces/               # Componentes atómicos (botones, texto)
│       ├── text.py
│       ├── buttons.py
│       └── svg/              # Iconos vectoriales
│
├── utilities/                 # 🔧 Utilidades
│   ├── apply_settings.py     # ConfigManager
│   └── ffmpeg_paths.py       # Gestión de rutas FFmpeg
│
├── config/                    # ⚙️ Archivos de configuración
│   ├── ajustes_conversion.json
│   ├── ajustes_subida.json
│   └── orden.json
│
├── data/                      # 📊 Datos de estado
│   ├── conversion_state.csv
│   └── upload_state.csv
│
└── workspace/                 # 📁 Archivos de trabajo
    ├── beats/                # Audios fuente
    ├── covers/               # Imágenes de portada
    ├── videos/               # Videos generados
    └── uploaded/             # Videos subidos
```

## 📐 Principios de Diseño

### 1. **Separación de Responsabilidades**

#### Capa de Presentación (`src/presentation/`)
- **Responsabilidad**: Interfaz de usuario, eventos, widgets
- **Dependencias**: Puede importar de `ui/` y `src/application/`
- **No debe**: Contener lógica de negocio

#### Capa de Aplicación (`src/application/`)
- **Responsabilidad**: Casos de uso, orquestación de procesos
- **Ejemplo**: `ProcessController` coordina inicio/parada de procesos
- **Dependencias**: Puede importar de `core/` y `shared/`

#### Capa Core (`core/`)
- **Responsabilidad**: Lógica de negocio central
- **Componentes**:
  - `StateManager`: Gestión de estado global con señales PyQt6
  - `converter.py`: Conversión de videos con FFmpeg
  - `uploader.py`: Gestión de carga de videos
  - `core.py`: Orquestador de procesos

#### Componentes UI (`ui/`)
- **Responsabilidad**: Widgets reutilizables sin lógica de negocio
- **Patrón**: Componentes puros que reciben datos y emiten eventos
- **Organización**:
  - `blocks/`: Componentes compuestos (paneles, módulos)
  - `pieces/`: Componentes atómicos (texto, botones, iconos)

#### Shared (`shared/`)
- **Responsabilidad**: Infraestructura común
- **Componentes**:
  - `paths.py`: Gestión centralizada de rutas del proyecto
  - `validators.py`: Validación de configuraciones JSON

### 2. **Flujo de Dependencias**

```
Presentación (src/presentation/)
    ↓ usa
Aplicación (src/application/)
    ↓ usa
Core (core/) + UI Components (ui/)
    ↓ usa
Shared (shared/) + Utilities (utilities/)
```

**Regla de oro**: Las capas superiores pueden depender de las inferiores, nunca al revés.

### 3. **Comunicación entre Capas**

#### Señales PyQt6 (Observer Pattern)
```python
# core/core.py
class StateManager(QObject):
    mode_changed = pyqtSignal(str)
    action_requested = pyqtSignal(str)
```

#### Controladores (Command Pattern)
```python
# src/application/process_controller.py
class ProcessController:
    def start(self, mode: str) -> None
    def stop(self) -> None
```

## 🔄 Flujo de Ejecución

### Inicio de la Aplicación

1. **main.py**
   - Configura entorno (FFmpeg, logging)
   - Valida entorno virtual
   - Importa y lanza `MainWindow`

2. **MainWindow** (`src/presentation/main_window.py`)
   - Construye interfaz usando componentes de `ui/blocks/`
   - Conecta señales de `StateManager`

3. **Usuario presiona RUN**
   - `ModulesPanel` → `ProcessController.start(mode)`
   - `ProcessController` → actualiza `orden.json` + lanza `core.py` subprocess

4. **Conversión de Video**
   - `core.py` lee modo → ejecuta `converter.py`
   - `converter.py` usa FFmpeg → genera video
   - Estado se guarda en CSV

## 📝 Convenciones de Código

### Nombres de Archivos
- **Clases**: `PascalCase` → `ModulesPanel`
- **Funciones**: `snake_case` → `load_config()`
- **Archivos**: `snake_case.py` → `process_controller.py`

### Imports
```python
# Absolutos desde raíz del proyecto
from shared.paths import ROOT_DIR
from core.core import StateManager
from ui.blocks.modules_panel import ModulesPanel

# Relativos solo dentro del mismo paquete
from .counter_widget import CounterWidget
```

### Documentación
```python
def function_name(param: Type) -> ReturnType:
    """
    Descripción breve de una línea.
    
    Args:
        param: Descripción del parámetro
    
    Returns:
        Descripción del retorno
    
    Raises:
        ExceptionType: Cuándo se lanza
    """
    pass
```

## 🎯 Patrones de Diseño Utilizados

1. **Singleton**: `StateManager` (instancia única de estado global)
2. **Observer**: Señales PyQt6 para comunicación desacoplada
3. **Command**: `ProcessController` encapsula acciones
4. **Factory**: Funciones `title_text()`, `header_text()` en `ui/pieces/text.py`
5. **Repository**: `ConfigManager` abstrae acceso a configuraciones

## 🚀 Ventajas de Esta Arquitectura

✅ **Testeable**: Cada capa puede probarse independientemente
✅ **Mantenible**: Cambios en UI no afectan lógica de negocio
✅ **Escalable**: Fácil añadir nuevas features
✅ **Clara**: Responsabilidades bien definidas
✅ **Reutilizable**: Componentes UI pueden usarse en otros proyectos

## 📌 Próximas Mejoras

1. **Implementar capa Domain**
   - Entidades: `Video`, `Beat`, `Cover`
   - Value Objects: `VideoConfig`, `UploadConfig`

2. **Implementar capa Infrastructure**
   - `YouTubeService`: Integración con YouTube API
   - `FFmpegService`: Abstracción de FFmpeg

3. **Añadir Tests**
   - `tests/unit/`: Tests unitarios por capa
   - `tests/integration/`: Tests de integración
   - `tests/e2e/`: Tests end-to-end

4. **Dependency Injection**
   - Contenedor de dependencias para desacoplar aún más

## 🔗 Referencias

- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [FFmpeg Python](https://github.com/kkroening/ffmpeg-python)
