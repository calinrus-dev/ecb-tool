# ECB ATOOL 🎵✨

**ECB ATOOL** (El Conde Beats Automated Tool) es una aplicación de escritorio profesional de última generación para la automatización completa del flujo de trabajo musical. Diseñada específicamente para productores, creadores de beats y gestores de contenido musical en YouTube.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.13+-green.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)
![CI/CD](https://github.com/calinrus-dev/ecb-tool/workflows/CI/CD%20Pipeline/badge.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-success.svg)

## ✨ Características Principales

### �️ Arquitectura Modular Profesional
- **Estructura `ecb_tool/`**: Organización clean code con separación de responsabilidades
- **Sistema de Features**: Módulos independientes (conversion, upload, settings, ui)
- **Core Compartido**: Utilidades centralizadas para configuración, paths y validaciones
- **Tests Integrados**: Suite completa de tests unitarios e integración

### 🎨 Interfaz Moderna de Nueva Generación
- **6 Temas Profesionales**: Azul Cian, Rojo Fuego, Verde Neón, Amarillo Solar, Morado Místico, Oscuro Elite
- **3 Idiomas Completos**: Español, English, Français con traducciones nativas
- **Diseño Responsivo Adaptativo**: Escalado automático a cualquier resolución (base 1920x1080)
- **Efectos Visuales Premium**: Animaciones hover, transiciones suaves, feedback visual inmediato
- **Controles Separados**: ConversionControl y UploadControl independientes con estética coherente

### 🔄 Gestión Avanzada de Procesos
- **4 Modos de Operación Inteligentes**:
  - **🎬 Convertir**: Transforma beats en videos profesionales con FFmpeg
  - **📤 Subir**: Automatiza subidas a YouTube con OAuth 2.0
  - **🔀 Alternar**: Alterna dinámicamente entre conversión y subida
  - **⚡ Simultáneo**: Ejecuta ambos procesos en paralelo para máxima eficiencia
- **Control Granular**: Start, pause, resume, stop por proceso individual
- **Recuperación Automática**: Continúa desde el último punto en caso de interrupción

### 📊 Sistema de Cola Inteligente
- Gestión avanzada de tareas con 7 estados diferentes
- Validación automática de recursos (beats, covers, videos, títulos)
- Límites inteligentes basados en archivos disponibles
- Seguimiento en tiempo real del progreso

### 🎯 Validación Inteligente de Recursos
- **Pre-validación de Conversión**: 
  - Verifica beats disponibles en `workspace/beats/`
  - Valida covers en `workspace/covers/` o `workspace/covers/images/`
  - Comprueba espacio en disco
  - Valida codecs FFmpeg
- **Pre-validación de Subida**: 
  - Valida videos procesados en `workspace/videos/`
  - Comprueba títulos en `data/titles.txt`
  - Verifica descripción en `data/description.txt`
  - Valida autenticación OAuth
- **Cálculo Dinámico**: 
  - Máximo de órdenes = min(beats disponibles / BPV, títulos disponibles)
  - Ajuste automático según recursos más limitados
  - Alertas tempranas de recursos insuficientes

### 📈 Panel de Estado Reactivo
- Barras de progreso que aparecen/desaparecen dinámicamente
- Archivos completados en gris con indicador verde
- Procesos activos resaltados en blanco
- Auto-scroll para nuevas tareas
- Indicadores visuales: ✓ (completado), barra animada (procesando), ✗ (error)

### 🎭 Modos Avanzados de Cover
- **🎲 Random**: Selección completamente aleatoria con posibilidad de repetición
- **🔄 Random (No Repeat)**: Algoritmo inteligente que evita repeticiones hasta agotar todas las opciones
- **🎯 Select One**: Selecciona y usa una cover específica para todos los videos
- **📊 Sequential**: Procesa covers en orden alfabético secuencial

### 🔐 Sistema OAuth 2.0 Integrado
- **Autenticación Segura**: Sign-in con Google OAuth 2.0
- **Dialog Dedicado**: Interfaz visual para gestionar credenciales
- **Estado Persistente**: Mantiene sesión entre reinicios
- **Renovación Automática**: Refresh tokens sin intervención manual

### 📅 Programación Inteligente de Subidas
- **Calendario Visual**: Selector de fechas con vista mensual
- **Horarios Flexibles**: Configuración de hora exacta de publicación
- **Múltiples Programaciones**: Agenda varios videos a diferentes horarios
- **Validación Temporal**: Previene programar en fechas pasadas
- **Confirmación Pre-subida**: Dialog de revisión con todos los detalles

## 🚀 Instalación Rápida

### Requisitos del Sistema

| Componente | Versión Mínima | Recomendado |
|------------|----------------|-------------|
| Python | 3.13.0 | 3.13.5+ |
| Sistema Operativo | Windows 10 | Windows 11 |
| RAM | 4 GB | 8 GB+ |
| Espacio en Disco | 2 GB | 10 GB+ |
| FFmpeg | 4.0+ | Última versión |

### Instalación Automática (Recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/calinrus-dev/ecb-tool.git
cd ecb-tool

# 2. Ejecutar script de instalación automático
install_dependencies.bat

# 3. (Opcional) Instalar dependencias de YouTube
install_youtube_deps.bat

# 4. Iniciar la aplicación
start.bat
```

### Instalación Manual

```bash
# 1. Clonar repositorio
git clone https://github.com/calinrus-dev/ecb-tool.git
cd ecb-tool

# 2. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate

# 3. Actualizar pip
python -m pip install --upgrade pip

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Verificar instalación
python -c "import PyQt6; print('PyQt6 OK')"

# 6. Ejecutar aplicación
python ecb_tool/main.py
```

### Configuración de FFmpeg

ECB ATOOL incluye FFmpeg preconfigurado en `ffmpeg/bin/`. Si necesitas actualizar:

1. Descargar FFmpeg desde [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extraer en carpeta `ffmpeg/bin/`
3. Verificar instalación:
   ```bash
   ffmpeg\bin\ffmpeg.exe -version
   ```

### Configuración OAuth (Para Subidas a YouTube)

1. Acceder a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear nuevo proyecto o seleccionar existente
3. Habilitar **YouTube Data API v3**
4. Crear credenciales OAuth 2.0:
   - Tipo: Aplicación de escritorio
   - Descargar JSON de credenciales
5. Renombrar a `client_secrets.json`
6. Colocar en carpeta `oauth/`
7. Al ejecutar por primera vez, se abrirá navegador para autorizar

> ⚠️ **Importante**: El archivo `client_secrets.json` contiene información sensible y **NO debe compartirse** ni subirse a repositorios públicos.

## 📁 Estructura del Proyecto

```
ECB ATOOL/
├── ecb_tool/                     # Paquete principal de la aplicación
│   ├── __init__.py
│   ├── main.py                  # Punto de entrada de la aplicación
│   ├── core/                    # Núcleo de la aplicación
│   │   ├── config.py            # Gestor de configuración
│   │   ├── paths.py             # Gestión centralizada de rutas
│   │   ├── legacy.py            # Compatibilidad con versiones anteriores
│   │   └── shared/              # Utilidades compartidas
│   │       ├── screen_utils.py  # Adaptación de resolución
│   │       ├── theme_manager.py # Gestor de temas visuales
│   │       ├── navigation.py    # Sistema de navegación entre pantallas
│   │       ├── language_manager.py # Sistema multidioma
│   │       ├── queue_manager.py # Gestor de colas de tareas
│   │       ├── file_validator.py # Validación de recursos
│   │       └── validators.py    # Validadores generales
│   ├── features/                # Módulos de funcionalidad
│   │   ├── conversion/          # Módulo de conversión
│   │   │   ├── converter.py     # Motor de conversión FFmpeg
│   │   │   ├── models.py        # Modelos de datos
│   │   │   └── runner.py        # Ejecutor de conversiones
│   │   ├── upload/              # Módulo de subida
│   │   │   ├── uploader.py      # Motor de subida YouTube
│   │   │   └── models.py        # Modelos de subida
│   │   ├── settings/            # Módulo de configuraciones
│   │   │   └── manager.py       # Gestor de ajustes
│   │   └── ui/                  # Interfaz de usuario
│   │       ├── main_window.py   # Ventana principal
│   │       ├── blocks/          # Componentes grandes
│   │       │   ├── conversion_control.py  # Control de conversión
│   │       │   ├── upload_control.py      # Control de subida
│   │       │   ├── counter_widget.py      # Widget contador
│   │       │   ├── counters_panel.py      # Panel de contadores
│   │       │   ├── modules_panel.py       # Panel de módulos
│   │       │   ├── status_panel.py        # Panel de estado
│   │       │   ├── top_bar.py             # Barra superior
│   │       │   ├── oauth_dialog.py        # Dialog OAuth
│   │       │   ├── upload_settings_dialog_v2.py  # Configuración subida V2
│   │       │   └── upload_confirmation_dialog.py # Confirmación subida
│   │       ├── pieces/          # Componentes pequeños
│   │       │   ├── progress_bar.py
│   │       │   ├── blink_animator.py
│   │       │   ├── buttons.py
│   │       │   ├── text.py
│   │       │   └── svg/             # Iconos SVG
│   │       ├── screens/         # Pantallas principales
│   │       │   ├── home_screen.py
│   │       │   ├── general_settings_screen.py
│   │       │   ├── ffmpeg_settings_screen.py
│   │       │   └── upload_settings_screen.py
│   │       └── legacy_src/      # Código legacy (compatibilidad)
│   └── workspace/               # Área de trabajo (ignorado en git)
│       ├── beats/               # Beats de entrada (.mp3, .wav)
│       ├── covers/              # Portadas (.jpg, .png)
│       ├── videos/              # Videos generados (.mp4)
│       ├── processed/           # Archivos ya procesados
│       ├── temp/                # Archivos temporales
│       ├── trash/               # Papelera de reciclaje
│       └── uploaded/            # Videos ya subidos
├── config/                      # Configuraciones JSON
│   ├── ajustes_conversion.json  # Parámetros de conversión
│   ├── ajustes_subida.json      # Parámetros de subida
│   ├── nombres.json             # Nombres personalizados
│   ├── orden.json               # Orden de procesamiento
│   ├── rutas.json               # Rutas configurables
│   ├── theme.json               # Tema seleccionado
│   └── language.json            # Idioma seleccionado
├── data/                        # Datos de la aplicación
│   ├── titles.txt               # Títulos para videos (uno por línea)
│   ├── description.txt          # Descripción para videos
│   ├── conversion_state.csv     # Estado de conversiones
│   └── upload_state.csv         # Estado de subidas
├── tests/                       # Suite de tests
│   ├── unit/                    # Tests unitarios
│   ├── integration/             # Tests de integración
│   └── conftest.py              # Configuración pytest
├── docs/                        # Documentación completa
│   ├── ARCHITECTURE.md          # Arquitectura del sistema
│   ├── QUICKSTART.md            # Guía rápida
│   ├── YOUTUBE_SETUP.md         # Setup OAuth YouTube
│   └── CHANGELOG.md             # Historial de cambios
├── scripts/                     # Scripts de utilidad
│   ├── auto_backup.py           # Backup automático
│   ├── auto_cleanup.py          # Limpieza automática
│   └── auto_update_titles.py    # Actualización de títulos
├── ffmpeg/                      # FFmpeg (excluido de git)
│   ├── bin/                     # Binarios FFmpeg
│   ├── doc/                     # Documentación FFmpeg
│   └── presets/                 # Presets de conversión
├── oauth/                       # Credenciales OAuth (NO VERSIONADO)
│   └── client_secrets.json      # Credenciales Google API
├── logs/                        # Logs de la aplicación
├── .gitignore                   # Archivos ignorados por git
├── requirements.txt             # Dependencias Python
├── pyproject.toml               # Configuración del proyecto
├── pytest.ini                   # Configuración pytest
├── install_dependencies.bat     # Script instalación automática
├── install_youtube_deps.bat     # Script instalación YouTube API
├── start.bat                    # Iniciar aplicación
├── run.bat                      # Ejecutar con venv activado
├── LICENSE                      # Licencia MIT
└── README.md                    # Este archivo
```

## 🎮 Uso

### Flujo de Trabajo Básico

1. **Preparar Recursos**
   - Colocar beats en `workspace/beats/`
   - Colocar covers en `workspace/covers/`
   - Añadir títulos en `data/titles.txt` (uno por línea)
   - Escribir descripción en `data/description.txt`

2. **Configurar Parámetros**
   - Seleccionar modo de operación
   - Ajustar número de órdenes
   - Configurar BPV (Beats Por Video)
   - Elegir modo de cover

3. **Ejecutar Proceso**
   - Verificar contadores (beats, covers, videos, títulos)
   - Presionar botón EJECUTAR
   - Monitorear progreso en panel de estado

4. **Revisar Resultados**
   - Videos en `workspace/videos/`
   - Archivos procesados en `workspace/procesed/`
   - Logs en `logs/`

### Atajos de Teclado

- **ESC**: Cerrar pantallas de configuración (bloqueado en pantalla principal)
- **Menú**: Acceso rápido a todas las configuraciones

## ⚙️ Configuración

### Temas
Acceder desde `Menú → Ajustes Generales → Tema`
- 6 temas preconfigurados
- Cambio instantáneo sin reiniciar

### Idiomas
Acceder desde `Menú → Ajustes Generales → Idioma`
- Español (predeterminado)
- English
- Français
- Actualización automática de toda la UI

### Conversión FFmpeg
Acceder desde `Menú → Ajustes de Conversión`
- Codec de video
- Bitrate
- Resolución
- FPS
- Filtros personalizados

### Subida a YouTube
Acceder desde `Menú → Ajustes de Subida`
- Configuración de privacidad
- Tags automáticos
- Calendario de subidas programadas
- Configuración de OAuth

## 🔧 Tecnologías Utilizadas

- **PyQt6**: Framework de interfaz gráfica
- **FFmpeg**: Procesamiento de video/audio
- **Google API**: Integración con YouTube
- **Python 3.13**: Lenguaje base
- **CSV**: Almacenamiento de estado
- **JSON**: Configuración persistente

## 🎨 Sistema de Temas

Los temas incluyen:
- **Azul**: Tema principal, colores cian y azul
- **Rojo**: Tonos cálidos rojos
- **Verde**: Tonos naturales verdes
- **Amarillo**: Tonos energéticos amarillos
- **Morado**: Tonos místicos morados
- **Oscuro**: Tema minimalista en escala de grises

## 🌍 Sistema Multiidioma

Traducciones completas para:
- Interfaz principal (módulos, botones, labels)
- Modos de operación
- Mensajes de estado
- Configuraciones
- Menús y diálogos

## 📊 Sistema de Cola

Estados de tareas:
- **waiting**: En espera
- **ready**: Listo para ejecutar
- **running**: En ejecución
- **paused**: Pausado
- **completed**: Completado exitosamente
- **error**: Error en procesamiento
- **missing_files**: Archivos faltantes

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verificar instalación de Python 3.13+
- Comprobar todas las dependencias: `pip install -r requirements.txt`
- Revisar logs en carpeta `logs/`

### No se pueden convertir videos
- Verificar instalación de FFmpeg
- Comprobar rutas en `config/rutas.json`
- Asegurar beats y covers disponibles

### Error en subida a YouTube
- Verificar `oauth/client_secrets.json`
- Renovar credenciales OAuth
- Comprobar conexión a internet

### Interfaz se ve mal
- Ajustar resolución de pantalla
- Cambiar escala en `shared/screen_utils.py`
- Probar diferentes temas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👤 Autor

**Calin Rus - El Conde Beats**

- Instagram: [@c4linrus](https://www.instagram.com/c4linrus)
- YouTube: [El Conde Beats](https://youtube.com/@elcondebeats)
- Email: calinrus@gmail.com

## 🙏 Agradecimientos

- Comunidad de PyQt6
- FFmpeg Team
- Todos los contribuidores

## 📅 Roadmap

- [ ] Módulo Generador (IA para crear beats)
- [ ] Soporte para más plataformas (TikTok, Instagram)
- [ ] Editor de thumbnails integrado
- [ ] Sistema de plantillas
- [ ] Análisis de métricas
- [ ] Modo oscuro automático
- [ ] Exportación de reportes
- [ ] Sistema de plugins

---

**Versión**: 1.0.0  
**Última actualización**: Enero 2026  
**Estado**: Activo

Si encuentras útil este proyecto, ¡dale una ⭐ en GitHub!
