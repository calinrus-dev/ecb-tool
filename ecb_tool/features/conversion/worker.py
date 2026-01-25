from PyQt6.QtCore import QThread, pyqtSignal
from ecb_tool.core.paths import get_paths
from ecb_tool.features.conversion.converter import VideoConverter
from ecb_tool.features.conversion.models import ConversionConfig, ConversionJob
from pathlib import Path

class ConversionWorker(QThread):
    progress_signal = pyqtSignal(str, float) # job_id, percent
    status_signal = pyqtSignal(str, str)     # job_id, status
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, config: ConversionConfig, jobs: list[ConversionJob], parent=None):
        super().__init__(parent)
        self.config = config
        self.jobs = jobs
        self.stop_requested = False
        
    def run(self):
        self.log_signal.emit("🚀 Starting conversion process...")
        
        converter = VideoConverter(self.config, on_progress=self._on_progress_callback)
        
        for job in self.jobs:
            if self.stop_requested:
                break
                
            self.status_signal.emit(job.id, "Processing")
            self.log_signal.emit(f"Processing job: {job.id}")
            
            success = converter.convert(job)
            
            status = "Completed" if success else "Failed"
            self.status_signal.emit(job.id, status)
            
            if success:
                self.progress_signal.emit(job.id, 100.0)
            
        self.log_signal.emit("✅ Process finished.")
        self.finished_signal.emit()

    def _on_progress_callback(self, job_id, percent):
        self.progress_signal.emit(job_id, percent)

    def stop(self):
        self.stop_requested = True
