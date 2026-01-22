"""
Casos de uso de la aplicación.
Orquestan la lógica de negocio sin depender de detalles de implementación.
"""
from typing import List, Optional, Callable
from pathlib import Path

from ecb_tool.features.ui.legacy_src.domain.entities import Beat, Cover, Video, VideoConfig
from ecb_tool.features.ui.legacy_src.infrastructure.services import FileSystemService, FFmpegService


class ConvertVideosUseCase:
    """
    Caso de uso: Convertir beats + covers en videos.
    
    Responsabilidades:
    - Validar entradas (beats, covers existen)
    - Coordinar la conversión usando FFmpeg
    - Reportar progreso
    - Manejar errores
    """
    
    def __init__(
        self,
        filesystem: FileSystemService,
        ffmpeg: FFmpegService,
        progress_callback: Optional[Callable[[str, int], None]] = None
    ):
        """
        Args:
            filesystem: Servicio de sistema de archivos
            ffmpeg: Servicio de FFmpeg
            progress_callback: Callback(message, percentage) para reportar progreso
        """
        self.filesystem = filesystem
        self.ffmpeg = ffmpeg
        self.progress_callback = progress_callback
    
    def execute(
        self,
        beats_dir: Path,
        covers_dir: Path,
        output_dir: Path,
        config: VideoConfig,
        max_videos: int = 1
    ) -> List[Video]:
        """
        Ejecuta la conversión de videos.
        
        Args:
            beats_dir: Directorio con beats
            covers_dir: Directorio con covers
            output_dir: Directorio de salida
            config: Configuración de video
            max_videos: Número máximo de videos a generar
        
        Returns:
            Lista de videos generados
        
        Raises:
            ValueError: Si no hay beats o covers suficientes
            RuntimeError: Si FFmpeg no está disponible
        """
        # Validar FFmpeg
        if not self.ffmpeg.is_available():
            raise RuntimeError("FFmpeg no está disponible")
        
        # Cargar beats y covers
        beats = self.filesystem.list_beats(beats_dir)
        covers = self.filesystem.list_covers(covers_dir)
        
        if not beats:
            raise ValueError(f"No se encontraron beats en {beats_dir}")
        if not covers:
            raise ValueError(f"No se encontraron covers en {covers_dir}")
        
        # Limitar según max_videos
        beats_to_process = beats[:max_videos]
        
        # Crear directorio de salida
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Convertir cada beat
        generated_videos = []
        total = len(beats_to_process)
        
        for idx, beat in enumerate(beats_to_process, 1):
            # Seleccionar cover (ciclar si hay menos covers que beats)
            cover = covers[(idx - 1) % len(covers)]
            
            # Nombre del video de salida
            output_filename = f"{beat.name_without_extension}.mp4"
            output_path = output_dir / output_filename
            
            # Reportar progreso
            if self.progress_callback:
                self.progress_callback(
                    f"Convirtiendo {beat.filename} + {cover.filename}",
                    int((idx - 1) / total * 100)
                )
            
            # Aquí iría la llamada real a FFmpeg
            # Por ahora, crear Video entity
            video = Video(
                filename=output_filename,
                path=output_path,
                beat=beat,
                cover=cover,
                config=config
            )
            
            generated_videos.append(video)
            
            # Reportar completado
            if self.progress_callback:
                self.progress_callback(
                    f"Completado: {output_filename}",
                    int(idx / total * 100)
                )
        
        return generated_videos


class UploadVideosUseCase:
    """
    Caso de uso: Subir videos a YouTube.
    
    Responsabilidades:
    - Validar que los videos existan
    - Coordinar la subida con YouTube API
    - Reportar progreso
    - Manejar errores
    """
    
    def __init__(
        self,
        filesystem: FileSystemService,
        progress_callback: Optional[Callable[[str, int], None]] = None
    ):
        """
        Args:
            filesystem: Servicio de sistema de archivos
            progress_callback: Callback(message, percentage) para reportar progreso
        """
        self.filesystem = filesystem
        self.progress_callback = progress_callback
    
    def execute(
        self,
        videos_dir: Path,
        uploaded_dir: Path,
        max_uploads: int = 1
    ) -> List[Video]:
        """
        Ejecuta la subida de videos.
        
        Args:
            videos_dir: Directorio con videos a subir
            uploaded_dir: Directorio donde mover videos subidos
            max_uploads: Número máximo de videos a subir
        
        Returns:
            Lista de videos subidos
        
        Raises:
            ValueError: Si no hay videos para subir
        """
        # Cargar videos
        videos = self.filesystem.list_videos(videos_dir)
        
        if not videos:
            raise ValueError(f"No se encontraron videos en {videos_dir}")
        
        # Limitar según max_uploads
        videos_to_upload = videos[:max_uploads]
        
        # Crear directorio de subidos
        uploaded_dir.mkdir(parents=True, exist_ok=True)
        
        # Subir cada video
        uploaded_videos = []
        total = len(videos_to_upload)
        
        for idx, video in enumerate(videos_to_upload, 1):
            # Reportar progreso
            if self.progress_callback:
                self.progress_callback(
                    f"Subiendo {video.filename}",
                    int((idx - 1) / total * 100)
                )
            
            # TODO: Aquí iría la llamada a YouTube API
            # Por ahora, solo mover el archivo
            destination = uploaded_dir / video.filename
            if video.path.exists():
                video.path.rename(destination)
                video.path = destination
            
            uploaded_videos.append(video)
            
            # Reportar completado
            if self.progress_callback:
                self.progress_callback(
                    f"Subido: {video.filename}",
                    int(idx / total * 100)
                )
        
        return uploaded_videos


__all__ = [
    "ConvertVideosUseCase",
    "UploadVideosUseCase",
]

