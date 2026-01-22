"""Pantalla de configuración de conversión FFMPEG."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.shared.theme_manager import get_theme_manager
from ecb_tool.core.shared.navigation import get_navigation_manager
from ecb_tool.core.shared.language_manager import get_language_manager
from ecb_tool.features.ui.blocks.ffmpeg_settings_dialog import FFmpegSettingsDialog


class FFmpegSettingsScreen(QWidget):
    """Pantalla de configuración de conversión."""
    
    def __init__(self):
        super().__init__()
        self.screen_adapter = get_screen_adapter()
        self.theme_manager = get_theme_manager()
        self.navigation = get_navigation_manager()
        self.language_manager = get_language_manager()
        self._init_ui()
        self._apply_theme()
        self.theme_manager.theme_changed.connect(self._apply_theme)
    
    def _init_ui(self):
        """Inicializa la interfaz."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header con botón volver
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        margin = self.screen_adapter.get_margin(20)
        header_layout.setContentsMargins(margin, margin, margin, int(margin*0.5))
        
        back_btn = QPushButton("✕")
        back_btn.setFixedSize(self.screen_adapter.scale(40), self.screen_adapter.scale(40))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a2a;
                color: #ff6b6b;
                border: 2px solid #3a3a3a;
                border-radius: 20px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff6b6b;
                color: #fff;
                border-color: #ff6b6b;
            }
        """)
        back_btn.clicked.connect(self.navigation.back)
        header_layout.addWidget(back_btn)
        
        title = QLabel(self.language_manager.get_text('conversion_settings'))
        font_size = self.screen_adapter.get_font_size(24)
        title.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title, 1)
        
        spacer = QWidget()
        spacer.setFixedWidth(self.screen_adapter.scale(40))
        header_layout.addWidget(spacer)
        
        layout.addWidget(header_container)
        
        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(2)
        layout.addWidget(sep)
        
        # Scroll para el diálogo embebido
        from PyQt6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Usar el diálogo como widget embebido
        self.settings_dialog = FFmpegSettingsDialog(None)
        self.settings_dialog.setWindowFlags(Qt.WindowType.Widget)
        scroll.setWidget(self.settings_dialog)
        layout.addWidget(scroll)
        
        # Separador
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setFixedHeight(2)
        layout.addWidget(sep2)
        
        # Botones de acción
        buttons_container = QWidget()
        buttons = QHBoxLayout(buttons_container)
        margin = self.screen_adapter.get_margin(20)
        buttons.setContentsMargins(margin, int(margin*0.7), margin, int(margin*0.7))
        buttons.setSpacing(self.screen_adapter.get_spacing(12))
        
        # Botón cancelar
        cancel_btn = QPushButton(self.language_manager.get_text('cancel'))
        cancel_btn.setMinimumHeight(self.screen_adapter.scale(45))
        cancel_btn.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(14), QFont.Weight.Bold))
        cancel_btn.clicked.connect(self.navigation.back)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #888;
                border: 2px solid #4a4a4a;
                border-radius: 8px;
                padding: 10px 20px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                color: #fff;
            }
        """)
        buttons.addStretch()
        buttons.addWidget(cancel_btn)
        
        # Botón guardar
        save_btn = QPushButton(self.language_manager.get_text('save_changes'))
        save_btn.setMinimumHeight(self.screen_adapter.scale(45))
        save_btn.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(14), QFont.Weight.Bold))
        save_btn.clicked.connect(self._save_settings)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #43b680;
                color: #fff;
                border: 2px solid #43b680;
                border-radius: 8px;
                padding: 10px 20px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #3a9d6f;
            }
        """)
        buttons.addWidget(save_btn)
        
        layout.addWidget(buttons_container)
    
    def _save_settings(self):
        """Guarda la configuración de FFmpeg."""
        # TODO: Implementar guardado
        self.navigation.back()
    
    def _apply_theme(self):
        """Aplica el tema."""
        theme = self.theme_manager.get_current_theme()
        self.setStyleSheet(f"""
            QWidget {{
                background: {theme['background']};
                color: {theme['text']};
            }}
            QFrame[frameShape="4"] {{
                background-color: {theme['border']};
            }}
        """)

