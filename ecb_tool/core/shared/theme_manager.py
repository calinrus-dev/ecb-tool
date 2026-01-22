"""Sistema de gestión de temas de la aplicación."""
import json
import os
from PyQt6.QtCore import QObject, pyqtSignal
from ecb_tool.core.shared.paths import ROOT_DIR

THEME_CONFIG_PATH = os.path.join(ROOT_DIR, 'config', 'theme.json')

THEMES = {
    "azul": {
        "name": "Azul",
        "primary": "#3998ff",
        "primary_hover": "#4fa8ff",
        "secondary": "#24eaff",
        "accent": "#8ad6ff",
        "success": "#43b680",
        "background": "#101722",
        "surface": "#181f2c",
        "surface_alt": "#141b28",
        "surface_dark": "#141c2c",
        "border": "#23304a",
        "text": "#f4f8ff",
        "text_secondary": "#8ad6ff",
        "topbar": "#070c13"
    },
    "rojo": {
        "name": "Rojo",
        "primary": "#ff4757",
        "primary_hover": "#ff6b7a",
        "secondary": "#ff3838",
        "accent": "#ffa8b4",
        "success": "#43b680",
        "background": "#1a0f14",
        "surface": "#2c1a20",
        "surface_alt": "#241419",
        "surface_dark": "#1f141a",
        "border": "#4a2330",
        "text": "#fff8f9",
        "text_secondary": "#ffb4be",
        "topbar": "#0d0509"
    },
    "verde": {
        "name": "Verde",
        "primary": "#1dd1a1",
        "primary_hover": "#10ac84",
        "secondary": "#2ecc71",
        "accent": "#55efc4",
        "success": "#00b894",
        "background": "#0f1a14",
        "surface": "#1a2c20",
        "surface_alt": "#141f19",
        "surface_dark": "#14201a",
        "border": "#234a30",
        "text": "#f4fff8",
        "text_secondary": "#8affcc",
        "topbar": "#070d09"
    },
    "amarillo": {
        "name": "Amarillo",
        "primary": "#ffa502",
        "primary_hover": "#ff8c00",
        "secondary": "#ffdd59",
        "accent": "#ffd93d",
        "success": "#43b680",
        "background": "#1a1510",
        "surface": "#2c2418",
        "surface_alt": "#241e14",
        "surface_dark": "#1f1a14",
        "border": "#4a3e23",
        "text": "#fffcf4",
        "text_secondary": "#ffe28a",
        "topbar": "#0d0a07"
    },
    "morado": {
        "name": "Morado",
        "primary": "#a55eea",
        "primary_hover": "#b77ff5",
        "secondary": "#8854d0",
        "accent": "#d3b4ff",
        "success": "#43b680",
        "background": "#14101a",
        "surface": "#201a2c",
        "surface_alt": "#19141f",
        "surface_dark": "#1a1420",
        "border": "#3e234a",
        "text": "#f9f4ff",
        "text_secondary": "#c8a8ff",
        "topbar": "#09070d"
    },
    "oscuro": {
        "name": "Oscuro",
        "primary": "#ffffff",
        "primary_hover": "#e0e0e0",
        "secondary": "#b0b0b0",
        "accent": "#808080",
        "success": "#43b680",
        "background": "#0a0a0a",
        "surface": "#141414",
        "surface_alt": "#0f0f0f",
        "surface_dark": "#0d0d0d",
        "border": "#2a2a2a",
        "text": "#ffffff",
        "text_secondary": "#a0a0a0",
        "topbar": "#000000"
    }
}


class ThemeManager(QObject):
    """Gestor de temas de la aplicación."""
    theme_changed = pyqtSignal(str)  # Emite el nombre del tema
    
    def __init__(self):
        super().__init__()
        self._current_theme = "azul"
        self._load_theme()
    
    def _load_theme(self):
        """Carga el tema guardado."""
        if os.path.exists(THEME_CONFIG_PATH):
            try:
                with open(THEME_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    theme = config.get('theme', 'azul')
                    if theme in THEMES:
                        self._current_theme = theme
            except:
                pass
    
    def _save_theme(self):
        """Guarda el tema actual."""
        os.makedirs(os.path.dirname(THEME_CONFIG_PATH), exist_ok=True)
        with open(THEME_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump({'theme': self._current_theme}, f, indent=2)
    
    def get_current_theme_name(self):
        """Retorna el nombre del tema actual."""
        return self._current_theme
    
    def get_current_theme(self):
        """Retorna los colores del tema actual."""
        return THEMES[self._current_theme]
    
    def set_theme(self, theme_name):
        """Cambia el tema."""
        if theme_name in THEMES:
            self._current_theme = theme_name
            self._save_theme()
            self.theme_changed.emit(theme_name)
    
    def get_available_themes(self):
        """Retorna lista de temas disponibles con nombres traducidos."""
        # Importar aquí para evitar dependencia circular
        try:
            from ecb_tool.core.shared.language_manager import get_language_manager
            lang = get_language_manager()
            return [
                ('azul', lang.get_text('theme_blue')),
                ('rojo', lang.get_text('theme_red')),
                ('verde', lang.get_text('theme_green')),
                ('amarillo', lang.get_text('theme_yellow')),
                ('morado', lang.get_text('theme_purple')),
                ('oscuro', lang.get_text('theme_dark'))
            ]
        except:
            # Fallback si falla el language manager
            return [(key, data['name']) for key, data in THEMES.items()]
    
    def get_stylesheet(self):
        """Genera stylesheet completo para la aplicación."""
        theme = self.get_current_theme()
        
        return f"""
            QWidget {{
                background: {theme['background']};
                color: {theme['text']};
            }}
            
            QScrollArea {{
                border: none;
                background: {theme['background']};
            }}
            
            QScrollBar:vertical {{
                background: {theme['surface']};
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical {{
                background: {theme['primary']};
                border-radius: 5px;
                min-height: 30px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: {theme['primary_hover']};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar:horizontal {{
                background: {theme['surface']};
                height: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            
            QScrollBar::handle:horizontal {{
                background: {theme['primary']};
                border-radius: 5px;
                min-width: 30px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background: {theme['primary_hover']};
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            
            QPushButton {{
                background-color: {theme['primary']};
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 15px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {theme['primary_hover']};
            }}
            
            QPushButton:pressed {{
                background-color: {theme['primary']};
            }}
            
            QPushButton:disabled {{
                background-color: {theme['border']};
                color: {theme['text_secondary']};
            }}
        """


# Instancia global
_theme_manager = None

def get_theme_manager():
    """Obtiene la instancia del gestor de temas."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
