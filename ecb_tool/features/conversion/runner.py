"""Runner for video conversion process."""

import os
import sys
import time
import random
from pathlib import Path
from typing import List, Optional

from ecb_tool.core.paths import get_paths
from ecb_tool.core.config import ConfigManager
from ecb_tool.features.conversion.models import ConversionConfig, ConversionJob
from ecb_tool.features.conversion.converter import VideoConverter


class ConversionRunner:
    """Runs the conversion process based on configuration."""
    
    def __init__(self):
        """Initialize the conversion runner."""
        self.paths = get_paths()
        self._load_config()
        self._setup_converter()
        self.should_stop = False
        
    def _load_config(self):
        """Load conversion configuration."""
        config_schema = {
            "conversion": {
                "bpv": 1,
                "lotes": 2,
                "resolucion": "1920x1080",
                "fps": 30,
                "bitrate_video": "2M",
                "formato_video": "mp4",
                "bitrate_audio": "192k",
                "formato_audio": "aac",
                "autoborrado_beats": False,
                "papelera_beats": False,
                "autoborrado_portadas": False,
                "papelera_portadas": False
            }
        }
        
        self.config = ConfigManager(
            self.paths.conversion_config,
            config_schema
        )
    
    def _setup_converter(self):
        """Setup the video converter."""
        conv_settings = self.config.get("conversion", {})
        
        self.converter_config = ConversionConfig(
            beats_dir=self.paths.beats,
            covers_dir=self.paths.covers,
            videos_dir=self.paths.videos,
            resolution=conv_settings.get("resolucion", "1920x1080"),
            fps=conv_settings.get("fps", 30),
            video_bitrate=conv_settings.get("bitrate_video", "2M"),
            audio_bitrate=conv_settings.get("bitrate_audio", "192k"),
            audio_format=conv_settings.get("formato_audio", "aac"),
            video_format=conv_settings.get("formato_video", "mp4"),
            batch_size=conv_settings.get("lotes", 2),
            beats_per_video=conv_settings.get("bpv", 1),
            auto_delete_beats=conv_settings.get("autoborrado_beats", False),
            auto_delete_covers=conv_settings.get("autoborrado_portadas", False)
        )
        
        self.converter = VideoConverter(self.converter_config)
    
    def _select_cover(self, covers: List[Path], mode: str = "random") -> Path:
        """Select a cover based on mode."""
        if not covers:
            raise ValueError("No covers available")
        
        # Load cover mode from order config
        order_schema = {"cover_mode": "Random"}
        order_config = ConfigManager(self.paths.order_config, order_schema)
        cover_mode = order_config.get("cover_mode", "Random")
        
        if cover_mode == "Random":
            return random.choice(covers)
        elif cover_mode == "Random (No Repeat)":
            # TODO: Implement no-repeat logic with state tracking
            return random.choice(covers)
        elif cover_mode == "Select One":
            # TODO: Implement UI selection
            return covers[0]
        elif cover_mode == "Sequential":
            # TODO: Implement sequential with state tracking
            return covers[0]
        else:
            return random.choice(covers)
    
    def _create_jobs(self, num_orders: int = 1) -> List[ConversionJob]:
        """Create conversion jobs."""
        beats = self.converter.list_beats()
        covers = self.converter.list_covers()
        
        if not beats:
            print("⚠️ No hay beats disponibles")
            return []
        
        if not covers:
            print("⚠️ No hay portadas disponibles")
            return []
        
        bpv = self.converter_config.beats_per_video
        jobs = []
        
        for order in range(num_orders):
            if len(beats) < bpv:
                print(f"⚠️ No hay suficientes beats para la orden {order + 1}")
                break
            
            # Take beats for this job
            job_beats = beats[:bpv]
            beats = beats[bpv:]  # Remove used beats
            
            # Select cover
            try:
                cover = self._select_cover(covers)
            except ValueError as e:
                print(f"⚠️ Error seleccionando portada: {e}")
                break
            
            # Use first beat as main audio (if bpv=1) or combine later
            main_beat = job_beats[0]
            
            # Generate output filename
            output_name = f"{main_beat.stem}_video.{self.converter_config.video_format}"
            output_file = self.converter_config.videos_dir / output_name
            
            job = ConversionJob(
                id=f"job-{order + 1:03d}",
                beat_file=main_beat,
                cover_file=cover,
                output_file=output_file
            )
            
            jobs.append(job)
            print(f"✓ Orden {order + 1}: {main_beat.name} + {cover.name} → {output_name}")
        
        return jobs
    
    def _check_stop_flag(self) -> bool:
        """Check if stop flag exists."""
        return self.paths.stop_flag.exists()
    
    def run(self, num_orders: int = 1) -> None:
        """
        Run the conversion process.
        
        Args:
            num_orders: Number of videos to create
        """
        print("=" * 60)
        print("🎬 INICIANDO CONVERSIÓN DE VIDEOS")
        print("=" * 60)
        print(f"📊 Configuración:")
        print(f"  - Resolución: {self.converter_config.resolution}")
        print(f"  - FPS: {self.converter_config.fps}")
        print(f"  - Bitrate Video: {self.converter_config.video_bitrate}")
        print(f"  - Bitrate Audio: {self.converter_config.audio_bitrate}")
        print(f"  - Beats por video: {self.converter_config.beats_per_video}")
        print(f"  - Órdenes: {num_orders}")
        print("=" * 60)
        
        # Create jobs
        jobs = self._create_jobs(num_orders)
        
        if not jobs:
            print("\n❌ No se pudieron crear órdenes de conversión")
            return
        
        print(f"\n✓ {len(jobs)} órdenes creadas\n")
        
        # Process jobs
        completed = 0
        failed = 0
        
        for i, job in enumerate(jobs, 1):
            if self._check_stop_flag():
                print("\n⏹️ Proceso detenido por el usuario")
                break
            
            print(f"\n[{i}/{len(jobs)}] Procesando: {job.output_file.name}")
            print("-" * 60)
            
            job.status = "processing"
            success = self.converter.convert(job)
            
            if success:
                print(f"✅ Completado: {job.output_file.name}")
                completed += 1
                
                # Cleanup if configured
                self.converter.cleanup(job)
                
                # Update state
                self._update_state(job, "completed")
            else:
                print(f"❌ Error: {job.error_message}")
                failed += 1
                self._update_state(job, "failed")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE CONVERSIÓN")
        print("=" * 60)
        print(f"✅ Completados: {completed}")
        print(f"❌ Fallidos: {failed}")
        print(f"📁 Videos: {self.converter_config.videos_dir}")
        print("=" * 60)
    
    def _update_state(self, job: ConversionJob, status: str):
        """Update conversion state file."""
        # TODO: Implement state tracking in CSV
        pass


def main():
    """Main entry point for conversion runner."""
    # Load order configuration
    paths = get_paths()
    order_schema = {
        "modo": "convertir",
        "ordenes": 1,
        "proceso": False
    }
    order_config = ConfigManager(paths.order_config, order_schema)
    
    num_orders = order_config.get("ordenes", 1)
    
    try:
        runner = ConversionRunner()
        runner.run(num_orders)
    except KeyboardInterrupt:
        print("\n\n⏹️ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
