"""
ECB Tool - Main Window.
Modern Windows 11 Style with Sidebar Navigation.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QStackedWidget, QLabel, QApplication, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont

from ecb_tool.core.paths import get_paths
from ecb_tool.features.ui.style_manager import StyleManager
from ecb_tool.features.ui.pages.conversion_page import ConversionPage
from ecb_tool.features.ui.pages.upload_page import UploadPage
from ecb_tool.features.ui.pages.history_page import HistoryPage
from ecb_tool.features.ui.pages.settings_page import SettingsPage

class MainWindow(QMainWindow):
    """Main application window with modern UI."""
    
    def __init__(self):
        super().__init__()
        self.paths = get_paths()
        self.setup_ui()
        
    def setup_ui(self):
        """Configure the main UI."""
        self.setWindowTitle("ECB TOOL - Professional Studio")
        self.setMinimumSize(1200, 800)
        
        # Apply Global Stylesheet
        app = QApplication.instance()
        if app:
            app.setStyleSheet(StyleManager.get_stylesheet())
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Layout (Horizontal: Sidebar | Content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Sidebar ---
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar_container")
        self.sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(5)
        
        # App Title in Sidebar
        title_label = QLabel("🎵 ECB STUDIO")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px; color: #FFFFFF;")
        sidebar_layout.addWidget(title_label)
        
        sidebar_layout.addSpacing(20)
        
        # Navigation Buttons
        self.nav_group = []
        self.btn_conversion = self._create_nav_button("🎬 Conversión", 0)
        self.btn_upload = self._create_nav_button("☁️ Subida YouTube", 1)
        self.btn_history = self._create_nav_button("📜 Historial", 2)
        sidebar_layout.addWidget(self.btn_conversion)
        sidebar_layout.addWidget(self.btn_upload)
        sidebar_layout.addWidget(self.btn_history)
        
        sidebar_layout.addStretch()
        
        # Bottom Settings
        self.btn_settings = self._create_nav_button("⚙️ Ajustes", 3)
        sidebar_layout.addWidget(self.btn_settings)
        
        # Version info
        version_label = QLabel("v2.0.0 Alpha")
        version_label.setStyleSheet("color: #666; font-size: 11px; padding: 10px;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_label)
        
        main_layout.addWidget(self.sidebar)
        
        # --- Main Content Area ---
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)  # No margin for the stack container
        
        # Stacked Pages
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        
        # Initialize Pages
        self.page_conversion = ConversionPage()
        self.page_upload = UploadPage()
        self.page_history = HistoryPage()
        self.page_settings = SettingsPage()
        
        self.stack.addWidget(self.page_conversion)
        self.stack.addWidget(self.page_upload)
        self.stack.addWidget(self.page_history)
        self.stack.addWidget(self.page_settings)
        
        main_layout.addWidget(content_container)
        
        # Set default page
        self.btn_conversion.setChecked(True)
        self.stack.setCurrentIndex(0)

    def _create_nav_button(self, text: str, index: int) -> QPushButton:
        """Create a styled navigation button."""
        btn = QPushButton(text)
        btn.setProperty("class", "nav_button")
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self._on_nav_click(index))
        self.nav_group.append(btn)
        return btn
        
    def _on_nav_click(self, index: int):
        """Handle navigation changes."""
        self.stack.setCurrentIndex(index)
        
        # Update checked state (exclusive)
        for i, btn in enumerate(self.nav_group):
            # The button at 'index' corresponds to pages 0, 1, 2. Settings is 3 (last button)
            # Logic: nav_group order matches stack order? 
            # nav_group = [conv, upload, history, settings] -> indexes 0, 1, 2, 3 matches stack
            btn.setChecked(i == index)
