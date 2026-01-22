"""Configuration management with validation."""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Lightweight JSON configuration manager with schema validation."""
    
    def __init__(self, config_path: Path, schema: Dict[str, Any]):
        """
        Initialize ConfigManager.
        
        Args:
            config_path: Path to JSON configuration file
            schema: Schema with default values
        """
        self.path = Path(config_path)
        self.schema = schema
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        if not self.path.exists():
            return self._deep_copy(self.schema)
        
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self._validate(data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Error loading {self.path}: {e}. Using defaults.")
            return self._deep_copy(self.schema)
    
    def _deep_copy(self, obj: Any) -> Any:
        """Deep copy to avoid shared references."""
        if isinstance(obj, dict):
            return {k: self._deep_copy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._deep_copy(item) for item in obj]
        else:
            return obj
    
    def _validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and merge data with schema."""
        config = self._deep_copy(self.schema)
        self._merge_dicts(config, data)
        return config
    
    def _merge_dicts(self, base: Dict[str, Any], updates: Dict[str, Any]) -> None:
        """Recursively merge updates into base."""
        for key, value in updates.items():
            if key in base:
                if isinstance(base[key], dict) and isinstance(value, dict):
                    self._merge_dicts(base[key], value)
                else:
                    base[key] = value
            else:
                base[key] = value
    
    def save(self) -> None:
        """Save current configuration to file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Key to retrieve
            default: Default value if key doesn't exist
        
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value and save.
        
        Args:
            key: Key to set
            value: Value to set
        """
        self.config[key] = value
        self.save()
    
    def update(self, key: str, value: Any) -> None:
        """
        Update a first-level key and save.
        
        Args:
            key: Key to update
            value: New value
        """
        if key in self.schema:
            self.config[key] = value
            self.save()
        else:
            print(f"Warning: Key '{key}' not in schema")
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self.config = self._load_config()


__all__ = ['ConfigManager']
