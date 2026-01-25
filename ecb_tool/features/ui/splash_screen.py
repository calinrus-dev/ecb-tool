from PyQt6.QtWidgets import QSplashScreen, QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QColor, QFont

from ecb_tool.features.ui.styles.theme import ThemeColors

class SplashScreen(QSplashScreen):
    """Professional Splash Screen."""
    def __init__(self):
        # Create a blank pixmap for custom painting (or transparent)
        pixmap = QPixmap(600, 350)
        pixmap.fill(QColor(ThemeColors.Background))
        super().__init__(pixmap)
        
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        
        # Layout inside the splash
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("ECB TOOL")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {ThemeColors.Primary}; font-size: 48px; font-weight: 900; letter-spacing: 4px;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Professional Beat Implementation Suite")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {ThemeColors.TextSecondary}; font-size: 16px; font-weight: 400;")
        layout.addWidget(subtitle)
        
        layout.addStretch()
        
        # Loading
        self.loading_label = QLabel("Initializing core modules...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet(f"color: {ThemeColors.TextDisabled}; font-size: 12px;")
        layout.addWidget(self.loading_label)
        
        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setFixedHeight(4)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: {ThemeColors.SurfaceHighlight};
                border: none;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background-color: {ThemeColors.Primary};
                border-radius: 2px;
            }}
        """)
        layout.addWidget(self.progress)
        
        self.counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30) # 30ms

    def update_progress(self):
        self.counter += 1
        self.progress.setValue(self.counter)
        
        if self.counter > 30:
            self.loading_label.setText("Loading user preferences...")
        if self.counter > 60:
            self.loading_label.setText("Connecting to services...")
        if self.counter > 90:
            self.loading_label.setText("Starting UI...")
            
        if self.counter >= 100:
            self.timer.stop()
            self.close()
