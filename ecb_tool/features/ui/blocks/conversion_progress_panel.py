"""Conversion progress panel widget."""

import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.shared.paths import ROOT_DIR, CONVERSION_STATE_CSV


class ConversionProgressPanel(QWidget):
    """Panel that shows real-time conversion progress."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen_adapter = get_screen_adapter()
        self.setObjectName("ConversionProgressPanel")
        
        self._init_ui()
        
        # Timer to update progress
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self._update_progress)
        self.update_timer.start(500)  # Update every 500ms
    
    def _init_ui(self):
        """Initialize UI."""
        self.setStyleSheet("""
            QWidget#ConversionProgressPanel {
                background-color: #141b28;
                border-radius: 18px;
                border: 1px solid #23304a;
            }
        """)
        
        layout = QVBoxLayout(self)
        margin = self.screen_adapter.get_margin(20)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(self.screen_adapter.get_spacing(15))
        
        # Title
        title = QLabel("📊 Progreso de Conversión")
        title.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(18), QFont.Weight.Bold))
        title.setStyleSheet("color: #24eaff;")
        layout.addWidget(title)
        
        # Current job info
        self.current_job_label = QLabel("Esperando...")
        self.current_job_label.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(13)))
        self.current_job_label.setStyleSheet("color: #8ad6ff;")
        layout.addWidget(self.current_job_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(self.screen_adapter.scale(30))
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #23304a;
                border-radius: 8px;
                background-color: #1a2332;
                text-align: center;
                color: #f4f8ff;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #24eaff, stop:1 #3998ff);
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Stats
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(self.screen_adapter.get_spacing(20))
        
        # Completed
        completed_frame = self._create_stat_frame("✅", "Completados", "0")
        stats_layout.addWidget(completed_frame)
        
        # Processing
        processing_frame = self._create_stat_frame("⚙️", "Procesando", "0")
        stats_layout.addWidget(processing_frame)
        
        # Failed
        failed_frame = self._create_stat_frame("❌", "Fallidos", "0")
        stats_layout.addWidget(failed_frame)
        
        layout.addLayout(stats_layout)
        
        # Store stat labels for updates
        self.completed_label = completed_frame.findChild(QLabel, "value")
        self.processing_label = processing_frame.findChild(QLabel, "value")
        self.failed_label = failed_frame.findChild(QLabel, "value")
    
    def _create_stat_frame(self, icon: str, label: str, value: str) -> QFrame:
        """Create a stat display frame."""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #1a2332;
                border: 1px solid #23304a;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Icon + Label
        header = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(16)))
        header.addWidget(icon_label)
        
        text_label = QLabel(label)
        text_label.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(12)))
        text_label.setStyleSheet("color: #8ad6ff;")
        header.addWidget(text_label)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(24), QFont.Weight.Bold))
        value_label.setStyleSheet("color: #f4f8ff;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        return frame
    
    def _update_progress(self):
        """Update progress from state file."""
        # TODO: Read from conversion_state.csv
        # For now, show placeholder data
        
        # Check if process is running
        from ecb_tool.core.shared.paths import get_paths
        from ecb_tool.core.config import ConfigManager
        
        paths = get_paths()
        order_config = ConfigManager(paths.order_config, {"proceso": False})
        
        is_running = order_config.get("proceso", False)
        
        if is_running:
            self.current_job_label.setText("🎬 Convirtiendo video...")
            # Simulate progress
            current = self.progress_bar.value()
            if current < 100:
                self.progress_bar.setValue(min(100, current + 5))
        else:
            if self.progress_bar.value() > 0:
                self.current_job_label.setText("✅ Proceso completado")
            else:
                self.current_job_label.setText("⏸️ Esperando inicio...")
    
    def reset(self):
        """Reset the progress panel."""
        self.progress_bar.setValue(0)
        self.current_job_label.setText("Esperando...")
        self.completed_label.setText("0")
        self.processing_label.setText("0")
        self.failed_label.setText("0")


__all__ = ["ConversionProgressPanel"]
