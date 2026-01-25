"""
Conversion Page.
Handles beat management, configuration, and conversion execution.
"""
import shutil
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QListWidget, QGroupBox, QFormLayout, QComboBox, QSpinBox,
    QTextEdit, QFileDialog, QSplitter
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

from ecb_tool.core.paths import get_paths
from ecb_tool.features.conversion.worker import ConversionWorker
from ecb_tool.core.config import ConfigManager

class ConversionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.paths = get_paths()
        self.worker = None
        self.init_ui()
        self.load_beats()
        
    def init_ui(self):
        """Initialize the UI layout."""
        layout = QHBoxLayout(self)
        
        # Splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # --- Left Panel: Beats Queue ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Header
        header = QLabel("🎵 Cola de Beats")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        left_layout.addWidget(header)
        
        # Drag & Drop Area / List
        self.beats_list = QListWidget()
        self.beats_list.setDragDropMode(QListWidget.DragDropMode.DropOnly)
        self.beats_list.setAcceptDrops(True)
        self.beats_list.dragEnterEvent = self.drag_enter_event
        self.beats_list.dropEvent = self.drop_event
        left_layout.addWidget(self.beats_list)
        
        # Queue Actions
        btn_clear = QPushButton("Limpiar Cola")
        btn_clear.clicked.connect(self.clear_queue)
        left_layout.addWidget(btn_clear)
        
        splitter.addWidget(left_panel)
        
        # --- Right Panel: Controls ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Configuration Group
        config_group = QGroupBox("⚙️ Configuración")
        form_layout = QFormLayout(config_group)
        
        self.combo_res = QComboBox()
        self.combo_res.addItems(["1920x1080", "1280x720", "3840x2160"])
        form_layout.addRow("Resolución:", self.combo_res)
        
        self.spin_fps = QSpinBox()
        self.spin_fps.setRange(24, 60)
        self.spin_fps.setValue(30)
        form_layout.addRow("FPS:", self.spin_fps)
        
        self.spin_orders = QSpinBox()
        self.spin_orders.setRange(1, 100)
        self.spin_orders.setValue(1)
        form_layout.addRow("Órdenes:", self.spin_orders)
        
        right_layout.addWidget(config_group)
        
        # Actions
        self.btn_start = QPushButton("🚀 Iniciar Conversión")
        self.btn_start.setProperty("class", "primary")
        self.btn_start.setMinimumHeight(50)
        self.btn_start.clicked.connect(self.start_conversion)
        right_layout.addWidget(self.btn_start)
        
        # Log Output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Registro de procesos...")
        right_layout.addWidget(self.log_output)
        
        splitter.addWidget(right_panel)
        
        # Set splitter sizes (40% left, 60% right)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
        
    def load_beats(self):
        """Load beats from workspace."""
        self.beats_list.clear()
        if self.paths.beats.exists():
            for f in self.paths.beats.iterdir():
                if f.suffix.lower() in ['.mp3', '.wav', '.flac']:
                    self.beats_list.addItem(f.name)
    
    def drag_enter_event(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def drop_event(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            path = Path(f)
            if path.suffix.lower() in ['.mp3', '.wav', '.flac']:
                # Copy to/Work in beats dir
                target = self.paths.beats / path.name
                if not target.exists():
                    shutil.copy2(path, target)
        self.load_beats()
        
    def clear_queue(self):
        """Clear beats from workspace."""
        if self.paths.beats.exists():
            for f in self.paths.beats.iterdir():
                try:
                    f.unlink()
                except Exception:
                    pass
        self.load_beats()
        
    def log(self, message: str):
        """Add message to log."""
        self.log_output.append(message)
        
    def start_conversion(self):
        """Start conversion process."""
        num_orders = self.spin_orders.value()
        
        # Save config (simple update for now)
        # Ideally we update the JSON file here via ConfigManager
        
        self.btn_start.setEnabled(False)
        self.beats_list.setEnabled(False)
        self.log("🚀 Iniciando worker...")
        
        self.worker = ConversionWorker(num_orders, self)
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.on_conversion_finished)
        self.worker.start()
        
    def on_conversion_finished(self):
        self.log("🏁 Proceso finalizado.")
        self.btn_start.setEnabled(True)
        self.beats_list.setEnabled(True)
        self.load_beats()  # Refresh list (some might be deleted)
