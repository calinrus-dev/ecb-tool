"""
ECB Tool - Main Window (Nueva Estructura)
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class MainWindow(QWidget):
    """Ventana principal de ECB Tool"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar interfaz"""
        self.setWindowTitle("ECB TOOL - Professional Beat Converter")
        self.setMinimumSize(1000, 600)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("🎵 ECB TOOL")
        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Professional Beat to Video Converter & YouTube Uploader")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666;")
        layout.addWidget(subtitle)
        
        layout.addStretch(1)
        
        # Info de versión
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)
        
        status_label = QLabel("✅ Aplicación iniciada correctamente")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_label.setStyleSheet("color: green; font-size: 16px; font-weight: bold;")
        info_layout.addWidget(status_label)
        
        version_label = QLabel("Versión: 1.0.0-alpha | Nueva Arquitectura Feature-First")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #888; font-size: 12px;")
        info_layout.addWidget(version_label)
        
        layout.addLayout(info_layout)
        
        layout.addStretch(1)
        
        # Panel de módulos
        modules_layout = QVBoxLayout()
        modules_layout.setSpacing(15)
        
        modules_title = QLabel("Módulos Disponibles:")
        modules_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        modules_layout.addWidget(modules_title)
        
        # Importar y verificar módulos
        self.check_modules(modules_layout)
        
        layout.addLayout(modules_layout)
        
        layout.addStretch(2)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        convert_btn = QPushButton("🎬 Convertir Videos")
        convert_btn.setMinimumHeight(50)
        convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        convert_btn.clicked.connect(self.open_converter)
        buttons_layout.addWidget(convert_btn)
        
        upload_btn = QPushButton("📤 Subir a YouTube")
        upload_btn.setMinimumHeight(50)
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        upload_btn.clicked.connect(self.open_uploader)
        buttons_layout.addWidget(upload_btn)
        
        settings_btn = QPushButton("⚙️ Configuración")
        settings_btn.setMinimumHeight(50)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        settings_btn.clicked.connect(self.open_settings)
        buttons_layout.addWidget(settings_btn)
        
        layout.addLayout(buttons_layout)
        
        # Footer
        footer = QLabel("Nueva arquitectura - Feature-First | Tests incluidos | Rutas centralizadas")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #999; font-size: 11px; margin-top: 20px;")
        layout.addWidget(footer)
        
        # Aplicar estilo global
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                color: #333;
            }
        """)
    
    def check_modules(self, layout):
        """Verificar que los módulos están disponibles"""
        modules_status = []
        
        try:
            from ecb_tool.core.paths import get_paths
            paths = get_paths()
            modules_status.append(("✅", "Sistema de Rutas", "OK"))
        except Exception as e:
            modules_status.append(("❌", "Sistema de Rutas", str(e)))
        
        try:
            from ecb_tool.core.config import ConfigManager
            modules_status.append(("✅", "Gestor de Configuración", "OK"))
        except Exception as e:
            modules_status.append(("❌", "Gestor de Configuración", str(e)))
        
        try:
            from ecb_tool.features.conversion import VideoConverter
            modules_status.append(("✅", "Conversor de Videos", "OK"))
        except Exception as e:
            modules_status.append(("❌", "Conversor de Videos", str(e)))
        
        try:
            from ecb_tool.features.upload import VideoUploader
            modules_status.append(("✅", "YouTube Uploader", "OK"))
        except Exception as e:
            modules_status.append(("❌", "YouTube Uploader", str(e)))
        
        try:
            from ecb_tool.features.settings import SettingsManager
            modules_status.append(("✅", "Settings Manager", "OK"))
        except Exception as e:
            modules_status.append(("❌", "Settings Manager", str(e)))
        
        # Mostrar status
        for icon, name, status in modules_status:
            label = QLabel(f"{icon} {name}: {status}")
            label.setStyleSheet("font-size: 13px; padding: 3px;")
            layout.addWidget(label)
    
    def open_converter(self):
        """Abrir módulo de conversión"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Conversor",
            "Módulo de conversión de videos\n\n"
            "Próximamente: Interfaz completa de conversión\n"
            "Por ahora usa: python -m ecb_tool.features.conversion"
        )
    
    def open_uploader(self):
        """Abrir módulo de upload"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "YouTube Uploader",
            "Módulo de subida a YouTube\n\n"
            "Próximamente: Interfaz completa de upload\n"
            "Por ahora usa: python -m ecb_tool.features.upload"
        )
    
    def open_settings(self):
        """Abrir configuración"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Configuración",
            "Gestor de configuración\n\n"
            "Rutas centralizadas en: ecb_tool/core/paths.py\n"
            "Configs en: ecb_tool/core/config.py"
        )
