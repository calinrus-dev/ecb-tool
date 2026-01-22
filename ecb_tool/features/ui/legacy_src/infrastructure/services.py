"""
Servicios de la capa de infraestructura.
Interactúan con sistemas externos (FFmpeg, archivos, etc.)
"""
import os
import subprocess
from typing import List, Optional
from pathlib import Path

from ecb_tool.features.ui.legacy_src.domain.entities import Beat, Cover, Video, VideoConfig


class FileSystemService:
    """Servicio para operaciones con el sistema de archivos."""
    
    @staticmethod
    def list_beats(directory: Path, extensions: Optional[List[str]] = None) -> List[Beat]:
        """
        Lista todos los beats en un directorio.
        
        Args:
            directory: Directorio donde buscar
            extensions: Extensiones permitidas (default: audio comunes)
        
        Returns:
            Lista de objetos Beat
        """
        if extensions is None:
            extensions = ['.mp3', '.wav', '.aac', '.flac', '.m4a']
        
        beats = []
        if not directory.exists():
            return beats
        
        for file in sorted(directory.iterdir()):
            if file.is_file() and file.suffix.lower() in extensions:
                beats.append(Beat(
                    filename=file.name,
                    path=file,
                    format=file.suffix[1:]  # Remove dot
                ))
        
        return beats
    
    @staticmethod
    def list_covers(directory: Path, extensions: Optional[List[str]] = None) -> List[Cover]:
        """
        Lista todas las portadas en un directorio.
        
        Args:
            directory: Directorio donde buscar
            extensions: Extensiones permitidas (default: imágenes comunes)
        
        Returns:
            Lista de objetos Cover
        """
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png']
        
        covers = []
        if not directory.exists():
            return covers
        
        for file in sorted(directory.iterdir()):
            if file.is_file() and file.suffix.lower() in extensions:
                covers.append(Cover(
                    filename=file.name,
                    path=file
                ))
        
        return covers
    
    @staticmethod
    def list_videos(directory: Path) -> List[Video]:
        """
        Lista todos los videos en un directorio.
        
        Args:
            directory: Directorio donde buscar
        
        Returns:
            Lista de objetos Video
        """
        videos = []
        if not directory.exists():
            return videos
        
        for file in sorted(directory.iterdir()):
            if file.is_file() and file.suffix.lower() == '.mp4':
                videos.append(Video(
                    filename=file.name,
                    path=file
                ))
        
        return videos


class FFmpegService:
    """Servicio para operaciones con FFmpeg."""
    
    def __init__(self, ffmpeg_path: Optional[str] = None):
        """
        Args:
            ffmpeg_path: Ruta al ejecutable de FFmpeg (None para buscar en PATH)
        """
        self.ffmpeg_path = ffmpeg_path or "ffmpeg"
    
    def is_available(self) -> bool:
        """Verifica si FFmpeg está disponible."""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def get_version(self) -> Optional[str]:
        """Obtiene la versión de FFmpeg."""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                first_line = result.stdout.split('\n')[0]
                return first_line.replace('ffmpeg version ', '').split()[0]
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        return None


__all__ = [
    "FileSystemService",
    "FFmpegService",
]

