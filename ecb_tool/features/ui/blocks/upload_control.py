"""Control independiente para subida de videos a YouTube."""
import os
import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.shared.file_validator import get_file_validator
from ecb_tool.core.shared.paths import ORDER_PATH, ROOT_DIR
from ecb_tool.features.ui.legacy_src.application.process_controller import ProcessController
from ecb_tool.features.ui.pieces.text import header_text, body_text


class UploadControl(QWidget):
    """Control independiente para subida de videos."""
    
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
        title = header_text("📤 SUBIDA A YOUTUBE", color="#3998ff", alignment=Qt.AlignmentFlag.AlignLeft)
        header.addWidget(title)
        
        header.addStretch()
        
        # Estado de autenticación
        self.auth_status = body_text("", color="#8ad6ff", alignment=Qt.AlignmentFlag.AlignRight)
        header.addWidget(self.auth_status)
        
        layout.addLayout(header)
        
        # Stats en grid compacto
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(self.screen_adapter.get_spacing(16))
        
        # Videos disponibles
        videos_widget = self._create_stat_widget("📹", "Videos", "0")
        self.videos_value = videos_widget.findChild(QLabel, "value")
        stats_grid.addWidget(videos_widget)
        
        # Títulos disponibles  
        titles_widget = self._create_stat_widget("📝", "Títulos", "0")
        self.titles_value = titles_widget.findChild(QLabel, "value")
        stats_grid.addWidget(titles_widget)
        
        # Programados
        scheduled_widget = self._create_stat_widget("📅", "Programados", "0")
        self.scheduled_value = scheduled_widget.findChild(QLabel, "value")
        stats_grid.addWidget(scheduled_widget)
        
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
        
        # Botón de configuración
        config_button = QPushButton("⚙️ Configurar")
        config_button.setObjectName("upload_config_btn")
        min_height = self.screen_adapter.scale(48)
        config_button.setMinimumHeight(min_height)
        font_size = self.screen_adapter.get_font_size(14)
        config_button.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
        config_button.setCursor(Qt.CursorShape.PointingHandCursor)
        config_button.setStyleSheet("""
            QPushButton#upload_config_btn {
                background-color: #1a2332;
                color: #8ad6ff;
                border: 1px solid #23304a;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton#upload_config_btn:hover {
                background-color: #23304a;
                border: 1px solid #3998ff;
            }
        """)
        config_button.clicked.connect(self._open_upload_settings)
        controls.addWidget(config_button)
        
        controls.addStretch()
        
        # Botón RUN/STOP
        self.run_button = QPushButton("▶ SUBIR AHORA")
        self.run_button.setObjectName("upload_run_btn")
        min_height = self.screen_adapter.scale(50)
        self.run_button.setMinimumHeight(min_height)
        self.run_button.setMinimumWidth(self.screen_adapter.scale(180))
        font_size = self.screen_adapter.get_font_size(16)
        self.run_button.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
        self.run_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_button.setStyleSheet("""
            QPushButton#upload_run_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3998ff, stop:1 #5aa8ff);
                color: #fff;
                border: none;
                border-radius: 12px;
                letter-spacing: 1px;
                padding: 12px 24px;
            }
            QPushButton#upload_run_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4fa8ff, stop:1 #6bb8ff);
            }
            QPushButton#upload_run_btn:disabled {
                background: #2a3544;
                color: #5a6c82;
            }
        """)
        self.run_button.clicked.connect(self._toggle_upload)
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
        value_label.setStyleSheet("color: #3998ff;")
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
        upload = validation['upload']
        
        # Actualizar contadores
        self.videos_value.setText(str(upload['videos']))
        self.titles_value.setText(str(upload['titles']))
        
        # Programados
        scheduled_count = self._get_scheduled_count()
        self.scheduled_value.setText(str(scheduled_count))
        
        # Autenticación
        if self._is_authenticated():
            self.auth_status.setText("✅ Autenticado")
            self.auth_status.setStyleSheet("color: #43b680; font-size: 12px;")
        else:
            self.auth_status.setText("⚠️ No autenticado")
            self.auth_status.setStyleSheet("color: #ff9500; font-size: 12px;")
        
        # Validación
        if not self._is_authenticated():
            self.validation_label.setText("⚠️ Haz clic en 'Sign In' arriba a la derecha")
            self.validation_label.setStyleSheet("color: #ff9500; font-size: 12px;")
            self.run_button.setEnabled(False)
        elif not upload['ready']:
            self.validation_label.setText(f"⚠️ Faltan recursos para subir")
            self.validation_label.setStyleSheet("color: #ff9500; font-size: 12px;")
            self.run_button.setEnabled(False)
        elif scheduled_count == 0:
            self.validation_label.setText("ℹ️ Configura la programación primero")
            self.validation_label.setStyleSheet("color: #8ad6ff; font-size: 12px;")
            self.run_button.setEnabled(True)
        else:
            self.validation_label.setText(f"✅ Listo para subir {scheduled_count} videos")
            self.validation_label.setStyleSheet("color: #43b680; font-size: 12px;")
            self.run_button.setEnabled(True)
        
        # Check si está ejecutando
        is_running = self._is_upload_running()
        if is_running:
            self.status_indicator.setStyleSheet("color: #3998ff; font-size: 20px;")
            self.run_button.setText("⏹ DETENER")
            self.run_button.setStyleSheet("""
                QPushButton#upload_run_btn {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #F44336, stop:1 #E53935);
                    color: #fff;
                    border: none;
                    border-radius: 12px;
                    letter-spacing: 1px;
                    padding: 12px 24px;
                }
                QPushButton#upload_run_btn:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #E53935, stop:1 #D32F2F);
                }
            """)
        else:
            self.status_indicator.setStyleSheet("color: #666; font-size: 20px;")
            self.run_button.setText("▶ SUBIR AHORA")
            self.run_button.setStyleSheet("""
                QPushButton#upload_run_btn {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3998ff, stop:1 #5aa8ff);
                    color: #fff;
                    border: none;
                    border-radius: 12px;
                    letter-spacing: 1px;
                    padding: 12px 24px;
                }
                QPushButton#upload_run_btn:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4fa8ff, stop:1 #6bb8ff);
                }
                QPushButton#upload_run_btn:disabled {
                    background: #2a3544;
                    color: #5a6c82;
                }
            """)
    
    def _is_authenticated(self):
        """Verifica si está autenticado."""
        credentials_path = os.path.join(ROOT_DIR, 'oauth', 'credentials.json')
        if not os.path.exists(credentials_path):
            return False
        try:
            with open(credentials_path, 'r', encoding='utf-8') as f:
                creds = json.load(f)
                return bool(creds.get('token'))
        except:
            return False
    
    def _get_scheduled_count(self):
        """Obtiene la cantidad de videos programados."""
        schedule_path = os.path.join(ROOT_DIR, 'config', 'programacion_subidas.json')
        if not os.path.exists(schedule_path):
            return 0
        try:
            with open(schedule_path, 'r', encoding='utf-8') as f:
                schedule = json.load(f)
                return sum(schedule.values())
        except:
            return 0
    
    def _is_upload_running(self):
        """Verifica si la subida está ejecutándose."""
        if not os.path.exists(ORDER_PATH):
            return False
        try:
            with open(ORDER_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('proceso', False) and data.get('modo', '') == 'subir'
        except:
            return False
    
    def _open_upload_settings(self):
        """Abre el diálogo de configuración de subidas."""
        from ecb_tool.features.ui.blocks.upload_settings_dialog_v2 import UploadSettingsDialogV2
        dialog = UploadSettingsDialogV2(self)
        dialog.exec()
        QTimer.singleShot(200, self._update_state)
    
    def _toggle_upload(self):
        """Inicia o detiene la subida."""
        if self._is_upload_running():
            self.controller.stop()
            self.stopped.emit()
        else:
            # Mostrar diálogo de confirmación
            from ecb_tool.features.ui.blocks.upload_confirmation_dialog import UploadConfirmationDialog
            
            confirmation = UploadConfirmationDialog(self)
            
            def on_modify():
                self._open_upload_settings()
            
            confirmation.modify_requested.connect(on_modify)
            
            result = confirmation.exec()
            
            if result == confirmation.DialogCode.Accepted:
                # Iniciar subida
                self._update_config({
                    'modo': 'subir',
                    'proceso': True
                })
                
                self.controller.start('subir', parent_widget=self)
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


__all__ = ['UploadControl']

