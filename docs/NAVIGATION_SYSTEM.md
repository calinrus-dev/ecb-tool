# Sistema de Navegación y Temas

## Arquitectura

La aplicación ahora utiliza un sistema de navegación basado en pantallas (screens) en lugar de diálogos emergentes. Todos los ajustes y configuraciones se muestran integrados en la ventana principal.

### Componentes Principales

#### 1. NavigationManager (`shared/navigation.py`)
- Gestiona el stack de navegación con historial
- Permite navegar entre pantallas: `navigate('screen_name')`
- Permite volver atrás: `back()`
- Emite señal `navigate_to` cuando cambia la pantalla

#### 2. ThemeManager (`shared/theme_manager.py`)
- Gestiona 6 temas de colores:
  - **Azul** (defecto)
  - **Rojo**
  - **Verde**
  - **Amarillo**
  - **Morado**
  - **Oscuro**

Cada tema incluye:
- `primary`, `primary_hover` - Colores principales
- `secondary` - Color secundario
- `accent` - Color de acento
- `success` - Color de éxito
- `background` - Fondo general
- `surface`, `surface_dark` - Superficies
- `border` - Bordes
- `text`, `text_secondary` - Texto
- `topbar` - Barra superior

Los temas se guardan en `config/theme.json`

#### 3. ScreenAdapter (`shared/screen_utils.py`)
- Adaptación automática a cualquier resolución
- Resolución base: 1920x1080
- Factor de escala: 0.6 - 2.0
- Funciones:
  - `scale(value)` - Escala un valor
  - `get_font_size(base_size)` - Tamaño de fuente adaptado
  - `get_spacing(base)` - Espaciado adaptado
  - `get_margin(base)` - Márgenes adaptados
  - `get_main_window_size()` - Tamaño de ventana principal
  - `get_dialog_size(w, h)` - Tamaño de diálogo adaptado

### Pantallas Disponibles

#### Home (`ui/screens/home_screen.py`)
Pantalla principal con:
- Panel de módulos (conversión/upload)
- Panel de contadores
- Panel de estado

#### General Settings (`ui/screens/general_settings_screen.py`)
Configuración general de la aplicación:
- Selector de temas (grid de 6 botones)
- Configuraciones futuras

#### FFMPEG Settings (`ui/screens/ffmpeg_settings_screen.py`)
Configuración de conversión de videos:
- Reutiliza `FFmpegSettingsDialog` como widget embebido
- Botón "Volver" para regresar

#### Upload Settings (`ui/screens/upload_settings_screen.py`)
Configuración de uploads:
- Reutiliza `UploadSettingsDialog` como widget embebido
- Calendario de programación
- Configuración de hora de subida
- Botón "Volver" para regresar

### Flujo de Navegación

```
Home (pantalla inicial)
  │
  ├─→ General Settings (Config General en menú)
  │     │
  │     └─→ Seleccionar tema → Aplicar → Volver
  │
  ├─→ FFMPEG Settings (Config Avanzada en menú)
  │     │
  │     └─→ Configurar → Aceptar → Volver
  │
  └─→ Upload Settings (Config Subida en menú)
        │
        └─→ Configurar calendario → Aceptar → Volver
```

### Implementación en MainWindow

```python
# QStackedWidget para contener todas las pantallas
self.screen_stack = QStackedWidget()

# Diccionario de pantallas
self.screens = {
    'home': HomeScreen(),
    'general_settings': GeneralSettingsScreen(),
    'ffmpeg_settings': FFmpegSettingsScreen(),
    'upload_settings': UploadSettingsScreen()
}

# Navegación
self.navigation.navigate('home')  # Pantalla inicial
self.navigation.navigate_to.connect(self._on_navigate)
```

### Características

✅ **Navegación integrada** - Todo en la ventana principal  
✅ **Historial de navegación** - Botón "Volver" funcional  
✅ **6 temas de colores** - Cambio en tiempo real  
✅ **Adaptación a resoluciones** - Escala automática  
✅ **Smooth scrolling** - Desplazamiento suave  
✅ **Persistencia** - Tema guardado en JSON  

### Uso del Sistema

#### Para navegar a una pantalla:
```python
from shared.navigation import get_navigation_manager

navigation = get_navigation_manager()
navigation.navigate('general_settings')
```

#### Para cambiar el tema:
```python
from shared.theme_manager import get_theme_manager

theme_manager = get_theme_manager()
theme_manager.set_theme('rojo')  # azul, rojo, verde, amarillo, morado, oscuro
```

#### Para adaptar tamaños:
```python
from shared.screen_utils import get_screen_adapter

adapter = get_screen_adapter()
width = adapter.scale(300)
font_size = adapter.get_font_size(16)
```

#### Para reaccionar a cambios de tema:
```python
def _apply_theme(self):
    theme = self.theme_manager.get_current_theme()
    self.setStyleSheet(f"background: {theme['background']};")

self.theme_manager.theme_changed.connect(self._apply_theme)
```
