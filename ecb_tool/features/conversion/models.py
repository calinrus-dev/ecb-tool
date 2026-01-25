"""Conversion data models."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List


@dataclass
class ConversionConfig:
    """Configuration for video conversion."""
    
    # Paths
    beats_dir: Path
    covers_dir: Path
    videos_dir: Path
    
    # Video settings
    resolution: str = "1920x1080"
    fps: int = 30
    video_bitrate: str = "2M"
    video_format: str = "mp4"
    
    # Audio settings
    audio_bitrate: str = "192k"
    audio_format: str = "aac"
    
    # Processing
    beats_per_video: int = 1
    batch_size: int = 1
    
    # Auto-cleanup
    auto_delete_beats: bool = False
    auto_delete_covers: bool = False
    
    # Fades
    fade_in_duration: float = 2.0
    fade_out_duration: float = 2.0
    enable_fades: bool = True


@dataclass
class ConversionJob:
    """Represents a single conversion job."""
    
    id: str
    beat_files: List[Path]  # Changed to list
    cover_file: Path
    output_file: Path
    status: str = "pending"  # pending, processing, completed, failed
    progress: float = 0.0
    error_message: Optional[str] = None


__all__ = ['ConversionConfig', 'ConversionJob']
