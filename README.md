# ECB TOOL 🎵

**ECB TOOL** es una aplicación de escritorio profesional para la gestión automatizada de contenido musical, diseñada específicamente para productores y creadores de beats. Permite convertir, procesar y subir contenido de manera eficiente con una interfaz moderna e intuitiva.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.13+-green.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)
![CI/CD](https://github.com/calinrus-dev/ecb-tool/workflows/CI/CD%20Pipeline/badge.svg)
![Downloads](https://img.shields.io/badge/downloads-0-blue.svg)

## ✨ Características Principales

### 🎨 Interfaz Moderna
- **6 Temas de Color**: Azul, Rojo, Verde, Amarillo, Morado, Oscuro
- **3 Idiomas**: Español, English, Français
- **Diseño Responsivo**: Adaptación automática a diferentes resoluciones (base 1920x1080)
- **Efectos Visuales**: Hover animado, transiciones suaves, feedback visual inmediato

### 🔄 Gestión de Procesos
- **4 Modos de Operación**:
  - Convertir: Procesa beats a videos
  - Subir: Sube videos a plataformas
  - Alternar: Alterna entre conversión y subida
  - Simultáneo: Ejecuta ambos procesos en paralelo

### 📊 Sistema de Cola Inteligente
- Gestión avanzada de tareas con 7 estados diferentes
- Validación automática de recursos (beats, covers, videos, títulos)
- Límites inteligentes basados en archivos disponibles
- Seguimiento en tiempo real del progreso

### 🎯 Validación de Recursos
- **Para Conversión**: Verifica beats y covers disponibles
- **Para Subida**: Valida videos, títulos y descripción
- **Cálculo Automático**: 
  - Máximo de órdenes = beats disponibles / BPV
  - Ajuste dinámico según recursos

### 📈 Panel de Estado Reactivo
- Barras de progreso que aparecen/desaparecen dinámicamente
- Archivos completados en gris con indicador verde
- Procesos activos resaltados en blanco
- Auto-scroll para nuevas tareas
- Indicadores visuales: ✓ (completado), barra animada (procesando), ✗ (error)

### 🎭 Modos de Cover
- Random: Selección aleatoria con repetición
- Random (No Repeat): Sin repetir hasta agotar opciones
- Select One: Usar una cover específica
- Sequential: Orden secuencial

## 🚀 Instalación

### Requisitos Previos
- Python 3.13 o superior
- FFmpeg instalado y configurado
- Windows 10/11 (optimizado para Windows)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/ecb-tool.git
cd ecb-tool
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar OAuth** (para funcionalidad de subida)
   - Obtener credenciales de la API de YouTube
   - Colocar `client_secrets.json` en la carpeta `oauth/`

5. **Ejecutar la aplicación**
```bash
python main.py
```

## 📁 Estructura del Proyecto

```
ECB TOOL/
├── config/                  # Archivos de configuración
│   ├── ajustes_conversion.json
│   ├── ajustes_subida.json
│   ├── nombres.json
│   ├── orden.json
│   ├── rutas.json
│   ├── theme.json          # Tema seleccionado
│   ├── language.json       # Idioma seleccionado
│   └── queue_state.json    # Estado de la cola
├── core/                    # Lógica de negocio central
│   ├── converter.py        # Motor de conversión
│   ├── uploader.py         # Motor de subida
│   └── core.py             # State manager
├── data/                    # Datos de la aplicación
│   ├── titles.txt          # Títulos para videos
│   ├── description.txt     # Descripción para videos
│   ├── conversion_state.csv
│   └── upload_state.csv
├── shared/                  # Utilidades compartidas
│   ├── screen_utils.py     # Adaptación de resolución
│   ├── theme_manager.py    # Gestor de temas
│   ├── navigation.py       # Sistema de navegación
│   ├── language_manager.py # Sistema multiidioma
│   ├── queue_manager.py    # Gestor de colas
│   ├── file_validator.py   # Validación de recursos
│   └── paths.py            # Rutas del proyecto
├── ui/                      # Componentes de interfaz
│   ├── blocks/             # Paneles y componentes grandes
│   │   ├── counters_panel.py
│   │   ├── modules_panel.py
│   │   ├── status_panel.py
│   │   └── top_bar.py
│   ├── pieces/             # Componentes pequeños
│   │   ├── progress_bar.py
│   │   ├── blink_animator.py
│   │   └── buttons.py
│   └── screens/            # Pantallas principales
│       ├── home_screen.py
│       ├── general_settings_screen.py
│       ├── ffmpeg_settings_screen.py
│       └── upload_settings_screen.py
├── workspace/               # Área de trabajo
│   ├── beats/              # Beats de entrada
│   ├── covers/             # Covers de entrada
│   ├── videos/             # Videos procesados
│   ├── procesed/           # Archivos procesados
│   └── temp/               # Archivos temporales
├── ffmpeg/                  # Binarios de FFmpeg
├── oauth/                   # Credenciales OAuth (NO VERSIONADO)
└── main.py                  # Punto de entrada

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
