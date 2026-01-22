"""Control independiente para conversión de videos."""
import os
import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QSpinBox
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.shared.file_validator import get_file_validator
from ecb_tool.core.shared.paths import ORDER_PATH, PARAR_PATH
from ecb_tool.features.ui.legacy_src.application.process_controller import ProcessController
from ecb_tool.features.ui.pieces.text import header_text, body_text


class ConversionControl(QWidget):
    """Control independiente para conversión de videos."""
    
    started = pyqtSignal()
    stopped = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen_adapter = get_screen_adapter()
        self.controller = ProcessController()
        self.file_validator = get_file_validator()
        
        self.setStyleSheet("""
            QWidget {
                background-color: #141b28;
                border-radius: 18px;
                border: 1px solid #23304a;
            }
        """)
        
        self._init_ui()
        self._start_monitoring()
    
    def _init_ui(self):
        """Inicializa la interfaz."""
        layout = QVBoxLayout(self)
        margin = self.screen_adapter.get_margin(24)
        spacing = self.screen_adapter.get_spacing(16)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(spacing)
        
        # Header
        header = QHBoxLayout()
        header.setSpacing(12)
        
        # Indicador de estado
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("color: #666; font-size: 20px;")
        header.addWidget(self.status_indicator)
        
        # Título
        title = header_text("🎬 CONVERSIÓN DE VIDEOS", color="#24eaff", alignment=Qt.AlignmentFlag.AlignLeft)
        header.addWidget(title)
        
        header.addStretch()
        layout.addLayout(header)
        
        # Stats en grid compacto
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(self.screen_adapter.get_spacing(16))
        
        # Beats disponibles
        beats_widget = self._create_stat_widget("🎵", "Beats", "0")
        self.beats_value = beats_widget.findChild(QLabel, "value")
        stats_grid.addWidget(beats_widget)
        
        # Covers disponibles  
        covers_widget = self._create_stat_widget("🖼️", "Covers", "0")
        self.covers_value = covers_widget.findChild(QLabel, "value")
        stats_grid.addWidget(covers_widget)
        
        # Max videos
        max_widget = self._create_stat_widget("📹", "Max Videos", "0")
        self.max_value = max_widget.findChild(QLabel, "value")
        stats_grid.addWidget(max_widget)
        
        stats_grid.addStretch()
        layout.addLayout(stats_grid)
        
        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #23304a; max-height: 1px;")
        layout.addWidget(sep)
        
        # Controles
        controls = QHBoxLayout()
        controls.setSpacing(self.screen_adapter.get_spacing(20))
        
        # Órdenes
        orders_box = QVBoxLayout()
        orders_box.setSpacing(6)
        orders_label = body_text("Órdenes:", color="#8ad6ff", alignment=Qt.AlignmentFlag.AlignLeft, bold=True)
        orders_box.addWidget(orders_label)
        
        self.orders_spin = QSpinBox()
        self.orders_spin.setMinimum(1)
        self.orders_spin.setMaximum(999)
        self.orders_spin.setValue(1)
        self.orders_spin.setStyleSheet("""
            QSpinBox {
                background-color: #1a2332;
                color: #f4f8ff;
                border: 1px solid #23304a;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 16px;
                min-width: 80px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                background-color: #23304a;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #3998ff;
            }
        """)
        self.orders_spin.valueChanged.connect(self._on_orders_changed)
        orders_box.addWidget(self.orders_spin)
        controls.addLayout(orders_box)
        
        # BPV
        bpv_box = QVBoxLayout()
        bpv_box.setSpacing(6)
        bpv_label = body_text("Beats/Video:", color="#8ad6ff", alignment=Qt.AlignmentFlag.AlignLeft, bold=True)
        bpv_box.addWidget(bpv_label)
        
        self.bpv_spin = QSpinBox()
        self.bpv_spin.setMinimum(1)
        self.bpv_spin.setMaximum(100)
        self.bpv_spin.setValue(1)
        self.bpv_spin.setStyleSheet(self.orders_spin.styleSheet())
        self.bpv_spin.valueChanged.connect(self._on_bpv_changed)
        bpv_box.addWidget(self.bpv_spin)
        controls.addLayout(bpv_box)
        
        controls.addStretch()
        
        # Botón RUN/STOP
        self.run_button = QPushButton("▶ CONVERTIR")
        self.run_button.setObjectName("conversion_run_btn")
        min_height = self.screen_adapter.scale(50)
        self.run_button.setMinimumHeight(min_height)
        self.run_button.setMinimumWidth(self.screen_adapter.scale(160))
        font_size = self.screen_adapter.get_font_size(16)
        self.run_button.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
        self.run_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_button.setStyleSheet("""
            QPushButton#conversion_run_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #24eaff, stop:1 #3998ff);
                color: #fff;
                border: none;
                border-radius: 12px;
                letter-spacing: 1px;
                padding: 12px 24px;
            }
            QPushButton#conversion_run_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3998ff, stop:1 #5aa8ff);
            }
            QPushButton#conversion_run_btn:disabled {
                background: #2a3544;
                color: #5a6c82;
            }
        """)
        self.run_button.clicked.connect(self._toggle_conversion)
        controls.addWidget(self.run_button)
        
        layout.addLayout(controls)
        
        # Validación
        self.validation_label = body_text("", color="#8ad6ff", alignment=Qt.AlignmentFlag.AlignLeft)
        self.validation_label.setStyleSheet("color: #8ad6ff; font-size: 12px;")
        layout.addWidget(self.validation_label)
    
    def _create_stat_widget(self, icon, label, value):
        """Crea un widget de estadística compacto."""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #0f1419;
                border: 1px solid #23304a;
                border-radius: 10px;
                padding: 12px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        
        # Icon + Label
        top = QHBoxLayout()
        top.setSpacing(8)
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 18px;")
        top.addWidget(icon_label)
        
        text_label = QLabel(label)
        text_label.setStyleSheet("color: #8ad6ff; font-size: 11px; font-weight: bold;")
        top.addWidget(text_label)
        top.addStretch()
        layout.addLayout(top)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #24eaff;")
        layout.addWidget(value_label)
        
        return widget
    
    def _start_monitoring(self):
        """Inicia el monitoreo de estado."""
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self._update_state)
        self.monitor_timer.start(500)
        self._update_state()
    
    def _update_state(self):
        """Actualiza el estado del control."""
        validation = self.file_validator.check_all()
        conversion = validation['conversion']
        
        # Actualizar contadores
        self.beats_value.setText(str(conversion['beats']))
        self.covers_value.setText(str(conversion['covers']))
        
        # Calcular máximo de videos
        orders = self.orders_spin.value()
        bpv = self.bpv_spin.value()
        beats_available = conversion['beats']
        covers_available = conversion['covers']
        
        max_from_beats = beats_available // max(1, bpv * orders) if orders > 0 and bpv > 0 else 0
        max_from_covers = covers_available // max(1, orders) if orders > 0 else 0
        max_videos = min(max_from_beats, max_from_covers) * orders
        
        self.max_value.setText(str(max_videos))
        
        # Validación
        if not conversion['ready']:
            self.validation_label.setText(f"⚠️ Faltan recursos para convertir")
            self.validation_label.setStyleSheet("color: #ff9500; font-size: 12px;")
            self.run_button.setEnabled(False)
        else:
            self.validation_label.setText("✅ Listo para convertir")
            self.validation_label.setStyleSheet("color: #43b680; font-size: 12px;")
            self.run_button.setEnabled(True)
        
        # Check si está ejecutando
        is_running = self._is_conversion_running()
        if is_running:
            self.status_indicator.setStyleSheet("color: #24eaff; font-size: 20px;")
            self.run_button.setText("⏹ DETENER")
            self.run_button.setStyleSheet("""
                QPushButton#conversion_run_btn {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #F44336, stop:1 #E53935);
                    color: #fff;
                    border: none;
                    border-radius: 12px;
                    letter-spacing: 1px;
                    padding: 12px 24px;
                }
                QPushButton#conversion_run_btn:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #E53935, stop:1 #D32F2F);
                }
            """)
        else:
            self.status_indicator.setStyleSheet("color: #666; font-size: 20px;")
            self.run_button.setText("▶ CONVERTIR")
            self.run_button.setStyleSheet("""
                QPushButton#conversion_run_btn {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #24eaff, stop:1 #3998ff);
                    color: #fff;
                    border: none;
                    border-radius: 12px;
                    letter-spacing: 1px;
                    padding: 12px 24px;
                }
                QPushButton#conversion_run_btn:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3998ff, stop:1 #5aa8ff);
                }
                QPushButton#conversion_run_btn:disabled {
                    background: #2a3544;
                    color: #5a6c82;
                }
            """)
    
    def _is_conversion_running(self):
        """Verifica si la conversión está ejecutándose."""
        if not os.path.exists(ORDER_PATH):
            return False
        try:
            with open(ORDER_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('proceso', False) and data.get('modo', '') == 'convertir'
        except:
            return False
    
    def _on_orders_changed(self, value):
        """Actualiza órdenes en config."""
        self._update_config({'ordenes': value})
        self._update_state()
    
    def _on_bpv_changed(self, value):
        """Actualiza BPV en config."""
        self._update_config({'bpv': value})
        self._update_state()
    
    def _update_config(self, updates):
        """Actualiza el archivo de configuración."""
        try:
            if os.path.exists(ORDER_PATH):
                with open(ORDER_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}
            
            data.update(updates)
            
            with open(ORDER_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error updating config: {e}")
    
    def _toggle_conversion(self):
        """Inicia o detiene la conversión."""
        if self._is_conversion_running():
            self.controller.stop()
            self.stopped.emit()
        else:
            # Actualizar config
            self._update_config({
                'modo': 'convertir',
                'ordenes': self.orders_spin.value(),
                'bpv': self.bpv_spin.value(),
                'proceso': True
            })
            
            if os.path.exists(PARAR_PATH):
                os.remove(PARAR_PATH)
            
            self.controller.start('convertir', parent_widget=self)
            self.started.emit()
        
        QTimer.singleShot(200, self._update_state)
    
    def _update_config(self, updates):
        """Actualiza el archivo de configuración."""
        try:
            if os.path.exists(ORDER_PATH):
                with open(ORDER_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}
            
            data.update(updates)
            
            with open(ORDER_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error updating config: {e}")


__all__ = ['ConversionControl']