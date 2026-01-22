"""Sistema de navegación entre pantallas."""
from PyQt6.QtCore import QObject, pyqtSignal


class NavigationManager(QObject):
    """Gestor de navegación entre pantallas."""
    navigate_to = pyqtSignal(str)  # Emite el nombre de la pantalla
    go_back = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._history = []
    
    def navigate(self, screen_name):
        """Navega a una pantalla."""
        self._history.append(screen_name)
        self.navigate_to.emit(screen_name)
    
    def back(self):
        """Vuelve a la pantalla anterior."""
        if len(self._history) > 1:
            self._history.pop()  # Quitar actual
            previous = self._history[-1]
            self.go_back.emit()
            self.navigate_to.emit(previous)
    
    def can_go_back(self):
        """Verifica si se puede volver atrás."""
        return len(self._history) > 1
    
    def clear_history(self):
        """Limpia el historial de navegación."""
        self._history.clear()


# Instancia global
_navigation_manager = None

def get_navigation_manager():
    """Obtiene la instancia del gestor de navegación."""
    global _navigation_manager
    if _navigation_manager is None:
        _navigation_manager = NavigationManager()
    return _navigation_manager
