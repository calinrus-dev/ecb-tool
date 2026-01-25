from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QUrl, QProcess
from PyQt6.QtGui import QPixmap, QDesktopServices
import os

class MediaPreviewLabel(QLabel):
    """
    Label that represents a media file.
    Hover: Shows visual highlight (or plays audio snippet if implemented).
    Click: Opens file in default system player.
    """
    def __init__(self, file_path, parent=None):
        super().__init__(file_path.name, parent)
        self.file_path = file_path
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QLabel {
                color: #A1A1AA;
                padding: 8px;
                border-radius: 4px;
                background: transparent;
            }
            QLabel:hover {
                background-color: #3f51b5;
                color: white;
            }
        """)
        self.setToolTip(f"Click to open: {file_path.name}")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.open_file()
            
    def open_file(self):
        try:
            os.startfile(str(self.file_path))
        except Exception as e:
            print(f"Error opening file: {e}")
            
    def enterEvent(self, event):
        # Could trigger a "preview" signal here to a main player
        if hasattr(self.parent(), 'preview_requested'):
             self.parent().preview_requested(self.file_path)
        super().enterEvent(event)

class AssetListWidget(QWidget):
    """Scrollable list of AssetLabels."""
    def __init__(self, files, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(2)
        
        self.preview_callback = None
        
        if not files:
            layout.addWidget(QLabel("No files found", styleSheet="color: #52525B;"))
        else:
            for f in files:
                lbl = MediaPreviewLabel(f, self)
                layout.addWidget(lbl)
                
        layout.addStretch()
        
    def preview_requested(self, path):
        if self.preview_callback:
            self.preview_callback(path)
