"""Sistema de animaciones de parpadeo para estados visuales."""
from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget


class BlinkPattern:
    """Patrones de parpadeo predefinidos."""
    SINGLE = [200, 200]  # Un parpadeo (encender, apagar)
    DOUBLE = [150, 100, 150, 200]  # Dos parpadeos rápidos
    SLOW_PULSE = [1000, 1000]  # Pulso lento
    ERROR_PULSE = [300, 300]  # Pulso de error
    WARNING_PULSE = [500, 500]  # Pulso de advertencia


class BlinkAnimator(QObject):
    """Animador de parpadeos para widgets."""
    
    animation_finished = pyqtSignal()
    
    def __init__(self, widget: QWidget):
        super().__init__()
        self.widget = widget
        self.timer = QTimer()
        self.timer.timeout.connect(self._next_step)
        self.pattern = []
        self.step_index = 0
        self.on_style = ""
        self.off_style = ""
        self.is_on = False
        self.loop = False
    
    def start_pattern(self, pattern: list, on_style: str, off_style: str, loop: bool = False):
        """Inicia un patrón de parpadeo."""
        self.pattern = pattern
        self.on_style = on_style
        self.off_style = off_style
        self.step_index = 0
        self.loop = loop
        self.is_on = False
        self._next_step()
    
    def _next_step(self):
        """Ejecuta el siguiente paso del patrón."""
        if self.step_index >= len(self.pattern):
            if self.loop:
                self.step_index = 0
            else:
                self.stop()
                self.animation_finished.emit()
                return
        
        # Alternar entre encendido y apagado
        self.is_on = not self.is_on
        style = self.on_style if self.is_on else self.off_style
        self.widget.setStyleSheet(style)
        
        # Programar siguiente paso
        delay = self.pattern[self.step_index]
        self.step_index += 1
        self.timer.start(delay)
    
    def stop(self):
        """Detiene la animación."""
        self.timer.stop()
        if self.off_style:
            self.widget.setStyleSheet(self.off_style)


class ModuleStateAnimator(QObject):
    """Animador de estados para módulos de conversión/subida."""
    
    def __init__(self, widget: QWidget):
        super().__init__()
        self.widget = widget
        self.blinker = BlinkAnimator(widget)
        self.current_state = "idle"
        
        # Estilos base
        self.styles = {
            'idle': """
                background: transparent;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid transparent;
            """,
            'ready': """
                background: transparent;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(255, 255, 255, 0.3);
            """,
            'running': """
                background: transparent;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(255, 255, 255, 0.6);
            """,
            'completed': """
                background: transparent;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(67, 182, 128, 0.8);
            """,
            'error': """
                background: transparent;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(255, 107, 107, 0.8);
            """,
            'warning': """
                background: transparent;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(255, 193, 7, 0.8);
            """,
            'paused': """
                background: transparent;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(158, 158, 158, 0.5);
            """
        }
        
        # Estilos de parpadeo
        self.blink_styles = {
            'ready_on': """
                background: transparent;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(255, 255, 255, 0.8);
            """,
            'completed_on': """
                background: transparent;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(67, 182, 128, 1.0);
            """,
            'error_on': """
                background: transparent;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(255, 107, 107, 1.0);
            """,
            'warning_on': """
                background: transparent;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(255, 193, 7, 1.0);
            """
        }
    
    def set_state(self, state: str, blink: bool = False):
        """Establece el estado del módulo."""
        self.current_state = state
        self.blinker.stop()
        
        if blink:
            if state == 'ready':
                # Un parpadeo al seleccionar
                self.blinker.start_pattern(
                    BlinkPattern.SINGLE,
                    self.blink_styles['ready_on'],
                    self.styles['ready'],
                    loop=False
                )
            elif state == 'completed':
                # Dos parpadeos rápidos al completar
                self.blinker.start_pattern(
                    BlinkPattern.DOUBLE,
                    self.blink_styles['completed_on'],
                    self.styles['completed'],
                    loop=False
                )
            elif state == 'error':
                # Parpadeo continuo en rojo
                self.blinker.start_pattern(
                    BlinkPattern.ERROR_PULSE,
                    self.blink_styles['error_on'],
                    self.styles['error'],
                    loop=True
                )
            elif state == 'warning':
                # Parpadeo de advertencia
                self.blinker.start_pattern(
                    BlinkPattern.WARNING_PULSE,
                    self.blink_styles['warning_on'],
                    self.styles['warning'],
                    loop=True
                )
            else:
                self.widget.setStyleSheet(self.styles.get(state, self.styles['idle']))
        else:
            self.widget.setStyleSheet(self.styles.get(state, self.styles['idle']))
    
    def stop_animation(self):
        """Detiene cualquier animación activa."""
        self.blinker.stop()
