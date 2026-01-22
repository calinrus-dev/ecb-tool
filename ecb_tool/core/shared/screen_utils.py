"""Utilidades para manejo de resoluciones de pantalla."""
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect


class ScreenAdapter:
    """Adaptador de resoluciones de pantalla con escalado dinámico."""
    
    def __init__(self):
        self.app = QApplication.instance()
        self.screen = QApplication.primaryScreen()
        self.geometry = self.screen.availableGeometry() if self.screen else QRect(0, 0, 1920, 1080)
        self.width = self.geometry.width()
        self.height = self.geometry.height()
        
        # Obtener DPI real del sistema
        self.dpi = self.screen.logicalDotsPerInch() if self.screen else 96.0
        self.dpi_scale = self.dpi / 96.0  # 96 DPI es el estándar
        
        # Factor de escala manual (1.0 = normal, puede ser modificado por usuario)
        self.user_scale_factor = 1.0
        
        # Calcular factor de escala automático basado en resolución
        self.auto_scale_factor = self._calculate_auto_scale()
        
    def _calculate_auto_scale(self):
        """Calcula el factor de escala automático según resolución y DPI."""
        # Base: 1920x1080 @ 96 DPI
        base_width = 1920
        base_height = 1080
        
        # Calcular escala basada en resolución
        width_scale = self.width / base_width
        height_scale = self.height / base_height
        
        # Usar el promedio para mejor balance
        resolution_scale = (width_scale + height_scale) / 2
        
        # Combinar con DPI
        combined_scale = resolution_scale * self.dpi_scale
        
        # Ajustar para que sea más conservador
        # Si la escala es muy pequeña o muy grande, suavizarla
        if combined_scale < 0.8:
            combined_scale = 0.8 + (combined_scale - 0.8) * 0.5
        elif combined_scale > 1.5:
            combined_scale = 1.5 + (combined_scale - 1.5) * 0.3
        
        # Limitar entre 0.7 y 2.5
        return max(0.7, min(2.5, combined_scale))
    
    def get_total_scale_factor(self):
        """Obtiene el factor de escala total (auto * usuario)."""
        return self.auto_scale_factor * self.user_scale_factor
    
    def set_user_scale(self, factor):
        """Establece el factor de escala manual del usuario (0.5 a 2.0)."""
        self.user_scale_factor = max(0.5, min(2.0, factor))
    
    def scale(self, value):
        """Escala un valor según la resolución y DPI."""
        return int(value * self.get_total_scale_factor())
    
    def get_main_window_size(self):
        """Retorna el tamaño ideal para la ventana principal."""
        # Usar 75% del ancho y 88% del alto disponible
        width = int(self.width * 0.75)
        height = int(self.height * 0.88)
        
        # Mínimos absolutos
        width = max(1000, width)
        height = max(650, height)
        
        # Máximos para evitar ventanas gigantes en 4K
        width = min(2400, width)
        height = min(1400, height)
        
        return (width, height)
    
    def get_dialog_size(self, base_width, base_height, max_percentage=0.9):
        """Retorna el tamaño ideal para un diálogo."""
        # Escalar tamaño base
        width = self.scale(base_width)
        height = self.scale(base_height)
        
        # No exceder porcentaje de pantalla
        max_width = int(self.width * max_percentage)
        max_height = int(self.height * max_percentage)
        
        width = min(width, max_width)
        height = min(height, max_height)
        
        return (width, height)
    
    def get_font_size(self, base_size):
        """Retorna el tamaño de fuente escalado."""
        # Aplicar escala total
        scaled = base_size * self.get_total_scale_factor()
        
        # Redondear a entero más cercano
        scaled = round(scaled)
        
        # Limitar entre 8 y 72pt
        return max(8, min(72, scaled))
    
    def get_spacing(self, base_spacing):
        """Retorna el espaciado escalado."""
        return max(2, self.scale(base_spacing))
    
    def get_margin(self, base_margin):
        """Retorna el margen escalado."""
        return max(5, self.scale(base_margin))
    
    def center_widget(self, widget):
        """Centra un widget en la pantalla."""
        x = int(self.geometry.x() + (self.width - widget.width()) / 2)
        y = int(self.geometry.y() + (self.height - widget.height()) / 2)
        widget.move(max(0, x), max(0, y))
    
    def get_window_constraints(self):
        """Obtiene constraints min/max para ventanas."""
        min_width = max(800, int(self.width * 0.4))
        min_height = max(550, int(self.height * 0.4))
        max_width = int(self.width * 0.95)
        max_height = int(self.height * 0.95)
        
        return {
            'min_width': min_width,
            'min_height': min_height,
            'max_width': max_width,
            'max_height': max_height
        }
    
    def refresh_screen_info(self):
        """Actualiza información de pantalla (útil para cambios de resolución)."""
        self.screen = QApplication.primaryScreen()
        if self.screen:
            self.geometry = self.screen.availableGeometry()
            self.width = self.geometry.width()
            self.height = self.geometry.height()
            self.dpi = self.screen.logicalDotsPerInch()
            self.dpi_scale = self.dpi / 96.0
            self.auto_scale_factor = self._calculate_auto_scale()


# Instancia global
_screen_adapter = None

def get_screen_adapter():
    """Obtiene la instancia del adaptador de pantalla."""
    global _screen_adapter
    if _screen_adapter is None:
        _screen_adapter = ScreenAdapter()
    return _screen_adapter

def reset_screen_adapter():
    """Reinicia el adaptador (útil para cambios de configuración)."""
    global _screen_adapter
    _screen_adapter = None

