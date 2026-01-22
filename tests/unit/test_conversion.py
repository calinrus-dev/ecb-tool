"""Unit tests for conversion feature."""

import pytest
from pathlib import Path

from ecb_tool.features.conversion.models import ConversionConfig, ConversionJob
from ecb_tool.features.conversion.converter import VideoConverter


def test_conversion_config_creation(project_paths):
    """Test ConversionConfig creation."""
    config = ConversionConfig(
        beats_dir=project_paths.beats,
        covers_dir=project_paths.covers,
        videos_dir=project_paths.videos,
    )
    
    assert config.resolution == "1920x1080"
    assert config.fps == 30
    assert config.beats_per_video == 1


def test_conversion_job_creation(project_paths):
    """Test ConversionJob creation."""
    job = ConversionJob(
        id="test-1",
        beat_file=project_paths.beats / "test.mp3",
        cover_file=project_paths.covers / "test.jpg",
        output_file=project_paths.videos / "output.mp4",
    )
    
    assert job.status == "pending"
    assert job.progress == 0.0
    assert job.error_message is None


def test_video_converter_list_beats(project_paths, sample_beat):
    """Test listing beat files."""
    config = ConversionConfig(
        beats_dir=project_paths.beats,
        covers_dir=project_paths.covers,
        videos_dir=project_paths.videos,
    )
    
    converter = VideoConverter(config)
    beats = converter.list_beats()
    
    assert len(beats) == 1
    assert beats[0].name == "test_beat.mp3"


def test_video_converter_list_covers(project_paths, sample_cover):
    """Test listing cover files."""
    config = ConversionConfig(
        beats_dir=project_paths.beats,
        covers_dir=project_paths.covers,
        videos_dir=project_paths.videos,
    )
    
    converter = VideoConverter(config)
    covers = converter.list_covers()
    
    assert len(covers) == 1
    assert covers[0].name == "test_cover.jpg"
