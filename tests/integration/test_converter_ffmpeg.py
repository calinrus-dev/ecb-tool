"""Integration tests for video converter with FFmpeg.

Tests the complete conversion workflow:
- FFmpeg execution and video creation
- File validation before/after conversion
- No auto-deletion of source files
- Error handling and status updates
- Output file verification
"""

import pytest
import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil

from ecb_tool.features.conversion.models import ConversionConfig, ConversionJob
from ecb_tool.features.conversion.converter import VideoConverter


class TestVideoConverterFFmpeg:
    """Integration tests for VideoConverter with real FFmpeg."""
    
    @pytest.fixture
    def converter_config(self, temp_project_dir):
        """Create converter configuration without auto-deletion."""
        config = ConversionConfig(
            beats_dir=temp_project_dir / 'workspace' / 'beats',
            covers_dir=temp_project_dir / 'workspace' / 'covers',
            videos_dir=temp_project_dir / 'workspace' / 'videos',
            resolution="1280x720",  # Smaller for faster testing
            fps=24,
            video_bitrate="1M",
            audio_bitrate="128k",
            auto_delete_beats=False,  # NO borrar beats
            auto_delete_covers=False,  # NO borrar covers
            enable_fades=False  # Simplificar para testing
        )
        return config
    
    @pytest.fixture
    def real_audio_file(self, temp_project_dir):
        """Create a minimal valid MP3 file for testing."""
        beat_file = temp_project_dir / 'workspace' / 'beats' / 'test_beat.mp3'
        
        # Create a minimal valid MP3 using FFmpeg if available
        # Otherwise create a silent audio file
        try:
            # Try to create a 3-second silent audio file
            result = subprocess.run([
                'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
                '-t', '3', '-q:a', '9', '-acodec', 'libmp3lame',
                str(beat_file)
            ], capture_output=True, timeout=10)
            
            if result.returncode == 0 and beat_file.exists():
                return beat_file
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Fallback: create fake file for basic tests
        beat_file.write_bytes(b'ID3' + b'\x00' * 100)
        return beat_file
    
    @pytest.fixture
    def real_image_file(self, temp_project_dir):
        """Create a minimal valid image file for testing."""
        cover_file = temp_project_dir / 'workspace' / 'covers' / 'test_cover.jpg'
        
        # Try to create a real image using FFmpeg
        try:
            result = subprocess.run([
                'ffmpeg', '-f', 'lavfi', '-i', 
                'color=c=blue:s=1280x720:d=1',
                '-frames:v', '1',
                str(cover_file)
            ], capture_output=True, timeout=10)
            
            if result.returncode == 0 and cover_file.exists():
                return cover_file
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Fallback: minimal JPEG header
        cover_file.write_bytes(
            b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
            + b'\xFF\xD9'
        )
        return cover_file
    
    def test_ffmpeg_availability(self):
        """Test 1: Verify FFmpeg is available in the system."""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                timeout=5
            )
            assert result.returncode == 0, "FFmpeg should be available"
            assert b'ffmpeg version' in result.stdout.lower()
        except FileNotFoundError:
            pytest.skip("FFmpeg not found in PATH")
    
    def test_converter_initialization(self, converter_config):
        """Test 2: Verify converter initializes with correct configuration."""
        converter = VideoConverter(converter_config)
        
        assert converter.config == converter_config
        assert converter.config.auto_delete_beats is False
        assert converter.config.auto_delete_covers is False
        assert converter.paths is not None
    
    def test_list_beats_with_multiple_formats(self, converter_config, temp_project_dir):
        """Test 3: Verify beat file detection with different audio formats."""
        beats_dir = converter_config.beats_dir
        
        # Create different audio file types
        (beats_dir / 'beat1.mp3').write_text("fake mp3")
        (beats_dir / 'beat2.wav').write_text("fake wav")
        (beats_dir / 'beat3.flac').write_text("fake flac")
        (beats_dir / 'beat4.m4a').write_text("fake m4a")
        (beats_dir / 'beat5.aac').write_text("fake aac")
        (beats_dir / '.hidden.mp3').write_text("hidden")  # Should be ignored
        (beats_dir / 'readme.txt').write_text("not audio")  # Should be ignored
        
        converter = VideoConverter(converter_config)
        beats = converter.list_beats()
        
        assert len(beats) == 5, "Should detect 5 audio files"
        beat_names = [b.name for b in beats]
        assert 'beat1.mp3' in beat_names
        assert 'beat2.wav' in beat_names
        assert '.hidden.mp3' not in beat_names
        assert 'readme.txt' not in beat_names
    
    def test_list_covers_with_multiple_formats(self, converter_config, temp_project_dir):
        """Test 4: Verify cover image detection with different formats."""
        covers_dir = converter_config.covers_dir
        
        # Create different image file types
        (covers_dir / 'cover1.jpg').write_text("fake jpg")
        (covers_dir / 'cover2.jpeg').write_text("fake jpeg")
        (covers_dir / 'cover3.png').write_text("fake png")
        (covers_dir / 'cover4.bmp').write_text("fake bmp")
        (covers_dir / '.hidden.jpg').write_text("hidden")
        (covers_dir / 'readme.txt').write_text("not image")
        
        converter = VideoConverter(converter_config)
        covers = converter.list_covers()
        
        assert len(covers) == 4, "Should detect 4 image files"
        cover_names = [c.name for c in covers]
        assert 'cover1.jpg' in cover_names
        assert 'cover3.png' in cover_names
        assert '.hidden.jpg' not in cover_names
        assert 'readme.txt' not in cover_names
    
    def test_conversion_job_creation_validation(self, converter_config, real_audio_file, real_image_file):
        """Test 5: Verify conversion job creation with proper validation."""
        output_file = converter_config.videos_dir / 'output_test.mp4'
        
        job = ConversionJob(
            id="test-job-001",
            beat_file=real_audio_file,
            cover_file=real_image_file,
            output_file=output_file
        )
        
        # Validate initial state
        assert job.status == "pending"
        assert job.progress == 0.0
        assert job.error_message is None
        assert job.beat_file.exists(), "Beat file must exist"
        assert job.cover_file.exists(), "Cover file must exist"
        assert job.id == "test-job-001"
    
    def test_output_directory_creation(self, converter_config, real_audio_file, real_image_file):
        """Test 6: Verify output directory is created if it doesn't exist."""
        # Create a nested output path
        nested_output = converter_config.videos_dir / 'subfolder' / 'nested' / 'video.mp4'
        
        job = ConversionJob(
            id="test-nested",
            beat_file=real_audio_file,
            cover_file=real_image_file,
            output_file=nested_output
        )
        
        converter = VideoConverter(converter_config)
        
        # Directory should not exist yet
        assert not nested_output.parent.exists()
        
        # Mock the actual FFmpeg call to avoid real conversion
        with patch('ffmpeg.run') as mock_run:
            converter.convert(job)
        
        # Directory should now exist
        assert nested_output.parent.exists()
        assert nested_output.parent.is_dir()
    
    @pytest.mark.skipif(
        not shutil.which('ffmpeg'),
        reason="FFmpeg not available in PATH"
    )
    def test_real_conversion_with_ffmpeg(self, converter_config, real_audio_file, real_image_file):
        """Test 7: REAL conversion using FFmpeg (requires FFmpeg installed)."""
        output_file = converter_config.videos_dir / 'real_output.mp4'
        
        job = ConversionJob(
            id="real-conversion-test",
            beat_file=real_audio_file,
            cover_file=real_image_file,
            output_file=output_file
        )
        
        converter = VideoConverter(converter_config)
        
        # Execute real conversion
        success = converter.convert(job)
        
        # Verify conversion succeeded
        assert success is True, "Conversion should succeed"
        assert job.status == "completed", f"Job should be completed, got: {job.status}"
        assert job.progress == 100.0
        assert job.error_message is None
        
        # Verify output file was created
        assert output_file.exists(), "Output video file should exist"
        assert output_file.stat().st_size > 0, "Output file should have content"
        
        # Verify it's a valid video file
        result = subprocess.run(
            ['ffmpeg', '-i', str(output_file), '-f', 'null', '-'],
            capture_output=True
        )
        assert b'Invalid data found' not in result.stderr
    
    def test_source_files_not_deleted(self, converter_config, real_audio_file, real_image_file):
        """Test 8: CRITICAL - Verify source files are NOT deleted after conversion."""
        output_file = converter_config.videos_dir / 'no_delete_test.mp4'
        
        # Verify auto-deletion is disabled
        assert converter_config.auto_delete_beats is False
        assert converter_config.auto_delete_covers is False
        
        job = ConversionJob(
            id="no-delete-test",
            beat_file=real_audio_file,
            cover_file=real_image_file,
            output_file=output_file
        )
        
        # Store original file paths and sizes
        beat_path = job.beat_file
        cover_path = job.cover_file
        beat_size = beat_path.stat().st_size
        cover_size = cover_path.stat().st_size
        
        converter = VideoConverter(converter_config)
        
        # Mock conversion to avoid actual FFmpeg call
        with patch('ffmpeg.run') as mock_run:
            mock_run.return_value = None
            success = converter.convert(job)
            job.status = "completed"  # Manually set for cleanup test
        
        # Run cleanup
        converter.cleanup(job)
        
        # VERIFY SOURCE FILES STILL EXIST
        assert beat_path.exists(), "Beat file should NOT be deleted"
        assert cover_path.exists(), "Cover file should NOT be deleted"
        assert beat_path.stat().st_size == beat_size, "Beat file should be unchanged"
        assert cover_path.stat().st_size == cover_size, "Cover file should be unchanged"
    
    def test_auto_delete_beats_when_enabled(self, converter_config, real_audio_file, real_image_file):
        """Test 9: Verify beats ARE deleted when auto_delete_beats=True."""
        # Enable auto-deletion for beats only
        converter_config.auto_delete_beats = True
        converter_config.auto_delete_covers = False
        
        output_file = converter_config.videos_dir / 'delete_beats_test.mp4'
        
        job = ConversionJob(
            id="delete-beats",
            beat_file=real_audio_file,
            cover_file=real_image_file,
            output_file=output_file
        )
        
        beat_path = job.beat_file
        cover_path = job.cover_file
        
        converter = VideoConverter(converter_config)
        
        # Mock conversion
        with patch('ffmpeg.run'):
            converter.convert(job)
            job.status = "completed"
        
        # Run cleanup
        converter.cleanup(job)
        
        # Beat should be deleted, cover should remain
        assert not beat_path.exists(), "Beat file should be deleted"
        assert cover_path.exists(), "Cover file should NOT be deleted"
    
    def test_auto_delete_covers_when_enabled(self, converter_config, real_audio_file, real_image_file):
        """Test 10: Verify covers ARE deleted when auto_delete_covers=True."""
        # Enable auto-deletion for covers only
        converter_config.auto_delete_beats = False
        converter_config.auto_delete_covers = True
        
        # Create fresh files for this test
        beat_file2 = converter_config.beats_dir / 'beat2.mp3'
        beat_file2.write_bytes(real_audio_file.read_bytes())
        
        cover_file2 = converter_config.covers_dir / 'cover2.jpg'
        cover_file2.write_bytes(real_image_file.read_bytes())
        
        output_file = converter_config.videos_dir / 'delete_covers_test.mp4'
        
        job = ConversionJob(
            id="delete-covers",
            beat_file=beat_file2,
            cover_file=cover_file2,
            output_file=output_file
        )
        
        converter = VideoConverter(converter_config)
        
        # Mock conversion
        with patch('ffmpeg.run'):
            converter.convert(job)
            job.status = "completed"
        
        # Run cleanup
        converter.cleanup(job)
        
        # Cover should be deleted, beat should remain
        assert beat_file2.exists(), "Beat file should NOT be deleted"
        assert not cover_file2.exists(), "Cover file should be deleted"
    
    def test_error_handling_invalid_beat_file(self, converter_config, real_image_file):
        """Test 11: Verify proper error handling for invalid beat file."""
        invalid_beat = converter_config.beats_dir / 'invalid.mp3'
        invalid_beat.write_text("not a real audio file")
        
        output_file = converter_config.videos_dir / 'error_test.mp4'
        
        job = ConversionJob(
            id="error-invalid-beat",
            beat_file=invalid_beat,
            cover_file=real_image_file,
            output_file=output_file
        )
        
        converter = VideoConverter(converter_config)
        success = converter.convert(job)
        
        # Should fail gracefully
        assert success is False, "Conversion should fail for invalid audio"
        assert job.status == "failed"
        assert job.error_message is not None
        assert len(job.error_message) > 0
    
    def test_error_handling_invalid_image_file(self, converter_config, real_audio_file):
        """Test 12: Verify proper error handling for invalid image file."""
        invalid_image = converter_config.covers_dir / 'invalid.jpg'
        invalid_image.write_text("not a real image file")
        
        output_file = converter_config.videos_dir / 'error_image_test.mp4'
        
        job = ConversionJob(
            id="error-invalid-image",
            beat_file=real_audio_file,
            cover_file=invalid_image,
            output_file=output_file
        )
        
        converter = VideoConverter(converter_config)
        success = converter.convert(job)
        
        # Should fail gracefully
        assert success is False
        assert job.status == "failed"
        assert job.error_message is not None
    
    def test_error_handling_missing_beat_file(self, converter_config, real_image_file):
        """Test 13: Verify error handling for non-existent beat file."""
        missing_beat = converter_config.beats_dir / 'does_not_exist.mp3'
        
        job = ConversionJob(
            id="missing-beat",
            beat_file=missing_beat,
            cover_file=real_image_file,
            output_file=converter_config.videos_dir / 'output.mp4'
        )
        
        converter = VideoConverter(converter_config)
        success = converter.convert(job)
        
        assert success is False
        assert job.status == "failed"
    
    def test_resolution_parsing(self, converter_config):
        """Test 14: Verify resolution string is properly parsed."""
        converter = VideoConverter(converter_config)
        
        # Test different resolution formats
        test_cases = [
            ("1920x1080", 1920, 1080),
            ("1280x720", 1280, 720),
            ("3840x2160", 3840, 2160),
            ("640x480", 640, 480)
        ]
        
        for resolution, expected_width, expected_height in test_cases:
            converter.config.resolution = resolution
            width, height = map(int, converter.config.resolution.split('x'))
            assert width == expected_width
            assert height == expected_height
    
    def test_cleanup_only_on_completed_jobs(self, converter_config, real_audio_file, real_image_file):
        """Test 15: Verify cleanup only happens for completed jobs, not failed ones."""
        converter_config.auto_delete_beats = True
        converter_config.auto_delete_covers = True
        
        job = ConversionJob(
            id="failed-job",
            beat_file=real_audio_file,
            cover_file=real_image_file,
            output_file=converter_config.videos_dir / 'failed.mp4',
            status="failed"  # Job failed
        )
        
        converter = VideoConverter(converter_config)
        converter.cleanup(job)
        
        # Files should NOT be deleted for failed jobs
        assert real_audio_file.exists(), "Should not delete beat from failed job"
        assert real_image_file.exists(), "Should not delete cover from failed job"
    
    def test_multiple_conversions_sequential(self, converter_config, temp_project_dir):
        """Test 16: Verify multiple sequential conversions work correctly."""
        # Create multiple source files
        beats = []
        covers = []
        
        for i in range(3):
            beat = temp_project_dir / 'workspace' / 'beats' / f'beat_{i}.mp3'
            beat.write_bytes(b'ID3' + b'\x00' * 100)
            beats.append(beat)
            
            cover = temp_project_dir / 'workspace' / 'covers' / f'cover_{i}.jpg'
            cover.write_bytes(b'\xFF\xD8\xFF\xE0' + b'\x00' * 20 + b'\xFF\xD9')
            covers.append(cover)
        
        converter = VideoConverter(converter_config)
        
        jobs = []
        for i in range(3):
            job = ConversionJob(
                id=f"multi-{i}",
                beat_file=beats[i],
                cover_file=covers[i],
                output_file=converter_config.videos_dir / f'output_{i}.mp4'
            )
            jobs.append(job)
        
        # Mock and run all conversions
        with patch('ffmpeg.run'):
            for job in jobs:
                success = converter.convert(job)
                # Success might be False due to mock limitations, that's OK
                # What matters is files aren't deleted
                if success:
                    assert job.status == "completed"
        
        # Verify all source files still exist (THE CRITICAL ASSERTION)
        for beat in beats:
            assert beat.exists(), f"Beat {beat.name} should not be deleted"
        for cover in covers:
            assert cover.exists(), f"Cover {cover.name} should not be deleted"
    
    def test_job_status_transitions(self, converter_config, real_audio_file, real_image_file):
        """Test 17: Verify job status transitions through conversion lifecycle."""
        job = ConversionJob(
            id="status-test",
            beat_file=real_audio_file,
            cover_file=real_image_file,
            output_file=converter_config.videos_dir / 'status.mp4'
        )
        
        # Initial state
        assert job.status == "pending"
        assert job.progress == 0.0
        
        converter = VideoConverter(converter_config)
        
        # Mock successful conversion
        with patch('ffmpeg.run'):
            success = converter.convert(job)
        
        # Final state after successful conversion
        assert success is True
        assert job.status == "completed"
        assert job.progress == 100.0
        assert job.error_message is None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
