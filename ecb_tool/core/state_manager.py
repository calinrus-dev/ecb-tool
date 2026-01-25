"""
Centralized State Management for ECB Tool.
Handles tracking of jobs, conversions, uploads, and persistence via CSV/JSON.
"""
import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

from ecb_tool.core.paths import get_paths

class StateManager:
    """
    Manages application state persistence including:
    - Conversion history (CSV)
    - Upload history (CSV)
    - Feature states (JSON) e.g., used covers index
    """
    
    def __init__(self):
        self.paths = get_paths()
        self._ensure_files()
        
    def _ensure_files(self):
        """Ensure storage files exist with correct headers."""
        # Conversion State CSV
        if not self.paths.conversion_state.exists():
            self._init_csv(self.paths.conversion_state, [
                'timestamp', 'job_id', 'beat_name', 'cover_name', 
                'output_file', 'status', 'error_message'
            ])
            
        # Upload State CSV
        if not self.paths.upload_state.exists():
            self._init_csv(self.paths.upload_state, [
                'timestamp', 'job_id', 'video_file', 'video_id', 
                'title', 'status', 'error_message'
            ])
            
        # General State JSON (for counters, indices, etc)
        # Using a general state file in config dir
        self.state_json_path = self.paths.config / 'app_state.json'
        if not self.state_json_path.exists():
            self._save_json(self.state_json_path, {
                'cover_sequential_index': 0,
                'used_covers_no_repeat': []
            })

    def _init_csv(self, path: Path, headers: List[str]):
        """Initialize a CSV file with headers."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def _save_json(self, path: Path, data: Dict[str, Any]):
        """Save data to JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
    def _load_json(self, path: Path) -> Dict[str, Any]:
        """Load data from JSON file."""
        if not path.exists():
            return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading state JSON {path}: {e}")
            return {}

    # --- Conversion State ---
    
    def log_conversion(self, job_id: str, beat: str, cover: str, output: str, status: str, error: str = ""):
        """Log a conversion event to CSV."""
        with open(self.paths.conversion_state, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                job_id, beat, cover, output, status, error
            ])
            
    # --- Upload State ---
    
    def log_upload(self, job_id: str, video: str, video_id: str, title: str, status: str, error: str = ""):
        """Log an upload event to CSV."""
        with open(self.paths.upload_state, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                job_id, video, video_id, title, status, error
            ])

    # --- Cover Selection State ---

    def get_sequential_cover_index(self) -> int:
        """Get the current index for sequential cover selection."""
        state = self._load_json(self.state_json_path)
        return state.get('cover_sequential_index', 0)
    
    def set_sequential_cover_index(self, index: int):
        """Update the index for sequential cover selection."""
        state = self._load_json(self.state_json_path)
        state['cover_sequential_index'] = index
        self._save_json(self.state_json_path, state)
        
    def get_used_covers(self) -> List[str]:
        """Get list of already used covers for No-Repeat mode."""
        state = self._load_json(self.state_json_path)
        return state.get('used_covers_no_repeat', [])
        
    def add_used_cover(self, cover_name: str):
        """Add a cover to the used list."""
        state = self._load_json(self.state_json_path)
        used = state.get('used_covers_no_repeat', [])
        if cover_name not in used:
            used.append(cover_name)
        state['used_covers_no_repeat'] = used
        self._save_json(self.state_json_path, state)
        
    def reset_used_covers(self):
        """Reset the used covers list."""
        state = self._load_json(self.state_json_path)
        state['used_covers_no_repeat'] = []
        self._save_json(self.state_json_path, state)

# Global Instance
_state_manager = None

def get_state_manager() -> StateManager:
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager
