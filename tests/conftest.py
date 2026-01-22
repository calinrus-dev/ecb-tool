"""Test configuration and fixtures."""

import pytest
from pathlib import Path
import tempfile
import shutil

from ecb_tool.core.paths import ProjectPaths, get_project_paths


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory structure."""
    # Create directory structure
    (tmp_path / 'config').mkdir()
    (tmp_path / 'data').mkdir()
    (tmp_path / 'logs').mkdir()
    (tmp_path / 'oauth').mkdir()
    (tmp_path / 'workspace').mkdir()
    (tmp_path / 'workspace' / 'beats').mkdir()
    (tmp_path / 'workspace' / 'covers').mkdir()
    (tmp_path / 'workspace' / 'videos').mkdir()
    (tmp_path / 'workspace' / 'uploaded').mkdir()
    (tmp_path / 'workspace' / 'processed').mkdir()
    (tmp_path / 'workspace' / 'temp').mkdir()
    (tmp_path / 'workspace' / 'trash').mkdir()
    (tmp_path / 'ffmpeg').mkdir()
    (tmp_path / 'ffmpeg' / 'bin').mkdir()
    
    # Create main.py to mark as project root
    (tmp_path / 'main.py').write_text("# Test project")
    
    yield tmp_path
    
    # Cleanup handled by pytest tmp_path


@pytest.fixture
def project_paths(temp_project_dir):
    """Get ProjectPaths for temporary directory."""
    return get_project_paths(temp_project_dir)


@pytest.fixture
def sample_beat(temp_project_dir):
    """Create a sample beat file."""
    beat_file = temp_project_dir / 'workspace' / 'beats' / 'test_beat.mp3'
    beat_file.write_text("fake beat data")
    return beat_file


@pytest.fixture
def sample_cover(temp_project_dir):
    """Create a sample cover file."""
    cover_file = temp_project_dir / 'workspace' / 'covers' / 'test_cover.jpg'
    cover_file.write_text("fake image data")
    return cover_file


@pytest.fixture
def ffmpeg_available():
    """Check if FFmpeg is available in system PATH."""
    import shutil
    return shutil.which('ffmpeg') is not None


@pytest.fixture
def conversion_config_no_delete(temp_project_dir):
    """Create a conversion config with auto-deletion disabled."""
    from ecb_tool.features.conversion.models import ConversionConfig
    
    return ConversionConfig(
        beats_dir=temp_project_dir / 'workspace' / 'beats',
        covers_dir=temp_project_dir / 'workspace' / 'covers',
        videos_dir=temp_project_dir / 'workspace' / 'videos',
        resolution="1280x720",
        fps=24,
        video_bitrate="1M",
        audio_bitrate="128k",
        auto_delete_beats=False,  # IMPORTANT: No delete
        auto_delete_covers=False,  # IMPORTANT: No delete
        enable_fades=False
    )
