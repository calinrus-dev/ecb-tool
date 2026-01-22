# ECB-copilot

ECB-copilot es una Content Factory automatizada para productores musicales. Permite crear y subir videos musicales de forma masiva, combinando audios (beats) e imágenes (portadas), gestionando la metadata y la programación de publicaciones en YouTube. Todo desde una interfaz moderna y oscura, optimizada para Windows 11.

## Requisitos Previos

- Python 3.10+
- FFmpeg instalado y accesible desde la terminal ([descargar](https://ffmpeg.org/download.html))
- Credenciales OAuth2 de Google Cloud Console para YouTube Data API v3 ([instrucciones](https://console.cloud.google.com/))
- Internet para traducción automática y subida a YouTube

## Instalación

1. Clona el repositorio y entra en la carpeta raíz.
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   Principales dependencias:
   - pyqt6
   - pyqtdarktheme
   - ffmpeg-python
   - google-api-python-client
   - deep-translator

3. Configura tus credenciales de Google en la carpeta `datos/` (ver documentación interna).
4. Asegúrate de tener FFmpeg en tu PATH.

## Ejecución rápida

No es necesario activar el entorno virtual con PowerShell. Simplemente ejecuta la app así:

```powershell
C:/Users/calin/Desktop/ECB TOOL/.venv/Scripts/python.exe main.py
```

Esto usará el entorno virtual automáticamente.

## Estructura del Proyecto

```
root/
│
├── main.py                # Entry point
├── copiar.py              # Utilidad para copiar código/estructura
├── estructura.py          # Visualización de estructura de carpetas
├── helper.py              # Funciones de apoyo y utilidades
├── raizejecutor.py        # Ejecución de archivos desde la GUI
├── ui.py                  # Interfaz principal
│
├── interfaz/
│   ├── bloques/           # Componentes visuales (barra, paneles, selectores)
│   ├── piezas/            # Elementos UI (botones, texto, separadores)
│   └── ventanas/          # Ventanas principales
│
├── nucleo/
│   ├── convertidor.py     # Lógica de renderizado y procesamiento multimedia
│   └── core.py            # Motor central y lógica de negocio
│
├── utilidades/
│   └── aplicar_ajustes.py # Aplicación de configuraciones y utilidades extra
│
├── configuracion/
│   ├── ajustes_conversion.json
│   ├── ajustes_subida.json
│   ├── nombres.json
│   ├── orden.json
│   └── rutas.json
│
├── datos/
│   ├── titulos.txt
│   ├── descripcion.txt
│   ├── estado_conversion.csv
│   ├── estado_subida.csv
│   └── history.json
│
├── beats/                 # Audios fuente
├── portadas/              # Imágenes de portada
├── subidos/               # Videos subidos
├── videos/                # Videos renderizados
```

## Uso Básico

1. Ejecuta `main.py`.
2. Carga tus beats e imágenes en las carpetas correspondientes.
3. Configura BPV, FPS y filtros en la interfaz.
4. Genera videos y gestiona la metadata.
5. Programa la subida a YouTube desde la pestaña Calendario.

## Licencia

MIT
