"""Pantalla principal (Home)."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, QEvent, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QKeyEvent, QFont

from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.shared.theme_manager import get_theme_manager
from ecb_tool.features.ui.blocks.status_panel import StatusPanel
from ecb_tool.features.ui.blocks.conversion_control import ConversionControl
from ecb_tool.features.ui.blocks.upload_control import UploadControl
from ecb_tool.features.ui.blocks.counters_panel import CountersPanel
from ecb_tool.features.ui.blocks.conversion_progress_panel import ConversionProgressPanel
from ecb_tool.features.ui.pieces.text import title_text


class HomeScreen(QWidget):
    """Pantalla principal de la aplicación."""
    
    def __init__(self):
        super().__init__()
        self.screen_adapter = get_screen_adapter()
        self.theme_manager = get_theme_manager()
        self._init_ui()
        self._apply_theme()
        self.theme_manager.theme_changed.connect(self._apply_theme)
    
    def keyPressEvent(self, event: QKeyEvent):
        """Prevenir que ESC cierre la ventana."""
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
        else:
            super().keyPressEvent(event)
    
    def _init_ui(self):
        """Inicializa la interfaz."""
        layout_global = QVBoxLayout(self)
        spacing = self.screen_adapter.get_spacing(15)
        margin = self.screen_adapter.get_margin(20)
        layout_global.setContentsMargins(margin, margin, margin, margin)
        layout_global.setSpacing(spacing)

        # Header con título
        header = QHBoxLayout()
        self.title = title_text("ECB TOOL", color="#24eaff", bold=True)
        header.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)
        header.addStretch(1)
        layout_global.addLayout(header)

        # Body con distribución horizontal
        body = QHBoxLayout()
        body.setSpacing(self.screen_adapter.get_spacing(20))

        # Zona central (controles separados + contadores)
        center_zone = QVBoxLayout()
        center_zone.setSpacing(self.screen_adapter.get_spacing(15))

        # Control de conversión
        self.conversion_control = ConversionControl()
        self.conversion_control.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        center_zone.addWidget(self.conversion_control)

        # Control de subida
        self.upload_control = UploadControl()
        self.upload_control.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        center_zone.addWidget(self.upload_control)

        # Panel de contadores
        self.counters_panel = CountersPanel()
        self.counters_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        center_zone.addWidget(self.counters_panel)
        
        # Panel de progreso de conversión
        self.conversion_progress = ConversionProgressPanel()
        self.conversion_progress.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        center_zone.addWidget(self.conversion_progress)
        
        # Stretch para empujar contenido arriba
        center_zone.addStretch(1)

        # Agregar zona central al body (ocupa todo el ancho ahora)
        body.addLayout(center_zone, 1)

        layout_global.addLayout(body, 1)
        
        # Panel de estado deslizante (overlay)
        self.status_panel = StatusPanel(self)
        self.status_panel.setFixedWidth(380)
        self.status_panel_visible = False
        self._setup_sliding_panel()
        
        # Botón flotante para mostrar/ocultar panel
        self.toggle_status_btn = QPushButton("📊", self)
        self.toggle_status_btn.setFont(QFont("Segoe UI", 20))
        self.toggle_status_btn.setFixedSize(56, 56)
        self.toggle_status_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_status_btn.setToolTip("Mostrar/Ocultar Panel de Estados")
        self.toggle_status_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #24eaff, stop:1 #3998ff);
                border: 2px solid rgba(36, 234, 255, 0.6);
                border-radius: 28px;
                color: white;
                font-size: 24px;
                padding: 0px;
            }
            QPushButton:hover {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3998ff, stop:1 #5aa8ff);
                border: 2px solid rgba(36, 234, 255, 1.0);
            }
            QPushButton:pressed {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a7a8a, stop:1 #2a5a7a);
            }
        """)
        self.toggle_status_btn.clicked.connect(self._toggle_status_panel)
        self._position_toggle_button()
    
    def _setup_sliding_panel(self):
        """Configura el panel deslizante."""
        # Posicionar panel fuera de la pantalla (a la derecha)
        self.status_panel.move(self.width(), 0)
        self.status_panel.setFixedHeight(self.height())
        self.status_panel.raise_()
        
        # Animación de deslizamiento
        self.slide_animation = QPropertyAnimation(self.status_panel, b"pos")
        self.slide_animation.setDuration(300)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def _position_toggle_button(self):
        """Posiciona el botón flotante en la esquina inferior derecha."""
        margin = 20
        x = self.width() - self.toggle_status_btn.width() - margin
        y = self.height() - self.toggle_status_btn.height() - margin
        self.toggle_status_btn.move(x, y)
        self.toggle_status_btn.raise_()
    
    def _toggle_status_panel(self):
        """Muestra/oculta el panel de estado con animación."""
        from PyQt6.QtCore import QPoint
        
        panel_width = self.status_panel.width()
        
        if self.status_panel_visible:
            # Ocultar: deslizar hacia la derecha
            start_x = self.width() - panel_width
            end_x = self.width()
            self.toggle_status_btn.setText("📊")
            self.toggle_status_btn.setToolTip("Mostrar Panel de Estados")
        else:
            # Mostrar: deslizar desde la derecha
            start_x = self.width()
            end_x = self.width() - panel_width
            self.toggle_status_btn.setText("✖")
            self.toggle_status_btn.setToolTip("Ocultar Panel de Estados")
        
        self.slide_animation.setStartValue(QPoint(start_x, 0))
        self.slide_animation.setEndValue(QPoint(end_x, 0))
        self.slide_animation.start()
        
        self.status_panel_visible = not self.status_panel_visible
    
    def resizeEvent(self, event):
        """Manejar redimensionamiento."""
        super().resizeEvent(event)
        # Reposicionar elementos flotantes
        self._position_toggle_button()
        if hasattr(self, 'status_panel'):
            self.status_panel.setFixedHeight(self.height())
            if self.status_panel_visible:
                panel_width = self.status_panel.width()
                self.status_panel.move(self.width() - panel_width, 0)
            else:
                self.status_panel.move(self.width(), 0)
    
    def _apply_theme(self):
        """Aplica el tema actual."""
        theme = self.theme_manager.get_current_theme()
        self.title.setStyleSheet(f"color: {theme['accent']};")
