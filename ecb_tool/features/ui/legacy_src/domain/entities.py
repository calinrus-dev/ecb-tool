"""
Entidades del dominio para ECB TOOL.
Representan los conceptos core del negocio.
"""
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class Beat:
    """Representa un archivo de audio (beat)."""
    
    filename: str
    path: Path
    duration: Optional[float] = None
    format: Optional[str] = None
    
    @property
    def name_without_extension(self) -> str:
        """Retorna el nombre sin extensión."""
        return Path(self.filename).stem
    
    def exists(self) -> bool:
        """Verifica si el archivo existe."""
        return self.path.exists()


@dataclass
class Cover:
    """Representa una imagen de portada."""
    
    filename: str
    path: Path
    width: Optional[int] = None
    height: Optional[int] = None
    
    @property
    def name_without_extension(self) -> str:
        """Retorna el nombre sin extensión."""
        return Path(self.filename).stem
    
    def exists(self) -> bool:
        """Verifica si el archivo existe."""
        return self.path.exists()


@dataclass
class VideoConfig:
    """Configuración para generación de video."""
    
    resolution: str = "1920x1080"
    fps: int = 30
    video_bitrate: str = "2M"
    audio_bitrate: str = "192k"
    loop_cover: bool = True
    auto_delete_beats: bool = False
    auto_delete_covers: bool = False
    
    @property
    def width(self) -> int:
        """Retorna el ancho del video."""
        return int(self.resolution.split('x')[0])
    
    @property
    def height(self) -> int:
        """Retorna la altura del video."""
        return int(self.resolution.split('x')[1])


@dataclass
class Video:
    """Representa un video generado."""
    
    filename: str
    path: Path
    beat: Optional[Beat] = None
    cover: Optional[Cover] = None
    config: Optional[VideoConfig] = None
    
    @property
    def name_without_extension(self) -> str:
        """Retorna el nombre sin extensión."""
        return Path(self.filename).stem
    
    def exists(self) -> bool:
        """Verifica si el archivo existe."""
        return self.path.exists()
    
    def size_mb(self) -> Optional[float]:
        """Retorna el tamaño en MB."""
        if self.path.exists():
            return self.path.stat().st_size / (1024 * 1024)
        return None


@dataclass
class ProcessState:
    """Estado de un proceso de conversión o subida."""
    
    mode: str  # convertir, subir, alternar, simultaneo
    orders: int = 1
    is_running: bool = False
    auto_continue: bool = False
    videos_converted: int = 0
    videos_uploaded: int = 0
    
    def is_complete(self) -> bool:
        """Verifica si el proceso está completo."""
        if self.mode == "convertir":
            return self.videos_converted >= self.orders
        elif self.mode == "subir":
            return self.videos_uploaded >= self.orders
        return False


__all__ = [
    "Beat",
    "Cover",
    "Video",
    "VideoConfig",
    "ProcessState",
]
