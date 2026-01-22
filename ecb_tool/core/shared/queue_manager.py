"""Sistema de gestión de colas de conversión y subida."""
import os
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class QueueStatus(Enum):
    """Estados de la cola."""
    WAITING = "waiting"  # Esperando
    READY = "ready"  # Lista para ejecutar
    RUNNING = "running"  # En ejecución
    PAUSED = "paused"  # Pausada
    COMPLETED = "completed"  # Completada
    ERROR = "error"  # Error
    MISSING_FILES = "missing_files"  # Faltan archivos


class TaskType(Enum):
    """Tipos de tarea."""
    CONVERSION = "conversion"
    UPLOAD = "upload"


@dataclass
class QueueTask:
    """Tarea individual en la cola."""
    id: str
    type: TaskType
    file_path: str
    status: QueueStatus
    progress: int = 0
    error_message: Optional[str] = None
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def to_dict(self):
        """Convierte a diccionario."""
        data = asdict(self)
        data['type'] = self.type.value
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Crea desde diccionario."""
        data['type'] = TaskType(data['type'])
        data['status'] = QueueStatus(data['status'])
        return cls(**data)


class QueueManager:
    """Gestor de colas de procesamiento."""
    
    def __init__(self, queue_file="queue_state.json"):
        self.queue_file = os.path.join("config", queue_file)
        self.conversion_queue: List[QueueTask] = []
        self.upload_queue: List[QueueTask] = []
        self._load_state()
    
    def _load_state(self):
        """Carga el estado de las colas."""
        if os.path.exists(self.queue_file):
            try:
                with open(self.queue_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversion_queue = [QueueTask.from_dict(t) for t in data.get('conversion', [])]
                    self.upload_queue = [QueueTask.from_dict(t) for t in data.get('upload', [])]
            except Exception:
                pass
    
    def _save_state(self):
        """Guarda el estado de las colas."""
        os.makedirs(os.path.dirname(self.queue_file), exist_ok=True)
        data = {
            'conversion': [t.to_dict() for t in self.conversion_queue],
            'upload': [t.to_dict() for t in self.upload_queue],
            'updated_at': datetime.now().isoformat()
        }
        with open(self.queue_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_task(self, task: QueueTask):
        """Añade una tarea a la cola correspondiente."""
        if task.type == TaskType.CONVERSION:
            self.conversion_queue.append(task)
        else:
            self.upload_queue.append(task)
        self._save_state()
    
    def remove_task(self, task_id: str, task_type: TaskType):
        """Elimina una tarea de la cola."""
        if task_type == TaskType.CONVERSION:
            self.conversion_queue = [t for t in self.conversion_queue if t.id != task_id]
        else:
            self.upload_queue = [t for t in self.upload_queue if t.id != task_id]
        self._save_state()
    
    def get_next_task(self, task_type: TaskType) -> Optional[QueueTask]:
        """Obtiene la siguiente tarea pendiente."""
        queue = self.conversion_queue if task_type == TaskType.CONVERSION else self.upload_queue
        for task in queue:
            if task.status == QueueStatus.WAITING or task.status == QueueStatus.READY:
                return task
        return None
    
    def update_task_status(self, task_id: str, status: QueueStatus, progress: int = None, error: str = None):
        """Actualiza el estado de una tarea."""
        for queue in [self.conversion_queue, self.upload_queue]:
            for task in queue:
                if task.id == task_id:
                    task.status = status
                    if progress is not None:
                        task.progress = progress
                    if error:
                        task.error_message = error
                    if status == QueueStatus.RUNNING and not task.started_at:
                        task.started_at = datetime.now().isoformat()
                    elif status == QueueStatus.COMPLETED:
                        task.completed_at = datetime.now().isoformat()
                    self._save_state()
                    return
    
    def get_queue_stats(self, task_type: TaskType) -> Dict:
        """Obtiene estadísticas de la cola."""
        queue = self.conversion_queue if task_type == TaskType.CONVERSION else self.upload_queue
        total = len(queue)
        waiting = sum(1 for t in queue if t.status == QueueStatus.WAITING)
        running = sum(1 for t in queue if t.status == QueueStatus.RUNNING)
        completed = sum(1 for t in queue if t.status == QueueStatus.COMPLETED)
        errors = sum(1 for t in queue if t.status == QueueStatus.ERROR)
        
        return {
            'total': total,
            'waiting': waiting,
            'running': running,
            'completed': completed,
            'errors': errors,
            'progress': int((completed / total * 100)) if total > 0 else 0
        }
    
    def clear_completed(self, task_type: TaskType):
        """Limpia las tareas completadas."""
        if task_type == TaskType.CONVERSION:
            self.conversion_queue = [t for t in self.conversion_queue if t.status != QueueStatus.COMPLETED]
        else:
            self.upload_queue = [t for t in self.upload_queue if t.status != QueueStatus.COMPLETED]
        self._save_state()
    
    def has_errors(self, task_type: TaskType) -> bool:
        """Verifica si hay errores en la cola."""
        queue = self.conversion_queue if task_type == TaskType.CONVERSION else self.upload_queue
        return any(t.status == QueueStatus.ERROR for t in queue)
    
    def is_queue_completed(self, task_type: TaskType) -> bool:
        """Verifica si la cola está completada."""
        queue = self.conversion_queue if task_type == TaskType.CONVERSION else self.upload_queue
        if not queue:
            return False
        return all(t.status == QueueStatus.COMPLETED for t in queue)


# Instancia global
_queue_manager = None

def get_queue_manager():
    """Obtiene la instancia del gestor de colas."""
    global _queue_manager
    if _queue_manager is None:
        _queue_manager = QueueManager()
    return _queue_manager
