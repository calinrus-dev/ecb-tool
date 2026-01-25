from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QFrame, QLineEdit, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QSize
from PyQt6.QtGui import QColor, QFont, QCursor

from ecb_tool.features.ui.styles.theme import ThemeColors

class ModernFrame(QFrame):
    """Base frame with corner radius and optional glass effect."""
    def __init__(self, parent=None, glass=False):
        super().__init__(parent)
        self.glass = glass
        self.update_style()
    
    def update_style(self):
        bg = ThemeColors.Surface
        if self.glass:
            bg = f"{ThemeColors.Surface}{ThemeColors.OverlayAlpha}"
            
        self.setStyleSheet(f"""
            ModernFrame {{
                background-color: {bg};
                border-radius: 12px;
                border: 1px solid {ThemeColors.Border};
            }}
        """)

class ModernButton(QPushButton):
    """Professional button with hover animation and primary/secondary variants."""
    def __init__(self, text, variant="primary", parent=None):
        super().__init__(text, parent)
        self.variant = variant
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(40)
        self.setup_style()
        
    def setup_style(self):
        if self.variant == "primary":
            bg = ThemeColors.Primary
            color = "#FFFFFF"
            border = "none"
            hover = ThemeColors.PrimaryHover
        elif self.variant == "secondary":
            bg = ThemeColors.SurfaceHighlight
            color = ThemeColors.TextPrimary
            border = f"1px solid {ThemeColors.Border}"
            hover = ThemeColors.BorderHighlight
        elif self.variant == "ghost":
            bg = "transparent"
            color = ThemeColors.TextSecondary
            border = "none"
            hover = ThemeColors.SurfaceHighlight
        elif self.variant == "danger":
            bg = ThemeColors.Error
            color = "#FFFFFF"
            border = "none"
            hover = "#dc2626"
            
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border: {border};
                border-radius: 8px;
                padding: 0 16px;
                font-weight: 600;
                font-size: 13px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {bg};
                padding-top: 1px;
            }}
        """)

class ModernInput(QLineEdit):
    """Styled input field."""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(40)
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {ThemeColors.Surface};
                border: 1px solid {ThemeColors.Border};
                border-radius: 8px;
                padding: 0 12px;
                color: {ThemeColors.TextPrimary};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 1px solid {ThemeColors.Primary};
                background-color: {ThemeColors.SurfaceHighlight};
            }}
            QLineEdit::placeholder {{
                color: {ThemeColors.TextDisabled};
            }}
        """)

class StatCard(ModernFrame):
    """Card to display a statistic."""
    def __init__(self, title, value, parent=None):
        super().__init__(parent)
        from PyQt6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {ThemeColors.TextSecondary}; font-size: 12px; font-weight: 600; text-transform: uppercase;")
        
        value_lbl = QLabel(str(value))
        value_lbl.setStyleSheet(f"color: {ThemeColors.TextPrimary}; font-size: 24px; font-weight: 700;")
        
        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
