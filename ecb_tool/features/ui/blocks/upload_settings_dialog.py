import os
import json
import calendar
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSpinBox, QComboBox, QPushButton, QGroupBox, 
                             QGridLayout, QScrollArea, QWidget, QTextEdit,
                             QFrame, QSizePolicy, QTimeEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QTime
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor

from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.config import ConfigManager
from ecb_tool.core.shared.paths import ROOT_DIR, DATA_DIR, VIDEOS_DIR
from PyQt6.QtSvgWidgets import QSvgWidget

UPLOAD_CONFIG_PATH = os.path.join(ROOT_DIR, 'config', 'ajustes_subida.json')
SCHEDULE_PATH = os.path.join(ROOT_DIR, 'config', 'programacion_subidas.json')
TITLES_PATH = os.path.join(ROOT_DIR, 'data', 'titles.txt')
DESCRIPTION_PATH = os.path.join(ROOT_DIR, 'data', 'description.txt')
TRASH_DIR = os.path.join(ROOT_DIR, 'workspace', 'trash')
PROCESSED_DIR = os.path.join(ROOT_DIR, 'workspace', 'processed')
SVG_DIR = os.path.join(os.path.dirname(__file__), '..', 'pieces', 'svg')


class CalendarDayWidget(QFrame):
    """Widget editable para un día del calendario."""
    value_changed = pyqtSignal(int, int)  # day, count
    
    def __init__(self, year, month, day_number, upload_count=0):
        super().__init__()
        self.year = year
        self.month = month
        self.day_number = day_number
        self.upload_count = upload_count
        
        self.setFixedSize(80, 80)
        self.setStyleSheet("""
            CalendarDayWidget {
                background-color: #1a2332;
                border: 2px solid #23304a;
                border-radius: 8px;
            }
            CalendarDayWidget:hover {
                border: 2px solid #3998ff;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        
        # Número del día
        day_label = QLabel(str(day_number))
        day_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        day_label.setStyleSheet("color: #24eaff; border: none;")
        day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(day_label)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #23304a; border: none; max-height: 1px;")
        layout.addWidget(separator)
        
        # SpinBox editable
        self.spin = QSpinBox()
        self.spin.setMinimum(0)
        self.spin.setMaximum(99)
        self.spin.setValue(upload_count)
        self.spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin.setStyleSheet("""
            QSpinBox {
                background-color: #141b28;
                color: #43b680;
                border: 1px solid #43b680;
                border-radius: 4px;
                padding: 2px;
                font-size: 16px;
                font-weight: bold;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 16px;
                background-color: #23304a;
                border: none;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #3998ff;
            }
        """)
        self.spin.valueChanged.connect(self._on_value_changed)
        layout.addWidget(self.spin)
        
        # Label inferior
        videos_label = QLabel("videos")
        videos_label.setFont(QFont("Segoe UI", 9))
        videos_label.setStyleSheet("color: #8ad6ff; border: none;")
        videos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(videos_label)
    
    def _on_value_changed(self, value):
        self.upload_count = value
        # Actualizar borde según si hay uploads
        if value > 0:
            self.setStyleSheet("""
                CalendarDayWidget {
                    background-color: #1a2332;
                    border: 2px solid #43b680;
                    border-radius: 8px;
                }
                CalendarDayWidget:hover {
                    border: 2px solid #3998ff;
                }
            """)
        else:
            self.setStyleSheet("""
                CalendarDayWidget {
                    background-color: #1a2332;
                    border: 2px solid #23304a;
                    border-radius: 8px;
                }
                CalendarDayWidget:hover {
                    border: 2px solid #3998ff;
                }
            """)
        self.value_changed.emit(self.day_number, value)
    
    def get_value(self):
        return self.spin.value()
    
    def set_value(self, value):
        self.spin.setValue(value)


class CalendarWidget(QWidget):
    """Widget de calendario editable con programación de uploads."""
    schedule_changed = pyqtSignal()
    
    def __init__(self, parent_dialog):
        super().__init__()
        self.parent_dialog = parent_dialog
        self.current_date = datetime.now()
        self.day_widgets = {}  # {(year, month, day): widget}
        self._init_ui()
        self._load_schedule()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Header con mes/año y navegación
        header = QHBoxLayout()
        
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(35, 35)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #23304a;
                color: #f4f8ff;
                border: none;
                border-radius: 6px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #3998ff;
            }
        """)
        self.prev_btn.clicked.connect(self.prev_month)
        header.addWidget(self.prev_btn)
        
        self.month_label = QLabel()
        self.month_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.month_label.setStyleSheet("color: #24eaff;")
        self.month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(self.month_label, 1)
        
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(35, 35)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #23304a;
                color: #f4f8ff;
                border: none;
                border-radius: 6px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #3998ff;
            }
        """)
        self.next_btn.clicked.connect(self.next_month)
        header.addWidget(self.next_btn)
        
        layout.addLayout(header)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #23304a; max-height: 2px;")
        layout.addWidget(separator)
        
        # Días de la semana
        days_header = QHBoxLayout()
        days_header.setSpacing(8)
        for day in ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']:
            label = QLabel(day)
            label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            label.setStyleSheet("color: #8ad6ff;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFixedWidth(80)
            days_header.addWidget(label)
        layout.addLayout(days_header)
        
        # Grid del calendario
        self.calendar_grid = QGridLayout()
        self.calendar_grid.setSpacing(8)
        layout.addLayout(self.calendar_grid)
        
        self.update_calendar()
    
    def update_calendar(self):
        """Actualiza el calendario."""
        # Limpiar grid
        for i in reversed(range(self.calendar_grid.count())):
            widget = self.calendar_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Actualizar título
        months_es = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        month_name = months_es[self.current_date.month - 1]
        self.month_label.setText(f"{month_name} {self.current_date.year}")
        
        # Obtener información del mes
        year = self.current_date.year
        month = self.current_date.month
        cal = calendar.monthcalendar(year, month)
        
        # Llenar calendario
        for week_idx, week in enumerate(cal):
            for day_idx, day in enumerate(week):
                if day == 0:
                    # Día vacío
                    spacer = QWidget()
                    spacer.setFixedSize(80, 80)
                    self.calendar_grid.addWidget(spacer, week_idx, day_idx)
                else:
                    # Cargar programación guardada
                    schedule_key = f"{year}-{month:02d}-{day:02d}"
                    upload_count = self._get_day_schedule(schedule_key)
                    
                    # Crear widget del día
                    day_widget = CalendarDayWidget(year, month, day, upload_count)
                    day_widget.value_changed.connect(self._on_day_changed)
                    self.calendar_grid.addWidget(day_widget, week_idx, day_idx)
                    self.day_widgets[(year, month, day)] = day_widget
    
    def _on_day_changed(self, day, count):
        """Cuando cambia un día, guardar y actualizar."""
        year = self.current_date.year
        month = self.current_date.month
        schedule_key = f"{year}-{month:02d}-{day:02d}"
        self._save_day_schedule(schedule_key, count)
        self.schedule_changed.emit()
        self.parent_dialog._update_counters()
    
    def _load_schedule(self):
        """Carga la programación desde archivo."""
        if not os.path.exists(SCHEDULE_PATH):
            return {}
        try:
            with open(SCHEDULE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _get_day_schedule(self, date_key):
        """Obtiene la programación de un día específico."""
        schedule = self._load_schedule()
        return schedule.get(date_key, 0)
    
    def _save_day_schedule(self, date_key, count):
        """Guarda la programación de un día."""
        schedule = self._load_schedule()
        if count > 0:
            schedule[date_key] = count
        else:
            schedule.pop(date_key, None)
        
        os.makedirs(os.path.dirname(SCHEDULE_PATH), exist_ok=True)
        with open(SCHEDULE_PATH, 'w', encoding='utf-8') as f:
            json.dump(schedule, f, indent=2)
    
    def get_total_scheduled(self):
        """Retorna el total de videos programados."""
        schedule = self._load_schedule()
        return sum(schedule.values())
    
    def prev_month(self):
        """Ir al mes anterior."""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_calendar()
    
    def next_month(self):
        """Ir al mes siguiente."""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()


class UploadSettingsDialog(QDialog):
    """Diálogo de configuración de uploads con calendario y ajustes."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen_adapter = get_screen_adapter()
        
        self.setWindowTitle("Configuración de Uploads")
        self.setModal(True)
        
        # Tamaño adaptativo
        width, height = self.screen_adapter.get_dialog_size(1200, 850)
        self.setMinimumSize(int(width * 0.75), int(height * 0.75))
        self.resize(width, height)
        
        schema = {
            "subida": {
                "modo": "programado",  # programado (usa calendario)
                "hora_subida": "12:00",
                "autoborrado_videos": False,
                "papelera_videos": False,
                "estado": "publico",
                "contenido_niños": False
            }
        }
        
        self.config = ConfigManager(UPLOAD_CONFIG_PATH, schema)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #101722;
            }
            QLabel {
                color: #f4f8ff;
                font-size: 14px;
            }
            QGroupBox {
                color: #24eaff;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #23304a;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 18px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0px 10px;
                color: #24eaff;
            }
            QSpinBox, QComboBox {
                background-color: #1a2332;
                color: #f4f8ff;
                border: 1px solid #23304a;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton {
                background-color: #3998ff;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4fa8ff;
            }
            QPushButton#cancelButton {
                background-color: #2a3544;
            }
            QPushButton#cancelButton:hover {
                background-color: #344152;
            }
            QTextEdit {
                background-color: #1a2332;
                color: #f4f8ff;
                border: 1px solid #23304a;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
        """)
        
        self._init_ui()
        self._load_values()
        self._update_counters()
    
    def _init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # PANEL IZQUIERDO: Contadores y calendario
        left_panel = QVBoxLayout()
        left_panel.setSpacing(15)
        
        # Título
        title = QLabel("Programación de Uploads")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #24eaff; margin-bottom: 10px;")
        left_panel.addWidget(title)
        
        # Contadores
        counters_group = QGroupBox("Recursos")
        counters_layout = QGridLayout()
        counters_layout.setSpacing(12)
        
        # Videos
        videos_label = QLabel("Videos disponibles:")
        videos_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.videos_count = QLabel("0")
        self.videos_count.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.videos_count.setStyleSheet("color: #24eaff;")
        counters_layout.addWidget(videos_label, 0, 0)
        counters_layout.addWidget(self.videos_count, 0, 1)
        
        # Titles
        titles_label = QLabel("Títulos disponibles:")
        titles_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.titles_count = QLabel("0")
        self.titles_count.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.titles_count.setStyleSheet("color: #24eaff;")
        counters_layout.addWidget(titles_label, 1, 0)
        counters_layout.addWidget(self.titles_count, 1, 1)
        
        # Programados
        scheduled_label = QLabel("Videos programados:")
        scheduled_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.scheduled_count = QLabel("0")
        self.scheduled_count.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.scheduled_count.setStyleSheet("color: #43b680;")
        counters_layout.addWidget(scheduled_label, 2, 0)
        counters_layout.addWidget(self.scheduled_count, 2, 1)
        
        # Papelera con icono SVG
        trash_container = QHBoxLayout()
        trash_label = QLabel("Papelera:")
        trash_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        trash_icon = QSvgWidget(os.path.join(SVG_DIR, "carpeta.svg"))
        trash_icon.setFixedSize(20, 20)
        trash_container.addWidget(trash_icon)
        trash_container.addWidget(trash_label)
        trash_container.addStretch()
        trash_widget = QWidget()
        trash_widget.setLayout(trash_container)
        self.trash_count = QLabel("0")
        self.trash_count.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.trash_count.setStyleSheet("color: #ff9500;")
        counters_layout.addWidget(trash_widget, 3, 0)
        counters_layout.addWidget(self.trash_count, 3, 1)
        
        # Procesados con icono SVG
        processed_container = QHBoxLayout()
        processed_label = QLabel("Procesados:")
        processed_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        processed_icon = QSvgWidget(os.path.join(SVG_DIR, "archivo.svg"))
        processed_icon.setFixedSize(20, 20)
        processed_container.addWidget(processed_icon)
        processed_container.addWidget(processed_label)
        processed_container.addStretch()
        processed_widget = QWidget()
        processed_widget.setLayout(processed_container)
        self.processed_count = QLabel("0")
        self.processed_count.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.processed_count.setStyleSheet("color: #8ad6ff;")
        counters_layout.addWidget(processed_widget, 4, 0)
        counters_layout.addWidget(self.processed_count, 4, 1)
        
        counters_group.setLayout(counters_layout)
        left_panel.addWidget(counters_group)
        
        # Separador
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setStyleSheet("background-color: #23304a; max-height: 2px;")
        left_panel.addWidget(sep1)
        
        # Botón Set Description
        self.desc_button = QPushButton("📝 Set Description")
        self.desc_button.clicked.connect(self.open_description_editor)
        left_panel.addWidget(self.desc_button)
        
        # Separador
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("background-color: #23304a; max-height: 2px;")
        left_panel.addWidget(sep2)
        
        # Calendario
        calendar_group = QGroupBox("📅 Calendario de Programación")
        calendar_layout = QVBoxLayout()
        calendar_layout.setContentsMargins(15, 20, 15, 15)
        
        info_label = QLabel("✏️ Haz clic en los números para programar videos cada día")
        info_label.setStyleSheet("color: #8ad6ff; font-size: 12px; font-style: italic;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        calendar_layout.addWidget(info_label)
        
        self.calendar_widget = CalendarWidget(self)
        self.calendar_widget.schedule_changed.connect(self._update_counters)
        calendar_layout.addWidget(self.calendar_widget)
        calendar_group.setLayout(calendar_layout)
        left_panel.addWidget(calendar_group)
        
        main_layout.addLayout(left_panel, 2)
        
        # PANEL DERECHO: Ajustes
        right_panel = QVBoxLayout()
        right_panel.setSpacing(15)
        
        # Ajustes de subida
        settings_group = QGroupBox("Ajustes de Subida")
        settings_layout = QGridLayout()
        settings_layout.setSpacing(12)
        
        # Hora de subida
        time_label = QLabel("Hora de subida:")
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(12, 0))
        self.time_edit.setStyleSheet("""
            QTimeEdit {
                background-color: #1a2332;
                color: #f4f8ff;
                border: 1px solid #23304a;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
                min-width: 100px;
            }
        """)
        settings_layout.addWidget(time_label, 0, 0)
        settings_layout.addWidget(self.time_edit, 0, 1)
        
        # Estado del video
        status_label = QLabel("Estado:")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Público", "Privado", "No listado"])
        settings_layout.addWidget(status_label, 1, 0)
        settings_layout.addWidget(self.status_combo, 1, 1)
        
        settings_group.setLayout(settings_layout)
        right_panel.addWidget(settings_group)
        
        # Limpieza automática
        cleanup_group = QGroupBox("Limpieza tras Upload")
        cleanup_layout = QVBoxLayout()
        cleanup_layout.setSpacing(10)
        
        video_cleanup_label = QLabel("Videos subidos:")
        video_cleanup_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        video_cleanup_label.setStyleSheet("color: #24eaff;")
        cleanup_layout.addWidget(video_cleanup_label)
        
        self.delete_videos_check = QPushButton("Borrar completamente")
        self.delete_videos_check.setCheckable(True)
        self.delete_videos_check.clicked.connect(self._on_delete_videos_toggle)
        cleanup_layout.addWidget(self.delete_videos_check)
        
        self.trash_videos_check = QPushButton("Enviar a papelera")
        self.trash_videos_check.setCheckable(True)
        self.trash_videos_check.clicked.connect(self._on_trash_videos_toggle)
        cleanup_layout.addWidget(self.trash_videos_check)
        
        info_label = QLabel("ℹ️ Los títulos siempre se eliminan tras usar")
        info_label.setStyleSheet("color: #8ad6ff; font-size: 12px; font-style: italic;")
        cleanup_layout.addWidget(info_label)
        
        cleanup_group.setLayout(cleanup_layout)
        right_panel.addWidget(cleanup_group)
        
        right_panel.addStretch()
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_btn)
        
        right_panel.addLayout(buttons_layout)
        
        main_layout.addLayout(right_panel, 1)
    
    def _update_counters(self):
        """Actualiza los contadores de videos, títulos y programados."""
        # Contar videos
        videos = 0
        if os.path.isdir(VIDEOS_DIR):
            videos = len([f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith('.mp4')])
        self.videos_count.setText(str(videos))
        
        # Contar títulos
        titles = 0
        if os.path.isfile(TITLES_PATH):
            with open(TITLES_PATH, 'r', encoding='utf-8') as f:
                titles = len([l for l in f.readlines() if l.strip()])
        self.titles_count.setText(str(titles))
        
        # Programados (desde calendario)
        scheduled = self.calendar_widget.get_total_scheduled()
        self.scheduled_count.setText(str(scheduled))
        
        # Contar papelera
        trash = 0
        if os.path.isdir(TRASH_DIR):
            trash = len([f for f in os.listdir(TRASH_DIR) if f.lower().endswith('.mp4')])
        self.trash_count.setText(str(trash))
        
        # Contar procesados
        processed = 0
        if os.path.isdir(PROCESSED_DIR):
            processed = len([f for f in os.listdir(PROCESSED_DIR) if f.lower().endswith('.mp4')])
        self.processed_count.setText(str(processed))
    
    def _on_delete_videos_toggle(self):
        if self.delete_videos_check.isChecked():
            self.trash_videos_check.setChecked(False)
    
    def _on_trash_videos_toggle(self):
        if self.trash_videos_check.isChecked():
            self.delete_videos_check.setChecked(False)
    
    def open_description_editor(self):
        """Abre un editor para la descripción."""
        editor = QDialog(self)
        editor.setWindowTitle("Editar Descripción")
        editor.setMinimumSize(600, 500)
        editor.setModal(True)
        editor.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(editor)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        label = QLabel("Descripción de los videos:")
        label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        label.setStyleSheet("color: #24eaff;")
        layout.addWidget(label)
        
        text_edit = QTextEdit()
        text_edit.setMinimumHeight(300)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1a2332;
                color: #f4f8ff;
                border: 2px solid #23304a;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
        """)
        
        # Cargar descripción actual
        if os.path.isfile(DESCRIPTION_PATH):
            with open(DESCRIPTION_PATH, 'r', encoding='utf-8') as f:
                text_edit.setPlainText(f.read())
        
        layout.addWidget(text_edit)
        
        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        cancel = QPushButton("Cancelar")
        cancel.setObjectName("cancelButton")
        cancel.setMinimumWidth(120)
        cancel.clicked.connect(editor.reject)
        buttons.addWidget(cancel)
        
        save = QPushButton("Guardar")
        save.setMinimumWidth(120)
        save.clicked.connect(lambda: self._save_description(text_edit.toPlainText(), editor))
        buttons.addWidget(save)
        
        layout.addLayout(buttons)
        editor.exec()
    
    def _save_description(self, text, dialog):
        """Guarda la descripción."""
        os.makedirs(os.path.dirname(DESCRIPTION_PATH), exist_ok=True)
        with open(DESCRIPTION_PATH, 'w', encoding='utf-8') as f:
            f.write(text)
        dialog.accept()
    
    def _load_values(self):
        """Carga los valores actuales de la configuración."""
        upload_config = self.config.get("subida", {})
        
        # Hora de subida
        hora_str = upload_config.get("hora_subida", "12:00")
        try:
            hora, minuto = map(int, hora_str.split(':'))
            self.time_edit.setTime(QTime(hora, minuto))
        except:
            self.time_edit.setTime(QTime(12, 0))
        
        estado = upload_config.get("estado", "publico")
        status_map = {"publico": "Público", "privado": "Privado", "no_listado": "No listado"}
        self.status_combo.setCurrentText(status_map.get(estado, "Público"))
        
        self.delete_videos_check.setChecked(upload_config.get("autoborrado_videos", False))
        self.trash_videos_check.setChecked(upload_config.get("papelera_videos", False))
    
    def save_settings(self):
        """Guarda la configuración."""
        status_map = {"Público": "publico", "Privado": "privado", "No listado": "no_listado"}
        
        new_config = {
            "modo": "programado",
            "hora_subida": self.time_edit.time().toString("HH:mm"),
            "estado": status_map.get(self.status_combo.currentText(), "publico"),
            "autoborrado_videos": self.delete_videos_check.isChecked(),
            "papelera_videos": self.trash_videos_check.isChecked(),
            "contenido_niños": False
        }
        
        # Actualizar configuración usando el método correcto
        self.config.config["subida"] = new_config
        self.config.save()
        self.accept()


__all__ = ["UploadSettingsDialog"]
