"""Video converter using FFmpeg."""

import subprocess
from pathlib import Path
from typing import List, Optional
import ffmpeg

from ecb_tool.core.paths import get_paths
from ecb_tool.features.conversion.models import ConversionConfig, ConversionJob


class VideoConverter:
    """Handles video conversion from beats and covers."""
    
    def __init__(self, config: ConversionConfig, on_progress=None):
        self.config = config
        self.paths = get_paths()
        self.on_progress = on_progress
    
    def convert(self, job: ConversionJob) -> bool:
        """
        Convert beats + cover to video.
        Supports BPV (Beats Per Video) via concatenation.
        """
        try:
            job.output_file.parent.mkdir(parents=True, exist_ok=True)
            width, height = map(int, self.config.resolution.split('x'))
            
            # Prepare Logic for Multiple Beats
            audio_inputs = []
            total_duration_est = 0
            
            for beat in job.beat_files:
                inp = ffmpeg.input(str(beat))
                audio_inputs.append(inp)
                # Note: Getting duration requires probing, might slow down start. 
                # For concat, we usually just concat streams.
                
            # Concatenate Audio if > 1
            if len(audio_inputs) > 1:
                # [0:a][1:a]...concat=n=N:v=0:a=1[outa]
                audio_stream = ffmpeg.concat(*audio_inputs, v=0, a=1).node[0]
            elif len(audio_inputs) == 1:
                audio_stream = audio_inputs[0]
            else:
                raise ValueError("No beat files provided for job.")

            # Input Cover (Loop)
            # We rely on 'shortest=False' (default) but since image is infinite loop, 
            # we must set it to match audio duration.
            # However, ffmpeg 'shortest=1' makes output as short as shortest stream.
            # If we loop image, image stream is infinite. Audio is finite.
            # So shortest=1 should work to cut video when audio ends.
            video_stream = ffmpeg.input(str(job.cover_file), loop=1, framerate=self.config.fps)
            
            # Output
            out = ffmpeg.output(
                video_stream,
                audio_stream,
                str(job.output_file),
                vcodec='libx264',
                acodec=self.config.audio_format,
                video_bitrate=self.config.video_bitrate,
                audio_bitrate=self.config.audio_bitrate,
                s=f'{width}x{height}',
                pix_fmt='yuv420p',
                shortest=None # We use -shortest argument in .global_args usually vs kwargs
            )
            
            # Add global args
            out = out.global_args('-shortest') # Cut when shorter stream (audio) ends
            out = out.overwrite_output()
            
            # Run
            process = ffmpeg.run_async(out, pipe_stdout=True, pipe_stderr=True)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                raise ffmpeg.Error('ffmpeg', stdout, stderr)
            
            if self.on_progress:
                self.on_progress(job.id, 100.0)
            
            job.status = "completed"
            job.progress = 100.0
            return True
            
        except ffmpeg.Error as e:
            job.status = "failed"
            error_msg = e.stderr.decode() if e.stderr else str(e)
            job.error_message = f"FFmpeg error: {error_msg}"
            return False
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            return False

__all__ = ['VideoConverter']
