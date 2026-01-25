"""
Translation Service provider using googletrans.
Handles automatic translation of titles and descriptions.
"""
from typing import Dict, List
import logging
from googletrans import Translator

class TranslationService:
    """Service for translating text content."""
    
    def __init__(self):
        self.translator = Translator()
        
    def translate(self, text: str, dest_lang: str = 'en') -> str:
        """
        Translate text to destination language.
        
        Args:
            text: Text to translate
            dest_lang: Destination language code ('en', 'es', 'fr', etc.)
        
        Returns:
            Translated text or original if error
        """
        if not text:
            return ""
            
        try:
            result = self.translator.translate(text, dest=dest_lang)
            return result.text
        except Exception as e:
            logging.error(f"Translation error: {e}")
            return text  # Fallback to original
            
    def translate_metadata(self, title: str, description: str, target_langs: List[str]) -> Dict[str, Dict[str, str]]:
        """
        Translate title and description to multiple languages.
        
        Args:
            title: Original title
            description: Original description
            target_langs: List of target language codes
            
        Returns:
            Dictionary mapping lang_code -> {'title': str, 'description': str}
        """
        results = {}
        
        for lang in target_langs:
            results[lang] = {
                'title': self.translate(title, lang),
                'description': self.translate(description, lang)
            }
            
        return results

# Singleton instance
_translation_service = None

def get_translation_service() -> TranslationService:
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service
