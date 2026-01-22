"""
Centralized path management for ECB Tool.
All project paths are defined here to avoid duplication.
"""
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class ProjectPaths:
    """Container for all project paths."""
    
    # Root directories
    root: Path
    config: Path
    data: Path
    logs: Path
    oauth: Path
    
    # Workspace directories
    workspace: Path
    beats: Path
    covers: Path
    videos: Path
    uploaded: Path
    processed: Path
    temp: Path
    trash: Path
    
    # Config files
    order_config: Path
    conversion_config: Path
    upload_config: Path
    routes_config: Path
    names_config: Path
    theme_config: Path
    language_config: Path
    queue_state: Path
    schedule_config: Path
    
    # Data files
    titles_file: Path
    description_file: Path
    conversion_state: Path
    upload_state: Path
    app_log: Path
    
    # Special files
    stop_flag: Path
    
    # FFmpeg
    ffmpeg_dir: Path
    ffmpeg_bin: Path
    ffprobe_bin: Path
    ffplay_bin: Path


def find_project_root(start_path: Optional[Path] = None) -> Path:
    """
    Find project root by looking for main.py or config/orden.json.
    
    Args:
        start_path: Path to start search from (defaults to this file's directory)
    
    Returns:
        Path to project root
    """
    if start_path is None:
        start_path = Path(__file__).parent
    
    current = Path(start_path).resolve()
    
    # Search up to 5 levels
    for _ in range(5):
        # Check for main.py or config directory
        if (current / 'main.py').exists() or (current / 'config').exists():
            return current
        
        # Go up one level
        if current.parent == current:
            # Reached filesystem root
            break
        current = current.parent
    
    # Fallback: assume current directory
    return Path.cwd()


def get_project_paths(root_dir: Optional[Path] = None) -> ProjectPaths:
    """
    Get all project paths in a structured container.
    
    Args:
        root_dir: Project root directory (auto-detected if None)
    
    Returns:
        ProjectPaths instance with all paths
    """
    if root_dir is None:
        root_dir = find_project_root()
    
    root = Path(root_dir)
    
    # Ensure Path objects
    root = Path(root).resolve()
    
    # Core directories
    config = root / 'config'
    data = root / 'data'
    logs = root / 'logs'
    oauth = root / 'oauth'
    
    # Workspace structure
    workspace = root / 'workspace'
    beats = workspace / 'beats'
    covers = workspace / 'covers'
    videos = workspace / 'videos'
    uploaded = workspace / 'uploaded'
    processed = workspace / 'processed'
    temp = workspace / 'temp'
    trash = workspace / 'trash'
    
    # Config files
    order_config = config / 'orden.json'
    conversion_config = config / 'ajustes_conversion.json'
    upload_config = config / 'ajustes_subida.json'
    routes_config = config / 'rutas.json'
    names_config = config / 'nombres.json'
    theme_config = config / 'theme.json'
    language_config = config / 'language.json'
    queue_state = config / 'queue_state.json'
    schedule_config = config / 'programacion_subidas.json'
    
    # Data files
    titles_file = data / 'titles.txt'
    description_file = data / 'description.txt'
    conversion_state = data / 'conversion_state.csv'
    upload_state = data / 'upload_state.csv'
    app_log = data / 'app.log'
    
    # Special files
    stop_flag = root / '.parar'
    
    # FFmpeg paths
    ffmpeg_dir = root / 'ffmpeg'
    ffmpeg_bin = ffmpeg_dir / 'bin' / 'ffmpeg.exe'
    ffprobe_bin = ffmpeg_dir / 'bin' / 'ffprobe.exe'
    ffplay_bin = ffmpeg_dir / 'bin' / 'ffplay.exe'
    
    return ProjectPaths(
        root=root,
        config=config,
        data=data,
        logs=logs,
        oauth=oauth,
        workspace=workspace,
        beats=beats,
        covers=covers,
        videos=videos,
        uploaded=uploaded,
        processed=processed,
        temp=temp,
        trash=trash,
        order_config=order_config,
        conversion_config=conversion_config,
        upload_config=upload_config,
        routes_config=routes_config,
        names_config=names_config,
        theme_config=theme_config,
        language_config=language_config,
        queue_state=queue_state,
        schedule_config=schedule_config,
        titles_file=titles_file,
        description_file=description_file,
        conversion_state=conversion_state,
        upload_state=upload_state,
        app_log=app_log,
        stop_flag=stop_flag,
        ffmpeg_dir=ffmpeg_dir,
        ffmpeg_bin=ffmpeg_bin,
        ffprobe_bin=ffprobe_bin,
        ffplay_bin=ffplay_bin,
    )


def ensure_directories(paths: ProjectPaths) -> None:
    """
    Create all required directories if they don't exist.
    
    Args:
        paths: ProjectPaths instance
    """
    directories = [
        paths.config,
        paths.data,
        paths.logs,
        paths.oauth,
        paths.workspace,
        paths.beats,
        paths.covers,
        paths.videos,
        paths.uploaded,
        paths.processed,
        paths.temp,
        paths.trash,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# Global instance - lazy loaded
_paths_instance: Optional[ProjectPaths] = None


def get_paths() -> ProjectPaths:
    """Get global ProjectPaths instance (singleton pattern)."""
    global _paths_instance
    if _paths_instance is None:
        _paths_instance = get_project_paths()
        ensure_directories(_paths_instance)
    return _paths_instance


def reset_paths() -> None:
    """Reset global paths instance (useful for testing)."""
    global _paths_instance
    _paths_instance = None


__all__ = [
    'ProjectPaths',
    'find_project_root',
    'get_project_paths',
    'ensure_directories',
    'get_paths',
    'reset_paths',
]
