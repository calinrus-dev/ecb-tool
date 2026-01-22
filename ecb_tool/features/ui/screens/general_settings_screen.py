"""Pantalla de configuración general."""
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGroupBox, QGridLayout, QComboBox,
                             QScrollArea, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.shared.theme_manager import get_theme_manager
from ecb_tool.core.shared.navigation import get_navigation_manager
from ecb_tool.core.shared.language_manager import get_language_manager


class GeneralSettingsScreen(QWidget):
    """Pantalla de configuración general."""
    
    def __init__(self):
        super().__init__()
        self.screen_adapter = get_screen_adapter()
        self.theme_manager = get_theme_manager()
        self.navigation = get_navigation_manager()
        self.language_manager = get_language_manager()
        
        self._init_ui()
        self._apply_theme()
        self.theme_manager.theme_changed.connect(self._apply_theme)
        self.language_manager.language_changed.connect(self._on_language_changed)
    
    def _init_ui(self):
        """Inicializa la interfaz."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        content = QWidget()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        self.scroll = scroll
        self.content_widget = content
        
        self._build_content()
    
    def _build_content(self):
        """Construye el contenido de la pantalla."""
        # Limpiar layout anterior si existe
        if self.content_widget.layout():
            while self.content_widget.layout().count():
                item = self.content_widget.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        
        # Layout del contenido
        content_layout = QVBoxLayout(self.content_widget)
        margin = self.screen_adapter.get_margin(30)
        spacing = self.screen_adapter.get_spacing(20)
        content_layout.setContentsMargins(margin, margin, margin, margin)
        content_layout.setSpacing(spacing)
        
        # Header con botón volver
        header = QHBoxLayout()
        
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
        header.addWidget(back_btn)
        
        title = QLabel(self.language_manager.get_text('general_config'))
        font_size = self.screen_adapter.get_font_size(28)
        title.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(title, 1)
        
        spacer = QWidget()
        spacer.setFixedWidth(self.screen_adapter.scale(40))
        header.addWidget(spacer)
        
        content_layout.addLayout(header)
        
        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(2)
        content_layout.addWidget(sep)
        
        # Sección de temas
        theme_group = QGroupBox(self.language_manager.get_text('theme_section'))
        font_size = self.screen_adapter.get_font_size(18)
        theme_group.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
        theme_layout = QVBoxLayout()
        theme_layout.setSpacing(self.screen_adapter.get_spacing(15))
        
        # Descripción
        desc = QLabel(self.language_manager.get_text('theme_desc'))
        desc_size = self.screen_adapter.get_font_size(13)
        desc.setFont(QFont("Segoe UI", desc_size))
        desc.setWordWrap(True)
        theme_layout.addWidget(desc)
        
        # Grid de temas
        themes_grid = QGridLayout()
        themes_grid.setSpacing(self.screen_adapter.get_spacing(12))
        
        themes = self.theme_manager.get_available_themes()
        current_theme = self.theme_manager.get_current_theme_name()
        
        for idx, (theme_key, theme_name) in enumerate(themes):
            theme_btn = QPushButton(f"  {theme_name}  ")
            theme_btn.setCheckable(True)
            theme_btn.setChecked(theme_key == current_theme)
            theme_btn.setMinimumHeight(self.screen_adapter.scale(50))
            
            # Color preview
            preview_color = self.theme_manager.get_current_theme()['primary'] if theme_key == current_theme else "#666"
            
            font_size = self.screen_adapter.get_font_size(15)
            theme_btn.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
            
            theme_btn.clicked.connect(lambda checked, key=theme_key: self._on_theme_selected(key))
            
            row = idx // 3
            col = idx % 3
            themes_grid.addWidget(theme_btn, row, col)
        
        theme_layout.addLayout(themes_grid)
        theme_group.setLayout(theme_layout)
        content_layout.addWidget(theme_group)
        
        # Sección de idioma
        language_group = QGroupBox(self.language_manager.get_text('language_section'))
        language_group.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
        language_layout = QVBoxLayout()
        language_layout.setSpacing(self.screen_adapter.get_spacing(15))
        
        # Descripción
        lang_desc = QLabel(self.language_manager.get_text('language_desc'))
        lang_desc.setFont(QFont("Segoe UI", desc_size))
        lang_desc.setWordWrap(True)
        language_layout.addWidget(lang_desc)
        
        # Grid de idiomas
        languages_grid = QHBoxLayout()
        languages_grid.setSpacing(self.screen_adapter.get_spacing(12))
        
        languages = self.language_manager.get_available_languages()
        current_lang = self.language_manager.get_current_language()
        
        for lang_code, lang_name in languages:
            lang_btn = QPushButton(f"  {lang_name}  ")
            lang_btn.setCheckable(True)
            lang_btn.setChecked(lang_code == current_lang)
            lang_btn.setMinimumHeight(self.screen_adapter.scale(50))
            lang_btn.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(15), QFont.Weight.Bold))
            lang_btn.clicked.connect(lambda checked, code=lang_code: self._on_language_selected(code))
            languages_grid.addWidget(lang_btn)
        
        languages_grid.addStretch()
        language_layout.addLayout(languages_grid)
        language_group.setLayout(language_layout)
        content_layout.addWidget(language_group)
        
        # Sección de apariencia
        appearance_group = QGroupBox(self.language_manager.get_text('appearance_section'))
        appearance_group.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
        appearance_layout = QGridLayout()
        appearance_layout.setSpacing(self.screen_adapter.get_spacing(12))
        
        # Escala de interfaz
        scale_label = QLabel("Escala de interfaz:")
        scale_label.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(14)))
        appearance_layout.addWidget(scale_label, 0, 0)
        
        scale_combo = QComboBox()
        current_scale = self.screen_adapter.user_scale_factor
        scale_options = [
            ("50%", 0.5),
            ("75%", 0.75),
            ("100% (Normal)", 1.0),
            ("125%", 1.25),
            ("150%", 1.5),
            ("175%", 1.75),
            ("200%", 2.0)
        ]
        
        for i, (label, value) in enumerate(scale_options):
            scale_combo.addItem(label, value)
            if abs(value - current_scale) < 0.01:
                scale_combo.setCurrentIndex(i)
        
        scale_combo.currentIndexChanged.connect(self._on_scale_changed)
        appearance_layout.addWidget(scale_combo, 0, 1)
        self.scale_combo = scale_combo
        
        # Tamaño de fuente
        font_label = QLabel(self.language_manager.get_text('font_size'))
        font_label.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(14)))
        appearance_layout.addWidget(font_label, 1, 0)
        
        font_combo = QComboBox()
        font_combo.addItems([
            self.language_manager.get_text('font_small'),
            self.language_manager.get_text('font_medium'),
            self.language_manager.get_text('font_large')
        ])
        font_combo.setCurrentIndex(1)
        appearance_layout.addWidget(font_combo, 1, 1)
        
        # Animaciones
        anim_label = QLabel(self.language_manager.get_text('animations'))
        anim_label.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(14)))
        appearance_layout.addWidget(anim_label, 2, 0)
        
        anim_combo = QComboBox()
        anim_combo.addItems([
            self.language_manager.get_text('enabled'),
            self.language_manager.get_text('disabled')
        ])
        appearance_layout.addWidget(anim_combo, 2, 1)
        
        appearance_group.setLayout(appearance_layout)
        content_layout.addWidget(appearance_group)
        
        content_layout.addStretch()
        
        # Separador antes de botones
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setFixedHeight(2)
        content_layout.addWidget(sep2)
        
        # Botones de acción
        buttons = QHBoxLayout()
        buttons.setSpacing(self.screen_adapter.get_spacing(12))
        buttons.setContentsMargins(0, self.screen_adapter.get_margin(15), 0, self.screen_adapter.get_margin(15))
        
        # Botón restaurar
        restore_btn = QPushButton("🔄 " + self.language_manager.get_text('restore'))
        restore_btn.setMinimumHeight(self.screen_adapter.scale(45))
        restore_btn.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(14), QFont.Weight.Bold))
        restore_btn.clicked.connect(self._restore_defaults)
        restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #ffa500;
                border: 2px solid #4a4a4a;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #ffa500;
                color: #000;
            }
        """)
        buttons.addWidget(restore_btn)
        
        buttons.addStretch()
        
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
        
        content_layout.addLayout(buttons)
    
    def _on_theme_selected(self, theme_key):
        """Cuando se selecciona un tema."""
        self.theme_manager.set_theme(theme_key)
        
        # Actualizar estado de botones
        for btn in self.findChildren(QPushButton):
            if btn.isCheckable():
                btn.setChecked(False)
        
        sender = self.sender()
        if sender:
            sender.setChecked(True)
    
    def _on_scale_changed(self, index):
        """Cuando se cambia la escala de interfaz."""
        scale_value = self.scale_combo.currentData()
        self.screen_adapter.set_user_scale(scale_value)
        
        # Reconstruir UI con nueva escala
        self._build_content()
        self._apply_theme()
        
        # Notificar a la ventana principal para que se redibuje
        window = self.window()
        if window:
            window.update()
    
    def _on_language_selected(self, lang_code):
        """Cuando se selecciona un idioma."""
        self.language_manager.set_language(lang_code)
        
        # Actualizar estado de botones de idioma
        for btn in self.findChildren(QPushButton):
            if btn.isCheckable() and btn.text().strip() in [lang[1] for lang in self.language_manager.get_available_languages()]:
                btn.setChecked(False)
        
        sender = self.sender()
        if sender:
            sender.setChecked(True)
    
    def _on_language_changed(self, lang_code):
        """Se llama cuando cambia el idioma."""
        # Reconstruir la interfaz con las nuevas traducciones
        self._build_content()
        self._apply_theme()
    
    def _save_settings(self):
        """Guarda la configuración."""
        # TODO: Implementar guardado de configuración
        self.navigation.back()
    
    def _restore_defaults(self):
        """Restaura la configuración por defecto."""
        # Restaurar tema por defecto
        self.theme_manager.set_theme('azul')
        # Restaurar idioma por defecto
        self.language_manager.set_language('es')
        # Reconstruir UI
        self._build_content()
        self._apply_theme()
    
    def _apply_theme(self):
        """Aplica el tema actual."""
        theme = self.theme_manager.get_current_theme()
        
        self.setStyleSheet(f"""
            QWidget {{
                background: {theme['background']};
                color: {theme['text']};
            }}
            
            QGroupBox {{
                color: {theme['secondary']};
                font-size: 18px;
                font-weight: bold;
                border: 2px solid {theme['border']};
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 18px;
                background: {theme['surface']};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0px 10px;
                color: {theme['secondary']};
            }}
            
            QLabel {{
                color: {theme['text']};
            }}
            
            QComboBox {{
                background-color: {theme['surface_alt']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                min-width: 150px;
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid {theme['primary']};
                margin-right: 8px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {theme['surface_alt']};
                color: {theme['text']};
                selection-background-color: {theme['primary']};
                border: 1px solid {theme['border']};
            }}
            
            QFrame[frameShape="4"] {{
                background-color: {theme['border']};
            }}
        """)
