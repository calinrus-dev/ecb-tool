"""
Script de automatización para limpieza de archivos temporales y logs antiguos
Uso: python scripts/auto_cleanup.py
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
import shutil

# Configuración
DAYS_TO_KEEP_LOGS = 30
DAYS_TO_KEEP_TEMP = 7
DRY_RUN = False  # Cambiar a True para simular sin eliminar

def cleanup_logs():
    """Elimina logs antiguos"""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        return
    
    cutoff_date = datetime.now() - timedelta(days=DAYS_TO_KEEP_LOGS)
    deleted_count = 0
    freed_space = 0
    
    print(f"🗑️  Limpiando logs más antiguos que {DAYS_TO_KEEP_LOGS} días...")
    
    for log_file in logs_dir.glob("*.log"):
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        if mtime < cutoff_date:
            size = log_file.stat().st_size
            if not DRY_RUN:
                log_file.unlink()
            print(f"  ✗ {log_file.name} ({size / 1024:.2f} KB)")
            deleted_count += 1
            freed_space += size
    
    if deleted_count > 0:
        print(f"\n✅ Eliminados {deleted_count} archivos de log ({freed_space / (1024 * 1024):.2f} MB)")
    else:
        print("  ✓ No hay logs antiguos para eliminar")

def cleanup_temp():
    """Elimina archivos temporales"""
    temp_dir = Path("workspace/temp")
    if not temp_dir.exists():
        return
    
    cutoff_date = datetime.now() - timedelta(days=DAYS_TO_KEEP_TEMP)
    deleted_count = 0
    freed_space = 0
    
    print(f"\n🗑️  Limpiando archivos temporales más antiguos que {DAYS_TO_KEEP_TEMP} días...")
    
    for temp_file in temp_dir.rglob("*"):
        if temp_file.is_file():
            mtime = datetime.fromtimestamp(temp_file.stat().st_mtime)
            if mtime < cutoff_date:
                size = temp_file.stat().st_size
                if not DRY_RUN:
                    temp_file.unlink()
                print(f"  ✗ {temp_file.name} ({size / 1024:.2f} KB)")
                deleted_count += 1
                freed_space += size
    
    # Eliminar directorios vacíos
    for temp_dir in temp_dir.rglob("*"):
        if temp_dir.is_dir() and not any(temp_dir.iterdir()):
            if not DRY_RUN:
                temp_dir.rmdir()
            print(f"  ✗ [DIR] {temp_dir.name}")
    
    if deleted_count > 0:
        print(f"\n✅ Eliminados {deleted_count} archivos temporales ({freed_space / (1024 * 1024):.2f} MB)")
    else:
        print("  ✓ No hay archivos temporales antiguos para eliminar")

def cleanup_pycache():
    """Elimina archivos __pycache__"""
    print("\n🗑️  Limpiando __pycache__...")
    deleted_count = 0
    
    for pycache_dir in Path(".").rglob("__pycache__"):
        if pycache_dir.is_dir():
            if not DRY_RUN:
                shutil.rmtree(pycache_dir)
            print(f"  ✗ {pycache_dir}")
            deleted_count += 1
    
    if deleted_count > 0:
        print(f"\n✅ Eliminados {deleted_count} directorios __pycache__")
    else:
        print("  ✓ No hay __pycache__ para eliminar")

def cleanup_state_files():
    """Limpia archivos de estado antiguos"""
    print("\n🗑️  Limpiando archivos de estado duplicados...")
    
    state_files = [
        "data/conversion_state.csv",
        "data/upload_state.csv",
    ]
    
    for state_file in state_files:
        state_path = Path(state_file)
        if state_path.exists():
            # Crear backup antes de limpiar
            backup_path = state_path.with_suffix(".csv.bak")
            if not DRY_RUN:
                shutil.copy2(state_path, backup_path)
            print(f"  ✓ Backup creado: {backup_path.name}")

def get_disk_usage():
    """Obtiene el uso de disco del proyecto"""
    total_size = 0
    
    directories = {
        "workspace/": 0,
        "logs/": 0,
        "config/": 0,
        "data/": 0,
        "ffmpeg/": 0,
    }
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if dir_path.exists():
            for file in dir_path.rglob("*"):
                if file.is_file():
                    size = file.stat().st_size
                    directories[dir_name] += size
                    total_size += size
    
    print("\n📊 Uso de disco:")
    for dir_name, size in sorted(directories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {dir_name:<15} {size / (1024 * 1024):>10.2f} MB")
    print(f"  {'TOTAL':<15} {total_size / (1024 * 1024):>10.2f} MB")

def main():
    """Función principal"""
    print("=" * 60)
    print("ECB TOOL - Auto Cleanup Script")
    print("=" * 60)
    
    if DRY_RUN:
        print("\n⚠️  MODO DRY-RUN - No se eliminarán archivos\n")
    
    get_disk_usage()
    
    cleanup_logs()
    cleanup_temp()
    cleanup_pycache()
    cleanup_state_files()
    
    print("\n" + "=" * 60)
    print("✅ Limpieza completada")
    print("=" * 60)
    
    get_disk_usage()

if __name__ == "__main__":
    main()
