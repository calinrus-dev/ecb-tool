"""Video converter using FFmpeg."""

import subprocess
from pathlib import Path
from typing import List, Optional
import ffmpeg

from ecb_tool.core.paths import get_paths
from ecb_tool.features.conversion.models import ConversionConfig, ConversionJob


class VideoConverter:
    """Handles video conversion from beats and covers."""
    
    def __init__(self, config: ConversionConfig):
        """
        Initialize VideoConverter.
        
        Args:
            config: Conversion configuration
        """
        self.config = config
        self.paths = get_paths()
    
    def list_beats(self) -> List[Path]:
        """List all available beat files."""
        extensions = {'.mp3', '.wav', '.flac', '.m4a', '.aac'}
        beats = []
        
        if self.config.beats_dir.exists():
            for file in self.config.beats_dir.iterdir():
                if file.suffix.lower() in extensions and not file.name.startswith('.'):
                    beats.append(file)
        
        return sorted(beats)
    
    def list_covers(self) -> List[Path]:
        """List all available cover image files."""
        extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        covers = []
        
        if self.config.covers_dir.exists():
            for file in self.config.covers_dir.iterdir():
                if file.suffix.lower() in extensions and not file.name.startswith('.'):
                    covers.append(file)
        
        return sorted(covers)
    
    def convert(self, job: ConversionJob) -> bool:
        """
        Convert a single beat+cover to video.
        
        Args:
            job: Conversion job to process
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure output directory exists
            job.output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Parse resolution
            width, height = map(int, self.config.resolution.split('x'))
            
            # Build FFmpeg command
            stream = (
                ffmpeg
                .input(str(job.cover_file), loop=1, framerate=self.config.fps)
                .input(str(job.beat_file))
                .output(
                    str(job.output_file),
                    vcodec='libx264',
                    acodec=self.config.audio_format,
                    video_bitrate=self.config.video_bitrate,
                    audio_bitrate=self.config.audio_bitrate,
                    s=f'{width}x{height}',
                    shortest=None,
                    pix_fmt='yuv420p'
                )
                .overwrite_output()
            )
            
            # Run conversion
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            
            job.status = "completed"
            job.progress = 100.0
            return True
            
        except ffmpeg.Error as e:
            job.status = "failed"
            job.error_message = f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}"
            return False
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            return False
    
    def cleanup(self, job: ConversionJob) -> None:
        """
        Clean up processed files if configured.
        
        Args:
            job: Completed conversion job
        """
        if job.status == "completed":
            if self.config.auto_delete_beats and job.beat_file.exists():
                job.beat_file.unlink()
            
            if self.config.auto_delete_covers and job.cover_file.exists():
                job.cover_file.unlink()


__all__ = ['VideoConverter']
