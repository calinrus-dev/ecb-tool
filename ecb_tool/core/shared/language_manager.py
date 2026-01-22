"""Sistema de gestión de idiomas."""
import os
import json
from PyQt6.QtCore import QObject, pyqtSignal

from ecb_tool.core.shared.paths import CONFIG_DIR


LANGUAGE_CONFIG_PATH = os.path.join(CONFIG_DIR, "language.json")


# Traducciones para cada idioma
TRANSLATIONS = {
    "es": {
        # Menú principal
        "app_title": "ECB TOOL",
        "converter": "CONVERSOR",
        "uploader": "SUBIDOR",
        "generator": "GENERADOR",
        "execute": "EJECUTAR",
        "stop": "DETENER",
        
        # Modos
        "convert": "Convertir",
        "upload": "Subir",
        "alternate": "Alternar",
        "simultaneous": "Simultáneo",
        
        # Contadores
        "beats": "Beats",
        "covers": "Covers",
        "videos": "Videos",
        "titles": "Titles",
        "description": "Desc.",
        "cover_mode": "Cover Mode:",
        
        # Cover modes
        "random": "Random",
        "random_no_repeat": "Random (No Repeat)",
        "select_one": "Select One",
        "sequential": "Sequential",
        
        # Panel de estado
        "status": "Estado",
        "ready": "Listo",
        "mode": "Modo",
        "executing": "Ejecutando",
        "conversion": "Conversión",
        "uploads": "Subidas",
        
        # Selector de modo
        "orders": "Orders:",
        "bpv": "BPV:",
        
        # Menú
        "menu": "Menú",
        "general_settings": "Ajustes Generales",
        "conversion_settings": "Ajustes de Conversión",
        "upload_settings": "Ajustes de Subida",
        "upload_calendar": "Calendario de Subidas",
        
        # Configuración general
        "general_config": "Configuración General",
        "theme_section": "🎨 Tema de la Aplicación",
        "theme_desc": "Selecciona el tema de colores para personalizar la interfaz",
        "language_section": "🌍 Idioma",
        "language_desc": "Selecciona el idioma de la interfaz",
        "appearance_section": "🖥️ Apariencia",
        "font_size": "Tamaño de fuente:",
        "animations": "Animaciones:",
        "enabled": "Habilitadas",
        "disabled": "Deshabilitadas",
        
        # Tamaños de fuente
        "font_small": "Pequeño",
        "font_medium": "Mediano",
        "font_large": "Grande",
        
        # Temas
        "theme_blue": "Azul",
        "theme_red": "Rojo",
        "theme_green": "Verde",
        "theme_yellow": "Amarillo",
        "theme_purple": "Morado",
        "theme_dark": "Oscuro",
        
        # Idiomas
        "lang_spanish": "Español",
        "lang_english": "English",
        "lang_french": "Français",
        
        # Botones de acción
        "save": "Guardar",
        "save_changes": "💾 Guardar Cambios",
        "cancel": "Cancelar",
        "restore": "Restaurar",
        "close": "Cerrar",
    },
    
    "en": {
        # Main menu
        "app_title": "ECB TOOL",
        "converter": "CONVERTER",
        "uploader": "UPLOADER",
        "generator": "GENERATOR",
        "execute": "EXECUTE",
        "stop": "STOP",
        
        # Modes
        "convert": "Convert",
        "upload": "Upload",
        "alternate": "Alternate",
        "simultaneous": "Simultaneous",
        
        # Counters
        "beats": "Beats",
        "covers": "Covers",
        "videos": "Videos",
        "titles": "Titles",
        "description": "Desc.",
        "cover_mode": "Cover Mode:",
        
        # Cover modes
        "random": "Random",
        "random_no_repeat": "Random (No Repeat)",
        "select_one": "Select One",
        "sequential": "Sequential",
        
        # Status panel
        "status": "Status",
        "ready": "Ready",
        "mode": "Mode",
        "executing": "Executing",
        "conversion": "Conversion",
        "uploads": "Uploads",
        
        # Mode selector
        "orders": "Orders:",
        "bpv": "BPV:",
        
        # Menu
        "menu": "Menu",
        "general_settings": "General Settings",
        "conversion_settings": "Conversion Settings",
        "upload_settings": "Upload Settings",
        "upload_calendar": "Upload Calendar",
        
        # General settings
        "general_config": "General Settings",
        "theme_section": "🎨 Application Theme",
        "theme_desc": "Select the color theme to customize the interface",
        "language_section": "🌍 Language",
        "language_desc": "Select the interface language",
        "appearance_section": "🖥️ Appearance",
        "font_size": "Font size:",
        "animations": "Animations:",
        "enabled": "Enabled",
        "disabled": "Disabled",
        
        # Font sizes
        "font_small": "Small",
        "font_medium": "Medium",
        "font_large": "Large",
        
        # Themes
        "theme_blue": "Blue",
        "theme_red": "Red",
        "theme_green": "Green",
        "theme_yellow": "Yellow",
        "theme_purple": "Purple",
        "theme_dark": "Dark",
        
        # Languages
        "lang_spanish": "Español",
        "lang_english": "English",
        "lang_french": "Français",
        
        # Action buttons
        "save": "Save",
        "save_changes": "💾 Save Changes",
        "cancel": "Cancel",
        "restore": "Restore",
        "close": "Close",
    },
    
    "fr": {
        # Menu principal
        "app_title": "ECB TOOL",
        "converter": "CONVERTISSEUR",
        "uploader": "TÉLÉVERSEUR",
        "generator": "GÉNÉRATEUR",
        "execute": "EXÉCUTER",
        "stop": "ARRÊTER",
        
        # Modes
        "convert": "Convertir",
        "upload": "Téléverser",
        "alternate": "Alterner",
        "simultaneous": "Simultané",
        
        # Compteurs
        "beats": "Beats",
        "covers": "Covers",
        "videos": "Vidéos",
        "titles": "Titres",
        "description": "Desc.",
        "cover_mode": "Mode Cover:",
        
        # Cover modes
        "random": "Aléatoire",
        "random_no_repeat": "Aléatoire (Sans Répétition)",
        "select_one": "Sélectionner Un",
        "sequential": "Séquentiel",
        
        # Panneau d'état
        "status": "État",
        "ready": "Prêt",
        "mode": "Mode",
        "executing": "Exécution",
        "conversion": "Conversion",
        "uploads": "Téléversements",
        
        # Sélecteur de mode
        "orders": "Ordres:",
        "bpv": "BPV:",
        
        # Menu
        "menu": "Menu",
        "general_settings": "Paramètres Généraux",
        "conversion_settings": "Paramètres de Conversion",
        "upload_settings": "Paramètres de Téléversement",
        "upload_calendar": "Calendrier de Téléversement",
        
        # Configuration générale
        "general_config": "Paramètres Généraux",
        "theme_section": "🎨 Thème de l'Application",
        "theme_desc": "Sélectionnez le thème de couleur pour personnaliser l'interface",
        "language_section": "🌍 Langue",
        "language_desc": "Sélectionnez la langue de l'interface",
        "appearance_section": "🖥️ Apparence",
        "font_size": "Taille de police:",
        "animations": "Animations:",
        "enabled": "Activées",
        "disabled": "Désactivées",
        
        # Tailles de police
        "font_small": "Petite",
        "font_medium": "Moyenne",
        "font_large": "Grande",
        
        # Thèmes
        "theme_blue": "Bleu",
        "theme_red": "Rouge",
        "theme_green": "Vert",
        "theme_yellow": "Jaune",
        "theme_purple": "Violet",
        "theme_dark": "Sombre",
        
        # Langues
        "lang_spanish": "Español",
        "lang_english": "English",
        "lang_french": "Français",
        
        # Boutons d'action
        "save": "Enregistrer",
        "save_changes": "💾 Enregistrer les Modifications",
        "cancel": "Annuler",
        "restore": "Restaurer",
        "close": "Fermer",
    }
}


class LanguageManager(QObject):
    """Gestor de idiomas con soporte para múltiples lenguajes."""
    
    language_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._current_language = self._load_language()
    
    def _load_language(self):
        """Carga el idioma guardado."""
        if os.path.exists(LANGUAGE_CONFIG_PATH):
            try:
                with open(LANGUAGE_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    lang = data.get('language', 'es')
                    if lang in TRANSLATIONS:
                        return lang
            except Exception:
                pass
        return 'es'  # Por defecto español
    
    def _save_language(self, language):
        """Guarda el idioma seleccionado."""
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(LANGUAGE_CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump({'language': language}, f, indent=4)
        except Exception as e:
            print(f"Error guardando idioma: {e}")
    
    def set_language(self, language):
        """Cambia el idioma de la aplicación."""
        if language in TRANSLATIONS and language != self._current_language:
            self._current_language = language
            self._save_language(language)
            self.language_changed.emit(language)
    
    def get_current_language(self):
        """Obtiene el idioma actual."""
        return self._current_language
    
    def get_text(self, key):
        """Obtiene el texto traducido para la clave dada."""
        return TRANSLATIONS.get(self._current_language, {}).get(key, key)
    
    def get_available_languages(self):
        """Retorna lista de idiomas disponibles (code, name)."""
        return [
            ('es', TRANSLATIONS['es']['lang_spanish']),
            ('en', TRANSLATIONS['en']['lang_english']),
            ('fr', TRANSLATIONS['fr']['lang_french'])
        ]


# Singleton
_language_manager = None


def get_language_manager():
    """Obtiene la instancia singleton del gestor de idiomas."""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager


__all__ = ['LanguageManager', 'get_language_manager']
