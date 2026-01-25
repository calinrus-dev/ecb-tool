from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QIcon, QFont

from ecb_tool.features.ui.styles.theme import ThemeColors

class NavButton(QPushButton):
    """Sidebar navigation button."""
    def __init__(self, text, icon_name=None, active=False, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self.setChecked(active)
        
        # Simple style for now, can be enhanced with icons later
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {ThemeColors.TextSecondary};
                border: none;
                border-radius: 8px;
                padding-left: 16px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {ThemeColors.SurfaceHighlight};
                color: {ThemeColors.TextPrimary};
            }}
            QPushButton:checked {{
                background-color: {ThemeColors.SurfaceHighlight};
                color: {ThemeColors.Primary};
                font-weight: 600;
                border-left: 3px solid {ThemeColors.Primary};
            }}
        """)

class Sidebar(QFrame):
    """Application sidebar."""
    page_changed = pyqtSignal(str) # Emits page name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {ThemeColors.Surface}; border-right: 1px solid {ThemeColors.Border};")
        self.setFixedWidth(250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 24, 12, 24)
        layout.setSpacing(8)
        
        # Logo / Title
        title = QLabel("ECB TOOL")
        title.setStyleSheet(f"color: {ThemeColors.TextPrimary}; font-size: 20px; font-weight: 800; margin-bottom: 24px; margin-left: 8px;")
        layout.addWidget(title)
        
        # Nav Buttons
        self.group = []
        self.add_nav_item("Home", "home", layout, True)
        self.add_nav_item("Projects", "folder", layout)
        self.add_nav_item("Converter", "refresh-cw", layout)
        self.add_nav_item("Uploader", "upload-cloud", layout)
        
        layout.addStretch()
        
        # Version
        version = QLabel("v2.0 Professional")
        version.setStyleSheet(f"color: {ThemeColors.TextDisabled}; font-size: 11px; margin-left: 8px;")
        layout.addWidget(version)

    def add_nav_item(self, text, icon, layout, active=False):
        btn = NavButton(text, icon, active)
        btn.clicked.connect(lambda: self.handle_click(text))
        layout.addWidget(btn)
        self.group.append(btn)
        
    def handle_click(self, text):
        for btn in self.group:
            btn.setChecked(btn.text() == text)
        self.page_changed.emit(text)
