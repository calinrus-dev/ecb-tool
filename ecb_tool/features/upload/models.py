"""Upload data models."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class UploadConfig:
    """Configuration for video uploads."""
    
    videos_dir: Path
    uploaded_dir: Path
    
    # YouTube settings
    privacy_status: str = "public"  # public, private, unlisted
    category_id: str = "10"  # Music
    made_for_kids: bool = False
    
    # Metadata
    titles_file: Path = None
    description_file: Path = None
    
    # Scheduling
    scheduled_mode: bool = False
    upload_time: str = "12:00"
    
    # Auto-cleanup
    auto_delete_videos: bool = False
    move_to_trash: bool = False


@dataclass
class UploadJob:
    """Represents a single upload job."""
    
    id: str
    video_file: Path
    title: str
    description: str
    status: str = "pending"  # pending, uploading, completed, failed
    progress: float = 0.0
    video_id: Optional[str] = None  # YouTube video ID
    error_message: Optional[str] = None


__all__ = ['UploadConfig', 'UploadJob']
