import os
import json
import shutil
from pathlib import Path
from datetime import datetime

class ProjectManager:
    """Core logic for managing ECB Tool projects."""
    
    REQUIRED_FOLDERS = [
        "beats",
        "covers",
        "videos",
        "templates",
        "output"
    ]
    
    def __init__(self, workspace_root="workspace"):
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        
    def create_project(self, name, description="", settings=None):
        """Creates a new project structure."""
        project_id = name.lower().replace(" ", "_").strip()
        project_path = self.workspace_root / project_id
        
        if project_path.exists():
            raise FileExistsError(f"Project '{name}' already exists.")
            
        # Create folders
        for folder in self.REQUIRED_FOLDERS:
            (project_path / folder).mkdir(parents=True)
            
        # Create metadata
        metadata = {
            "id": project_id,
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "settings": settings or {},
            "status": "active"
        }
        
        self._save_metadata(project_path, metadata)
        return project_path
    
    def list_projects(self):
        """Returns list of valid projects."""
        projects = []
        if not self.workspace_root.exists():
            return []
            
        for child in self.workspace_root.iterdir():
            if child.is_dir() and (child / "metadata.json").exists():
                try:
                    meta = self._load_metadata(child)
                    projects.append(meta)
                except Exception:
                    continue # Skip invalid projects
        return sorted(projects, key=lambda x: x['created_at'], reverse=True)
    
    def get_project_path(self, project_id):
        return self.workspace_root / project_id
        
    def _save_metadata(self, project_path, data):
        with open(project_path / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
    def _load_metadata(self, project_path):
        with open(project_path / "metadata.json", "r", encoding="utf-8") as f:
            return json.load(f)

# Singleton instance
project_manager = ProjectManager()
