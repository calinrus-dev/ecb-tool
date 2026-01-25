"""
Style Manager for ECB Tool.
Provides Windows 11 (Fluent Design) inspired stylesheets for Dark Mode.
"""
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

class StyleManager:
    """Manages application styles and themes."""
    
    # Windows 11 Dark Mode Colors
    COLOR_BACKGROUND = "#202020"    # Mica-like background
    COLOR_SURFACE = "#2C2C2C"       # Card surface
    COLOR_SURFACE_HOVER = "#353535"
    COLOR_PRIMARY = "#60CDFF"       # System accent (Cyan/Blue)
    COLOR_PRIMARY_HOVER = "#78D6FF"
    COLOR_TEXT = "#FFFFFF"
    COLOR_TEXT_SECONDARY = "#A0A0A0"
    COLOR_BORDER = "#3E3E3E"
    COLOR_SUCCESS = "#6CCB5F"
    COLOR_ERROR = "#FF99A4"

    @staticmethod
    def get_stylesheet() -> str:
        """Get the main QSS stylesheet."""
        # Note: Using standard string format manually to avoid f-string curly brace hell if complex
        # But f-string is cleaner for constants.
        return f"""
        QMainWindow, QWidget {{
            background-color: {StyleManager.COLOR_BACKGROUND};
            color: {StyleManager.COLOR_TEXT};
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            font-size: 14px;
        }}
        
        /* --- Buttons --- */
        QPushButton {{
            background-color: {StyleManager.COLOR_SURFACE};
            border: 1px solid {StyleManager.COLOR_BORDER};
            border-radius: 4px;
            padding: 8px 16px;
            color: {StyleManager.COLOR_TEXT};
        }}
        QPushButton:hover {{
            background-color: {StyleManager.COLOR_SURFACE_HOVER};
            border-color: {StyleManager.COLOR_BORDER};
        }}
        QPushButton:pressed {{
            background-color: {StyleManager.COLOR_BACKGROUND};
            color: {StyleManager.COLOR_TEXT_SECONDARY};
        }}
        QPushButton:disabled {{
            background-color: {StyleManager.COLOR_BACKGROUND};
            color: {StyleManager.COLOR_TEXT_SECONDARY};
            border-color: #333333;
        }}
        
        /* Primary Button */
        QPushButton[class="primary"] {{
            background-color: {StyleManager.COLOR_PRIMARY};
            color: #000000;
            border: none;
            font-weight: 600;
        }}
        QPushButton[class="primary"]:hover {{
            background-color: {StyleManager.COLOR_PRIMARY_HOVER};
        }}
        
        /* --- Inputs --- */
        QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {{
            background-color: {StyleManager.COLOR_SURFACE};
            border: 1px solid {StyleManager.COLOR_BORDER};
            border-radius: 4px;
            padding: 8px;
            color: {StyleManager.COLOR_TEXT};
            selection-background-color: {StyleManager.COLOR_PRIMARY};
            selection-color: #000000;
        }}
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {{
            border-color: {StyleManager.COLOR_PRIMARY};
            border-bottom: 2px solid {StyleManager.COLOR_PRIMARY};
        }}
        
        /* --- Scrollbars --- */
        QScrollBar:vertical {{
            border: none;
            background: {StyleManager.COLOR_BACKGROUND};
            width: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: #505050;
            min-height: 20px;
            border-radius: 5px;
            margin: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: #6D6D6D;
        }}
        
        /* --- Tables/Lists --- */
        QTableWidget, QListWidget {{
            background-color: {StyleManager.COLOR_BACKGROUND};
            border: 1px solid {StyleManager.COLOR_BORDER};
            border-radius: 8px;
            gridline-color: {StyleManager.COLOR_BORDER};
        }}
        QHeaderView::section {{
            background-color: {StyleManager.COLOR_SURFACE};
            padding: 8px;
            border: none;
            border-bottom: 1px solid {StyleManager.COLOR_BORDER};
            font-weight: bold;
        }}
        QTableWidget::item {{
            padding: 5px;
        }}
        QTableWidget::item:selected {{
            background-color: {StyleManager.COLOR_SURFACE_HOVER};
            color: {StyleManager.COLOR_PRIMARY};
        }}
        
        /* --- Sidebar Navigation --- */
        QWidget#sidebar_container {{
            background-color: {StyleManager.COLOR_SURFACE};
            border-right: 1px solid {StyleManager.COLOR_BORDER};
        }}
        
        QPushButton[class="nav_button"] {{
            text-align: left;
            padding: 12px 20px;
            border-radius: 0px;
            border: none;
            background-color: transparent;
            font-size: 15px;
            margin: 2px 8px;
            border-radius: 6px;
        }}
        QPushButton[class="nav_button"]:hover {{
            background-color: #3D3D3D;
        }}
        QPushButton[class="nav_button"]:checked {{
            background-color: #454545;
            color: {StyleManager.COLOR_PRIMARY};
            font-weight: bold;
            border-left: 3px solid {StyleManager.COLOR_PRIMARY};
        }}
        
        /* --- Cards --- */
        QFrame[class="card"] {{
            background-color: {StyleManager.COLOR_SURFACE};
            border: 1px solid {StyleManager.COLOR_BORDER};
            border-radius: 8px;
        }}
        
        /* --- Labels --- */
        QLabel[class="h1"] {{
            font-size: 24px;
            font-weight: bold;
        }}
        QLabel[class="h2"] {{
            font-size: 18px;
            font-weight: 600;
            color: {StyleManager.COLOR_TEXT_SECONDARY};
        }}
        """
