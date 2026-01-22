"""
Settings management feature.
"""

from pathlib import Path
from typing import Dict, Any

from ecb_tool.core.config import ConfigManager
from ecb_tool.core.paths import get_paths


class SettingsManager:
    """Centralized settings management."""
    
    def __init__(self):
        """Initialize settings manager."""
        self.paths = get_paths()
        self._configs: Dict[str, ConfigManager] = {}
    
    def get_conversion_settings(self) -> ConfigManager:
        """Get conversion settings."""
        if 'conversion' not in self._configs:
            schema = {
                "rutas": {
                    "beats_entrada": "workspace/beats/",
                    "portadas_entrada": "workspace/covers/",
                    "videos_salida": "workspace/videos/",
                },
                "conversion": {
                    "bpv": 1,
                    "lotes": 2,
                    "resolucion": "1920x1080",
                    "fps": 30,
                    "bitrate_video": "2M",
                    "bitrate_audio": "192k",
                    "formato_video": "mp4",
                    "formato_audio": "aac",
                    "fade_in_duration": 2.0,
                    "fade_out_duration": 2.0,
                    "enable_fades": True,
                    "autoborrado_beats": False,
                    "autoborrado_portadas": False,
                }
            }
            self._configs['conversion'] = ConfigManager(
                self.paths.conversion_config, schema
            )
        
        return self._configs['conversion']
    
    def get_upload_settings(self) -> ConfigManager:
        """Get upload settings."""
        if 'upload' not in self._configs:
            schema = {
                "subida": {
                    "modo": "programado",
                    "hora_subida": "12:00",
                    "autoborrado_videos": False,
                    "papelera_videos": False,
                    "estado": "publico",
                    "contenido_niños": False,
                }
            }
            self._configs['upload'] = ConfigManager(
                self.paths.upload_config, schema
            )
        
        return self._configs['upload']
    
    def get_order_settings(self) -> ConfigManager:
        """Get order/process settings."""
        if 'order' not in self._configs:
            schema = {
                "modo": "Convert",
                "ordenes": 1,
                "auto": True,
                "proceso": False,
                "videos_convertidos": 0,
                "videos_subidos": 0,
                "bpv": 1,
                "cover_mode": "Random",
            }
            self._configs['order'] = ConfigManager(
                self.paths.order_config, schema
            )
        
        return self._configs['order']


__all__ = ['SettingsManager']
