from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette

from ecb_tool.features.ui.styles.theme import ThemeColors
from ecb_tool.features.ui.components.navigation import Sidebar

class PlaceholderPage(QWidget):
    """Temporary page for testing navigation."""
    def __init__(self, name, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl = QLabel(name)
        lbl.setStyleSheet(f"color: {ThemeColors.TextSecondary}; font-size: 24px; font-weight: 300;")
        layout.addWidget(lbl)

class MainWindow(QMainWindow):
    """Modern professional main window."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ECB Tool Professional")
        self.resize(1280, 800)
        
        # Apply Global Stylesheet
        with open("ecb_tool/features/ui/styles/dark.qss", "r") as f:
            self.app_style = f.read()
            self.setStyleSheet(self.app_style)
            
        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main Layout (Horizontal: Sidebar | Content)
        self.main_layout = QHBoxLayout(central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.switch_page)
        self.main_layout.addWidget(self.sidebar)
        
        # Content Area (Stacked)
        self.content_area = QStackedWidget()
        self.main_layout.addWidget(self.content_area)
        
        # Initialize Pages
        self.pages = {}
        self.init_pages()
        
    def init_pages(self):
        from ecb_tool.features.ui.pages.home_page import HomePage
        from ecb_tool.features.ui.pages.project_page import ProjectPage
        from ecb_tool.features.ui.pages.converter_page import ConverterPage
        from ecb_tool.features.ui.pages.uploader_page import UploaderPage
        
        self.add_page("Home", HomePage())
        self.add_page("Projects", ProjectPage())
        self.add_page("Converter", ConverterPage())
        self.add_page("Uploader", UploaderPage())
        
    def add_page(self, name, widget):
        self.pages[name] = widget
        self.content_area.addWidget(widget)
        
    def switch_page(self, name):
        if name in self.pages:
            self.content_area.setCurrentWidget(self.pages[name])
