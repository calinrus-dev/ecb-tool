# 📋 PLAN DE MIGRACIÓN: Archivos Viejos → Nueva Estructura

## 🎯 RESUMEN EJECUTIVO

**Situación:** Tienes 2 estructuras paralelas:
- ✅ **Nueva (ecb_tool/)**: Profesional, con tests, limpia
- ⚠️ **Vieja (core/, ui/, shared/, utilities/)**: Funcional pero desordenada

**Estrategia:** Migración gradual sin romper nada

---

## 📊 INVENTARIO DE ARCHIVOS

### ✅ NUEVOS (mantener y usar)

```
ecb_tool/
  ├── core/                       ⭐ USAR ESTOS
  │   ├── paths.py               ✅ Sistema de rutas centralizado
  │   └── config.py              ✅ ConfigManager mejorado
  │
  ├── features/                   ⭐ USAR ESTOS
  │   ├── conversion/            ✅ VideoConverter refactorizado
  │   ├── upload/                ✅ VideoUploader refactorizado
  │   ├── settings/              ✅ SettingsManager nuevo
  │   └── ui/                    📁 Vacío (migrar aquí)
  │
  └── main.py                    ✅ Entry point moderno

tests/                            ⭐ USAR ESTOS
  ├── unit/                      ✅ 20+ tests
  └── integration/               ✅ Tests de workflow

pyproject.toml                   ✅ Configuración moderna
```

### ⚠️ VIEJOS (migrar o eliminar)

#### 🔴 DUPLICADOS (pueden eliminarse después de migrar)

```
core/
  ├── converter.py              ⚠️ DUPLICADO → ecb_tool/features/conversion/converter.py
  ├── uploader.py               ⚠️ DUPLICADO → ecb_tool/features/upload/uploader.py
  └── core.py                   ⚠️ Lógica dispersa

shared/
  ├── paths.py                  ⚠️ DUPLICADO → ecb_tool/core/paths.py
  └── otros...                  ⚠️ Migrar funciones útiles

utilities/
  ├── apply_settings.py         ⚠️ DUPLICADO → ecb_tool/core/config.py
  ├── ffmpeg_paths.py           ⚠️ Migrar a ecb_tool/core/paths.py
  └── youtube_auth.py           ⚠️ Migrar a ecb_tool/features/upload/
```

#### 🟡 UI (migrar a ecb_tool/features/ui/)

```
ui/
  ├── blocks/                   🟡 MIGRAR a ecb_tool/features/ui/blocks/
  │   ├── upload_settings_dialog.py  (con bugs ya corregidos)
  │   ├── ffmpeg_settings_dialog.py  (con bugs ya corregidos)
  │   └── otros...
  │
  ├── pieces/                   🟡 MIGRAR a ecb_tool/features/ui/pieces/
  │   ├── buttons.py
  │   ├── progress_bar.py
  │   └── otros...
  │
  └── screens/                  🟡 MIGRAR a ecb_tool/features/ui/screens/
      ├── home_screen.py
      └── otros...
```

#### 🟢 MANTENER (útiles)

```
src/                             🟢 REVISAR - tiene presentation/main_window.py
  ├── presentation/
  │   └── main_window.py        🟢 Ventana principal de PyQt6
  └── otros...

shared/                          🟢 Revisar funciones útiles
  ├── theme_manager.py          🟢 Temas - migrar
  ├── language_manager.py       🟢 i18n - migrar
  ├── validators.py             🟢 Validadores - migrar
  └── navigation.py             🟢 Navegación - migrar

scripts/                         🟢 Mantener
  ├── auto_backup.py            🟢 Scripts auxiliares
  └── otros...
```

#### 🔵 CONFIGURACIÓN (mantener)

```
config/                          🔵 MANTENER - datos del usuario
  ├── ajustes_conversion.json
  ├── ajustes_subida.json
  ├── language.json
  └── otros...

data/                            🔵 MANTENER - datos runtime
  ├── conversion_state.csv
  ├── titles.txt
  └── otros...

oauth/                           🔵 MANTENER - credenciales YouTube
  └── client_secrets.json
```

---

## 🚀 PLAN DE ACCIÓN (3 fases)

### 📍 FASE 1: MIGRACIÓN UI (2-3 horas)

**Objetivo:** Mover components UI a nueva estructura

```bash
# 1. Crear estructura de directorios
ecb_tool/features/ui/
  ├── blocks/
  ├── pieces/
  ├── screens/
  └── __init__.py

# 2. Copiar archivos
cp ui/blocks/* ecb_tool/features/ui/blocks/
cp ui/pieces/* ecb_tool/features/ui/pieces/
cp ui/screens/* ecb_tool/features/ui/screens/

# 3. Actualizar imports en cada archivo
Viejo: from shared.paths import get_paths
Nuevo: from ecb_tool.core.paths import get_paths

Viejo: from utilities.apply_settings import ConfigManager
Nuevo: from ecb_tool.core.config import ConfigManager

Viejo: from core.converter import VideoConverter
Nuevo: from ecb_tool.features.conversion import VideoConverter
```

**Checklist:**
- [ ] Mover ui/blocks/ → ecb_tool/features/ui/blocks/
- [ ] Mover ui/pieces/ → ecb_tool/features/ui/pieces/
- [ ] Mover ui/screens/ → ecb_tool/features/ui/screens/
- [ ] Actualizar imports en todos los archivos UI
- [ ] Verificar con: `pytest tests/`

---

### 📍 FASE 2: MIGRACIÓN SHARED (1-2 horas)

**Objetivo:** Mover utilidades compartidas

```bash
# 1. Revisar qué funciones se usan
grep -r "from shared" --include="*.py"

# 2. Migrar a nueva estructura
shared/theme_manager.py → ecb_tool/features/ui/theme_manager.py
shared/language_manager.py → ecb_tool/core/i18n.py
shared/validators.py → ecb_tool/core/validators.py

# 3. Eliminar duplicados
rm shared/paths.py  # Ya tenemos ecb_tool/core/paths.py
```

**Checklist:**
- [ ] Migrar theme_manager.py
- [ ] Migrar language_manager.py
- [ ] Migrar validators.py
- [ ] Actualizar imports donde se usen
- [ ] Eliminar duplicados

---

### 📍 FASE 3: LIMPIEZA FINAL (30 min)

**Objetivo:** Eliminar archivos obsoletos

```bash
# 1. Mover a carpeta legacy (por si acaso)
mkdir legacy_backup/
mv core/ legacy_backup/
mv utilities/ legacy_backup/
mv shared/ legacy_backup/
mv ui/ legacy_backup/
mv src/ legacy_backup/  # Si ya no se usa

# 2. Actualizar main.py viejo para redirigir
# (Ya hecho en main_new.py)

# 3. Documentar
echo "Migración completa - $(date)" >> MIGRACION_LOG.txt
```

**Checklist:**
- [ ] Backup de archivos viejos
- [ ] Eliminar carpetas vacías
- [ ] Actualizar README.md
- [ ] Commit de migración

---

## ⚡ OPCIÓN RÁPIDA: "Convivencia Pacífica"

Si NO quieres migrar ahora, puedes hacer que convivan:

### 1. Crear wrapper en archivos viejos

**Ejemplo: core/converter.py**
```python
"""Legacy wrapper - redirects to new implementation."""
import warnings
from ecb_tool.features.conversion import VideoConverter

warnings.warn(
    "core.converter is deprecated. Use ecb_tool.features.conversion",
    DeprecationWarning,
    stacklevel=2
)

# Re-export para compatibilidad
__all__ = ['VideoConverter']
```

### 2. Actualizar main.py viejo

```python
# main.py (viejo)
import sys
from pathlib import Path

# Redirect to new main
sys.path.insert(0, str(Path(__file__).parent))
from ecb_tool.main import main

if __name__ == "__main__":
    print("⚠️ Using legacy main.py - please migrate to: python -m ecb_tool.main")
    sys.exit(main())
```

### 3. Pros/Contras

✅ **Pros:**
- No rompes nada
- Migración gradual
- Testing más seguro

❌ **Contras:**
- Duplicación de código
- Confusión para nuevos desarrolladores
- Más espacio en disco

---

## 🧪 VERIFICACIÓN POST-MIGRACIÓN

Después de cada fase, ejecutar:

```bash
# 1. Tests pasan
pytest tests/ -v

# 2. Imports funcionan
python -c "from ecb_tool.features.ui import *; print('✅ UI OK')"

# 3. App arranca
python -m ecb_tool.main

# 4. Sin warnings
python -W error -m ecb_tool.main  # Falla si hay deprecation warnings
```

---

## 📁 ESTRUCTURA FINAL (después de migración)

```
ECB TOOL/
  ├── ecb_tool/                  ⭐ TODO AQUÍ
  │   ├── core/
  │   │   ├── paths.py
  │   │   ├── config.py
  │   │   ├── validators.py
  │   │   └── i18n.py
  │   │
  │   ├── features/
  │   │   ├── conversion/
  │   │   ├── upload/
  │   │   ├── settings/
  │   │   └── ui/             ⭐ UI MIGRADA AQUÍ
  │   │       ├── blocks/
  │   │       ├── pieces/
  │   │       ├── screens/
  │   │       └── theme_manager.py
  │   │
  │   └── main.py
  │
  ├── tests/                    ⭐ TODOS LOS TESTS
  ├── config/                   📁 Datos usuario
  ├── data/                     📁 Runtime data
  ├── workspace/                📁 Videos/beats/covers
  │
  ├── legacy_backup/            📦 Archivos viejos (opcional)
  │   ├── core/
  │   ├── ui/
  │   └── shared/
  │
  ├── main.py                   → Redirect a ecb_tool/main.py
  ├── pyproject.toml
  └── README.md
```

---

## 🎯 RECOMENDACIÓN

### Para producción INMEDIATA:
```bash
# Opción "Convivencia" - 15 minutos
1. Crear wrappers en archivos viejos
2. Actualizar main.py para usar nueva estructura
3. Verificar que app arranca
4. Deploy
```

### Para refactor COMPLETO:
```bash
# Opción "Migración Total" - 4-6 horas
1. FASE 1: Migrar UI (2-3h)
2. FASE 2: Migrar shared (1-2h)
3. FASE 3: Limpieza (30min)
4. Testing extensivo (1h)
5. Deploy
```

---

## 🚨 ADVERTENCIAS

1. **NO elimines archivos sin backup**
   - Primero mueve a `legacy_backup/`
   - Después de 1 semana sin problemas, elimina

2. **NO migres todo de golpe**
   - Hazlo por fases
   - Verifica después de cada fase

3. **Mantén git commits frecuentes**
   ```bash
   git add .
   git commit -m "Fase 1: Migrar UI a ecb_tool/features/ui"
   ```

4. **Prueba en local antes de deploy**
   - `pytest tests/`
   - Ejecutar app manualmente
   - Probar todas las features

---

## ✅ DECISIÓN RÁPIDA

**¿Qué hacer AHORA?**

### Si necesitas que funcione YA:
```bash
# 1. Crear main.py redirect (ya existe main_new.py)
cp main_new.py main.py

# 2. Verificar
python main.py

# 3. Listo - conviven ambas estructuras
```

### Si tienes tiempo para hacerlo bien:
```bash
# Empezar Fase 1
mkdir -p ecb_tool/features/ui/{blocks,pieces,screens}
# ... seguir PLAN DE ACCIÓN arriba
```

---

**Actualizado:** 22 enero 2026  
**Autor:** GitHub Copilot  
**Estado:** PENDIENTE DE DECISIÓN
