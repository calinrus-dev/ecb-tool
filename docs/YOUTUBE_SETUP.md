# Configuración de OAuth para YouTube

## Paso 1: Obtener credenciales de Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto (o selecciona uno existente)
3. Ve a "APIs y servicios" > "Biblioteca"
4. Busca "YouTube Data API v3" y habilítala
5. Ve a "Credenciales" > "Crear credenciales" > "ID de cliente de OAuth 2.0"
6. Configura la pantalla de consentimiento si es necesario
7. Tipo de aplicación: "Aplicación de escritorio"
8. Descarga el archivo JSON de credenciales

## Paso 2: Configurar las credenciales

1. Renombra el archivo descargado a `client_secrets.json`
2. Colócalo en la carpeta `oauth/` del proyecto

## Paso 3: Instalar dependencias

Ejecuta `install_youtube_deps.bat` para instalar las librerías necesarias:
- google-auth
- google-auth-oauthlib
- google-api-python-client

## Paso 4: Primer uso

La primera vez que uses la función de upload:
1. Se abrirá automáticamente tu navegador
2. Inicia sesión con tu cuenta de YouTube
3. Autoriza la aplicación
4. Las credenciales se guardarán en `oauth/token.pickle`

## Notas

- Los títulos se toman del archivo `data/titles.txt` (una línea = un título)
- La descripción se toma de `data/description.txt`
- Cada título se elimina automáticamente después de usarse
- Si no hay títulos disponibles, el proceso espera
