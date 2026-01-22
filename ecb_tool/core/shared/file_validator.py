"""Sistema de validación de archivos necesarios."""
import os
from typing import Dict, List
from ecb_tool.core.shared.paths import ROOT_DIR


class FileValidator:
    """Valida la disponibilidad de archivos necesarios."""
    
    def __init__(self):
        self.workspace = os.path.join(ROOT_DIR, 'workspace')
        self.beats_dir = os.path.join(self.workspace, 'beats')
        self.covers_dir = os.path.join(self.workspace, 'covers')
        self.videos_dir = os.path.join(self.workspace, 'videos')
        self.titles_file = os.path.join(ROOT_DIR, 'data', 'titles.txt')
        self.description_file = os.path.join(ROOT_DIR, 'data', 'description.txt')
    
    def _count_files(self, directory: str, extensions: List[str]) -> int:
        """Cuenta archivos con extensiones específicas."""
        if not os.path.exists(directory):
            return 0
        count = 0
        for file in os.listdir(directory):
            if any(file.lower().endswith(ext) for ext in extensions):
                count += 1
        return count
    
    def check_conversion_files(self) -> Dict:
        """Verifica archivos necesarios para conversión."""
        beats = self._count_files(self.beats_dir, ['.mp3', '.wav', '.flac', '.ogg'])
        covers = self._count_files(self.covers_dir, ['.jpg', '.jpeg', '.png', '.gif'])
        
        return {
            'beats': beats,
            'covers': covers,
            'ready': beats > 0 and covers > 0,
            'missing': []
        }
    
    def check_upload_files(self) -> Dict:
        """Verifica archivos necesarios para subida."""
        videos = self._count_files(self.videos_dir, ['.mp4', '.avi', '.mov', '.mkv'])
        
        # Verificar títulos
        titles_exist = os.path.exists(self.titles_file)
        titles_count = 0
        if titles_exist:
            try:
                with open(self.titles_file, 'r', encoding='utf-8') as f:
                    titles_count = len([line.strip() for line in f if line.strip()])
            except:
                pass
        
        # Verificar descripción
        description_exists = os.path.exists(self.description_file)
        
        missing = []
        if videos == 0:
            missing.append('videos')
        if not titles_exist or titles_count == 0:
            missing.append('títulos')
        if not description_exists:
            missing.append('descripción')
        
        return {
            'videos': videos,
            'titles': titles_count,
            'description': description_exists,
            'ready': len(missing) == 0,
            'missing': missing
        }
    
    def check_all(self) -> Dict:
        """Verifica todos los archivos necesarios."""
        conv = self.check_conversion_files()
        upload = self.check_upload_files()
        
        return {
            'conversion': conv,
            'upload': upload,
            'all_ready': conv['ready'] and upload['ready']
        }


# Instancia global
_file_validator = None

def get_file_validator():
    """Obtiene la instancia del validador."""
    global _file_validator
    if _file_validator is None:
        _file_validator = FileValidator()
    return _file_validator
