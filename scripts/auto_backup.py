"""
Script de automatización para backups automáticos de workspace y configuración
Uso: python scripts/auto_backup.py
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
import zipfile

# Configuración
BACKUP_DIR = Path("backups")
MAX_BACKUPS = 10  # Mantener solo los últimos 10 backups

def create_backup():
    """Crea un backup completo del workspace y configuración"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.zip"
    backup_path = BACKUP_DIR / backup_name
    
    # Crear directorio de backups si no existe
    BACKUP_DIR.mkdir(exist_ok=True)
    
    print(f"Creando backup: {backup_name}")
    
    # Directorios y archivos a respaldar
    items_to_backup = [
        "config/",
        "data/titles.txt",
        "data/description.txt",
        "workspace/procesed/",
    ]
    
    # Crear archivo ZIP
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in items_to_backup:
            item_path = Path(item)
            if item_path.is_file():
                zipf.write(item_path, item_path.name)
                print(f"  ✓ {item}")
            elif item_path.is_dir():
                for file in item_path.rglob('*'):
                    if file.is_file():
                        arcname = file.relative_to(item_path.parent)
                        zipf.write(file, arcname)
                print(f"  ✓ {item}")
    
    file_size = backup_path.stat().st_size / (1024 * 1024)  # MB
    print(f"\n✅ Backup creado exitosamente: {backup_name} ({file_size:.2f} MB)")
    
    # Limpiar backups antiguos
    cleanup_old_backups()
    
    return backup_path

def cleanup_old_backups():
    """Elimina backups antiguos manteniendo solo MAX_BACKUPS"""
    backups = sorted(BACKUP_DIR.glob("backup_*.zip"), key=os.path.getmtime, reverse=True)
    
    if len(backups) > MAX_BACKUPS:
        print(f"\n🗑️  Limpiando backups antiguos (manteniendo {MAX_BACKUPS})...")
        for old_backup in backups[MAX_BACKUPS:]:
            old_backup.unlink()
            print(f"  ✗ Eliminado: {old_backup.name}")

def restore_backup(backup_file):
    """Restaura un backup específico"""
    backup_path = BACKUP_DIR / backup_file
    
    if not backup_path.exists():
        print(f"❌ Backup no encontrado: {backup_file}")
        return False
    
    print(f"Restaurando backup: {backup_file}")
    
    # Crear backup del estado actual antes de restaurar
    print("\n📦 Creando backup de seguridad del estado actual...")
    create_backup()
    
    # Restaurar
    with zipfile.ZipFile(backup_path, 'r') as zipf:
        zipf.extractall(".")
    
    print(f"\n✅ Backup restaurado exitosamente desde: {backup_file}")
    return True

def list_backups():
    """Lista todos los backups disponibles"""
    backups = sorted(BACKUP_DIR.glob("backup_*.zip"), key=os.path.getmtime, reverse=True)
    
    if not backups:
        print("No hay backups disponibles")
        return []
    
    print("\n📋 Backups disponibles:")
    for i, backup in enumerate(backups, 1):
        size = backup.stat().st_size / (1024 * 1024)
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"{i}. {backup.name} - {size:.2f} MB - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return backups

def main():
    """Función principal"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "create":
            create_backup()
        elif command == "list":
            list_backups()
        elif command == "restore":
            if len(sys.argv) > 2:
                restore_backup(sys.argv[2])
            else:
                backups = list_backups()
                if backups:
                    choice = input("\n¿Qué backup deseas restaurar? (número): ")
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(backups):
                            restore_backup(backups[idx].name)
                        else:
                            print("❌ Número inválido")
                    except ValueError:
                        print("❌ Entrada inválida")
        else:
            print(f"❌ Comando desconocido: {command}")
            print("\nComandos disponibles:")
            print("  create  - Crear nuevo backup")
            print("  list    - Listar backups disponibles")
            print("  restore - Restaurar un backup")
    else:
        # Sin argumentos, crear backup
        create_backup()

if __name__ == "__main__":
    main()
