from PyQt6.QtCore import QThread, pyqtSignal
from ecb_tool.features.conversion.runner import ConversionRunner

class ConversionWorker(QThread):
    progress_signal = pyqtSignal(str, float)
    status_signal = pyqtSignal(str, str)
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, num_orders: int, parent=None):
        super().__init__(parent)
        self.num_orders = num_orders
        self.runner = ConversionRunner()
        
        if hasattr(self.runner, 'converter'):
            self.runner.converter.on_progress = self._on_progress
            self.runner.converter.on_status_change = self._on_status
    
    def _on_progress(self, job_id, percent):
        self.progress_signal.emit(job_id, percent)
        
    def _on_status(self, job_id, status):
        self.status_signal.emit(job_id, status)
        
    def run(self):
        self.log_signal.emit("🚀 Iniciando proceso de conversión...")
        try:
            self.runner.run(self.num_orders)
            self.log_signal.emit("✅ Proceso finalizado.")
        except Exception as e:
            self.log_signal.emit(f"❌ Error crítico: {str(e)}")
        finally:
            self.finished_signal.emit()

    def stop(self):
        if self.runner:
            self.runner.paths.stop_flag.touch()
