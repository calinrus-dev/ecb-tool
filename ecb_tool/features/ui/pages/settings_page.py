"""
Settings Page.
Global application settings and maintenance.
"""
import shutil
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, 
    QComboBox, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from ecb_tool.core.paths import get_paths
from ecb_tool.core.config import ConfigManager

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.paths = get_paths()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # General Settings
        group_general = QGroupBox("🛠️ General")
        form = QFormLayout(group_general)
        
        self.combo_cover_mode = QComboBox()
        self.combo_cover_mode.addItems(["Random", "Random (No Repeat)", "Sequential", "Select One"])
        self.combo_cover_mode.currentTextChanged.connect(self.save_defaults)
        form.addRow("Modo de Portada por Defecto:", self.combo_cover_mode)
        
        layout.addWidget(group_general)
        
        # Maintenance
        group_maint = QGroupBox("🧹 Mantenimiento")
        layout_maint = QVBoxLayout(group_maint)
        
        btn_clean_temp = QPushButton("Limpiar Archivos Temporales")
        btn_clean_temp.clicked.connect(self.clean_temp)
        layout_maint.addWidget(btn_clean_temp)
        
        btn_open_logs = QPushButton("📂 Abrir Carpeta de Logs")
        btn_open_logs.clicked.connect(self.open_logs)
        layout_maint.addWidget(btn_open_logs)
        
        layout.addWidget(group_maint)
        
        # About
        group_about = QGroupBox("ℹ️ Acerca de")
        layout_about = QVBoxLayout(group_about)
        layout_about.addWidget(QLabel("ECB TOOL Professional v2.0"))
        layout_about.addWidget(QLabel("Desarrollado para El Conde Beats"))
        layout.addWidget(group_about)
        
        layout.addStretch()
        
        # Load current defaults
        self.load_defaults()
        
    def load_defaults(self):
        order_schema = {"cover_mode": "Random"}
        config = ConfigManager(self.paths.order_config, order_schema)
        mode = config.get("cover_mode", "Random")
        self.combo_cover_mode.setCurrentText(mode)
        
    def save_defaults(self, text):
        order_schema = {"cover_mode": "Random"}
        config = ConfigManager(self.paths.order_config, order_schema)
        config.set("cover_mode", text)
        
    def clean_temp(self):
        confirm = QMessageBox.question(self, "Confirmar", "¿Borrar temporales y trash?")
        if confirm == QMessageBox.StandardButton.Yes:
            # Clean temp and trash
            for d in [self.paths.temp, self.paths.trash]:
                if d.exists():
                    shutil.rmtree(d)
                    d.mkdir()
            QMessageBox.information(self, "Listo", "Limpieza completada")

    def open_logs(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.paths.logs)))
