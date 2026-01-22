"""Barra de progreso inteligente y reactiva."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont


class SmartProgressBar(QWidget):
    """Barra de progreso reactiva con animaciones."""
    
    value_changed = pyqtSignal(int)
    
    def __init__(self, label="Progreso", show_percentage=True, animate=True):
        super().__init__()
        self.show_percentage = show_percentage
        self.animate = animate
        self._current_value = 0
        self._target_value = 0
        self._init_ui(label)
        
        if self.animate:
            self._setup_animation()
    
    def _init_ui(self, label):
        """Inicializa la interfaz."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Header con label y porcentaje
        header = QHBoxLayout()
        header.setSpacing(8)
        
        self.label = QLabel(label)
        self.label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #8ad6ff;")
        header.addWidget(self.label)
        
        header.addStretch()
        
        if self.show_percentage:
            self.percentage_label = QLabel("0%")
            self.percentage_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            self.percentage_label.setStyleSheet("color: #24eaff;")
            header.addWidget(self.percentage_label)
        
        layout.addLayout(header)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(20)
        self._apply_style("default")
        
        layout.addWidget(self.progress_bar)
    
    def _setup_animation(self):
        """Configura la animación de la barra."""
        self.animation = QPropertyAnimation(self.progress_bar, b"value")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def _apply_style(self, mode="default"):
        """Aplica estilo según el modo."""
        styles = {
            "default": {
                "gradient": "stop:0 #24eaff, stop:1 #3998ff",
                "border": "#23304a",
                "bg": "#0d1117"
            },
            "converting": {
                "gradient": "stop:0 #24eaff, stop:0.5 #3998ff, stop:1 #24eaff",
                "border": "#24eaff",
                "bg": "#0d1117"
            },
            "uploading": {
                "gradient": "stop:0 #8ad6ff, stop:0.5 #3998ff, stop:1 #8ad6ff",
                "border": "#8ad6ff",
                "bg": "#0d1117"
            },
            "success": {
                "gradient": "stop:0 #43b680, stop:1 #2d9561",
                "border": "#43b680",
                "bg": "#0d1117"
            },
            "error": {
                "gradient": "stop:0 #ff6b6b, stop:1 #d32f2f",
                "border": "#ff6b6b",
                "bg": "#0d1117"
            }
        }
        
        style = styles.get(mode, styles["default"])
        
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {style['border']};
                border-radius: 10px;
                background-color: {style['bg']};
                text-align: center;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    {style['gradient']});
                border-radius: 8px;
            }}
        """)
    
    def set_mode(self, mode):
        """Cambia el modo visual de la barra."""
        self._apply_style(mode)
    
    def set_value(self, value, mode="default"):
        """Establece el valor con animación opcional."""
        value = max(0, min(100, value))
        self._target_value = value
        
        if self.animate and hasattr(self, 'animation'):
            self.animation.setStartValue(self._current_value)
            self.animation.setEndValue(value)
            self.animation.start()
        else:
            self.progress_bar.setValue(value)
        
        self._current_value = value
        
        if self.show_percentage:
            self.percentage_label.setText(f"{value}%")
        
        self._apply_style(mode)
        self.value_changed.emit(value)
    
    def set_indeterminate(self, active=True):
        """Activa/desactiva modo indeterminado."""
        if active:
            self.progress_bar.setRange(0, 0)
        else:
            self.progress_bar.setRange(0, 100)
    
    def set_label(self, text):
        """Cambia el texto de la etiqueta."""
        self.label.setText(text)
    
    def reset(self):
        """Reinicia la barra."""
        self.set_value(0, "default")
