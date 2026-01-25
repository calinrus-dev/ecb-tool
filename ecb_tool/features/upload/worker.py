from PyQt6.QtCore import QThread, pyqtSignal
from ecb_tool.features.upload.uploader import VideoUploader
from ecb_tool.features.upload.models import UploadJob, UploadConfig
from ecb_tool.core.paths import get_paths

class UploadWorker(QThread):
    progress_signal = pyqtSignal(str, float)
    status_signal = pyqtSignal(str, str)
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, jobs: list[UploadJob], config: UploadConfig, parent=None):
        super().__init__(parent)
        self.jobs = jobs
        self.config = config
        self.uploader = VideoUploader(config)
        self.should_stop = False
        
    def run(self):
        self.log_signal.emit("🚀 Iniciando carga a YouTube...")
        
        for job in self.jobs:
            if self.should_stop:
                break
                
            self.log_signal.emit(f"📤 Subiendo: {job.video_file.name}")
            self.status_signal.emit(job.id, "uploading")
            
            # Since uploader.upload is synchronous and blocks, we can't easily get fine-grained progress 
            # unless we modify uploader.py to accept callbacks (like we did for converter).
            # For now we'll wrap it.
            
            success = self.uploader.upload(job)
            
            if success:
                self.log_signal.emit(f"✅ Subido correctamente: {job.video_id}")
                self.progress_signal.emit(job.id, 100.0)
                self.status_signal.emit(job.id, "completed")
                
                # Cleanup
                self.uploader.cleanup(job)
            else:
                self.log_signal.emit(f"❌ Error al subir {job.video_file.name}: {job.error_message}")
                self.status_signal.emit(job.id, "failed")
                
        self.finished_signal.emit()

    def stop(self):
        self.should_stop = True
