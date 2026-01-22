"""Configuración de Upload mejorada con calendario real y programación inteligente."""
import os
import json
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGroupBox, QGridLayout, QSpinBox,
                             QComboBox, QFrame, QCalendarWidget, QWidget,
                             QScrollArea, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QTextCharFormat, QBrush, QColor
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
# SVG_DIR debe apuntar a la carpeta svg que está en el mismo paquete
SVG_DIR = os.path.join(os.path.dirname(__file__), '..', 'pieces', 'svg')


class SmartCalendar(QCalendarWidget):
    """Calendario inteligente que se actualiza a la fecha actual y maneja programación."""
    
    schedule_updated = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scheduled_days = {}  # {QDate: int}  día -> cantidad de videos
        
        # Estilo del calendario
        self.setStyleSheet("""
            QCalendarWidget {
                background-color: #1a2332;
                color: #f4f8ff;
            }
            QCalendarWidget QWidget {
                background-color: #1a2332;
                color: #f4f8ff;
            }
            QCalendarWidget QAbstractItemView {
                background-color: #141b28;
                color: #f4f8ff;
                selection-background-color: #3998ff;
                selection-color: #fff;
            }
            QCalendarWidget QToolButton {
                color: #24eaff;
                background-color: #23304a;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #3998ff;
            }
            QCalendarWidget QMenu {
                background-color: #1a2332;
                color: #f4f8ff;
            }
            QCalendarWidget QSpinBox {
                background-color: #23304a;
                color: #f4f8ff;
                border: 1px solid #3998ff;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        
        # Actualizar a la fecha actual cada vez que se muestra
        self.setSelectedDate(QDate.currentDate())
        self.setMinimumDate(QDate.currentDate())  # No permitir fechas pasadas
        
        self.clicked.connect(self._on_date_clicked)
        self._load_schedule()
        self._update_highlights()
    
    def _on_date_clicked(self, date):
        """Cuando se hace clic en una fecha."""
        # No hacer nada aquí, la selección se maneja externamente
        pass
    
    def set_videos_for_date(self, date, count):
        """Establece la cantidad de videos para una fecha."""
        if count > 0:
            self.scheduled_days[date] = count
        elif date in self.scheduled_days:
            del self.scheduled_days[date]
        self._update_highlights()
        self.schedule_updated.emit()
    
    def get_videos_for_date(self, date):
        """Obtiene la cantidad de videos programados para una fecha."""
        return self.scheduled_days.get(date, 0)
    
    def get_total_scheduled(self):
        """Retorna el total de videos programados."""
        return sum(self.scheduled_days.values())
    
    def get_scheduled_days_count(self):
        """Retorna la cantidad de días con videos programados."""
        return len(self.scheduled_days)
    
    def clear_schedule(self):
        """Limpia toda la programación."""
        self.scheduled_days.clear()
        self._update_highlights()
        self.schedule_updated.emit()
    
    def _update_highlights(self):
        """Actualiza los días destacados en el calendario."""
        # Formato para días programados
        format_scheduled = QTextCharFormat()
        format_scheduled.setBackground(QBrush(QColor("#43b680")))
        format_scheduled.setForeground(QBrush(QColor("#fff")))
        format_scheduled.setFontWeight(QFont.Weight.Bold)
        
        # Aplicar formato a días programados
        for date in self.scheduled_days.keys():
            self.setDateTextFormat(date, format_scheduled)
    
    def _load_schedule(self):
        """Carga la programación guardada."""
        if os.path.exists(SCHEDULE_PATH):
            try:
                with open(SCHEDULE_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for date_str, count in data.items():
                        date = QDate.fromString(date_str, "yyyy-MM-dd")
                        if date.isValid() and date >= QDate.currentDate():
                            self.scheduled_days[date] = count
                self._update_highlights()
            except:
                pass
    
    def save_schedule(self):
        """Guarda la programación."""
        data = {}
        for date, count in self.scheduled_days.items():
            data[date.toString("yyyy-MM-dd")] = count
        
        os.makedirs(os.path.dirname(SCHEDULE_PATH), exist_ok=True)
        with open(SCHEDULE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)


class UploadSettingsDialogV2(QDialog):
    """Diálogo mejorado de configuración de uploads."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen_adapter = get_screen_adapter()
        
        self.setWindowTitle("⚙️ Configuración de Uploads - YouTube")
        self.setModal(True)
        
        # Tamaño
        width, height = self.screen_adapter.get_dialog_size(1400, 900)
        self.setMinimumSize(int(width * 0.8), int(height * 0.8))
        self.resize(width, height)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #101722;
            }
            QLabel {
                color: #f4f8ff;
            }
            QGroupBox {
                color: #24eaff;
                font-size: 15px;
                font-weight: bold;
                border: 2px solid #23304a;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0px 8px;
            }
            QPushButton {
                background-color: #3998ff;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4fa8ff;
            }
            QPushButton:disabled {
                background-color: #2a3544;
                color: #5a6c82;
            }
            QPushButton#cancelButton {
                background-color: #2a3544;
            }
            QPushButton#cancelButton:hover {
                background-color: #344152;
            }
            QSpinBox, QComboBox {
                background-color: #1a2332;
                color: #f4f8ff;
                border: 1px solid #23304a;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                background-color: #23304a;
                border: none;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #3998ff;
            }
        """)
        
        self._init_ui()
        self._update_all_counters()
    
    def _init_ui(self):
        """Inicializa la interfaz."""
        main_layout = QVBoxLayout(self)
        margin = self.screen_adapter.get_margin(20)
        main_layout.setContentsMargins(margin, margin, margin, margin)
        main_layout.setSpacing(self.screen_adapter.get_spacing(16))
        
        # Título principal
        title = QLabel("📊 Configuración Inteligente de Subidas a YouTube")
        title.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(22), QFont.Weight.Bold))
        title.setStyleSheet("color: #24eaff; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Layout horizontal principal
        content_layout = QHBoxLayout()
        content_layout.setSpacing(self.screen_adapter.get_spacing(20))
        
        # ========== PANEL IZQUIERDO: CONTADORES Y CALENDARIO ==========
        left_panel = QVBoxLayout()
        left_panel.setSpacing(self.screen_adapter.get_spacing(16))
        
        # Contadores de recursos
        counters_group = self._create_counters_group()
        left_panel.addWidget(counters_group)
        
        # Calendario
        calendar_group = self._create_calendar_group()
        left_panel.addWidget(calendar_group, 1)
        
        content_layout.addLayout(left_panel, 2)
        
        # ========== PANEL DERECHO: PROGRAMACIÓN INTELIGENTE ==========
        right_panel = QVBoxLayout()
        right_panel.setSpacing(self.screen_adapter.get_spacing(16))
        
        # Sistema de programación inteligente
        smart_schedule_group = self._create_smart_schedule_group()
        right_panel.addWidget(smart_schedule_group)
        
        # Ajustes adicionales
        settings_group = self._create_settings_group()
        right_panel.addWidget(settings_group)
        
        right_panel.addStretch()
        
        content_layout.addLayout(right_panel, 1)
        
        main_layout.addLayout(content_layout)
        
        # Botones de acción
        buttons_layout = self._create_buttons()
        main_layout.addLayout(buttons_layout)
    
    def _create_counters_group(self):
        """Crea el grupo de contadores de recursos."""
        group = QGroupBox("📦 Recursos Disponibles")
        layout = QGridLayout()
        layout.setSpacing(self.screen_adapter.get_spacing(12))
        
        # Videos disponibles
        videos_icon = QSvgWidget(os.path.join(SVG_DIR, "archivo.svg"))
        videos_icon.setFixedSize(24, 24)
        videos_label = QLabel("Videos listos:")
        videos_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.videos_count = QLabel("0")
        self.videos_count.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.videos_count.setStyleSheet("color: #24eaff;")
        layout.addWidget(videos_icon, 0, 0)
        layout.addWidget(videos_label, 0, 1)
        layout.addWidget(self.videos_count, 0, 2, Qt.AlignmentFlag.AlignRight)
        
        # Títulos disponibles
        titles_icon = QSvgWidget(os.path.join(SVG_DIR, "archivo.svg"))
        titles_icon.setFixedSize(24, 24)
        titles_label = QLabel("Títulos disponibles:")
        titles_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.titles_count = QLabel("0")
        self.titles_count.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.titles_count.setStyleSheet("color: #43b680;")
        layout.addWidget(titles_icon, 1, 0)
        layout.addWidget(titles_label, 1, 1)
        layout.addWidget(self.titles_count, 1, 2, Qt.AlignmentFlag.AlignRight)
        
        # Descripciones (solo 1)
        desc_icon = QSvgWidget(os.path.join(SVG_DIR, "archivo.svg"))
        desc_icon.setFixedSize(24, 24)
        desc_label = QLabel("Descripción:")
        desc_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.desc_count = QLabel("0")
        self.desc_count.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.desc_count.setStyleSheet("color: #ff9500;")
        layout.addWidget(desc_icon, 2, 0)
        layout.addWidget(desc_label, 2, 1)
        layout.addWidget(self.desc_count, 2, 2, Qt.AlignmentFlag.AlignRight)
        
        # Botón editar descripción
        edit_desc_btn = QPushButton("✏️ Editar Descripción")
        edit_desc_btn.clicked.connect(self._edit_description)
        layout.addWidget(edit_desc_btn, 3, 0, 1, 3)
        
        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #23304a;")
        layout.addWidget(sep, 4, 0, 1, 3)
        
        # Videos programados
        scheduled_icon = QSvgWidget(os.path.join(SVG_DIR, "check.svg"))
        scheduled_icon.setFixedSize(24, 24)
        scheduled_label = QLabel("Videos programados:")
        scheduled_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.scheduled_count = QLabel("0")
        self.scheduled_count.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.scheduled_count.setStyleSheet("color: #43b680;")
        layout.addWidget(scheduled_icon, 5, 0)
        layout.addWidget(scheduled_label, 5, 1)
        layout.addWidget(self.scheduled_count, 5, 2, Qt.AlignmentFlag.AlignRight)
        
        # Días seleccionados
        days_label = QLabel("Días seleccionados:")
        days_label.setFont(QFont("Segoe UI", 12))
        self.days_count = QLabel("0")
        self.days_count.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.days_count.setStyleSheet("color: #8ad6ff;")
        layout.addWidget(days_label, 6, 1)
        layout.addWidget(self.days_count, 6, 2, Qt.AlignmentFlag.AlignRight)
        
        group.setLayout(layout)
        return group
    
    def _create_calendar_group(self):
        """Crea el grupo del calendario."""
        group = QGroupBox("📅 Calendario de Programación")
        layout = QVBoxLayout()
        
        info = QLabel("✨ Los días con videos programados aparecen en verde")
        info.setStyleSheet("color: #8ad6ff; font-size: 12px; font-style: italic;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        self.calendar = SmartCalendar()
        self.calendar.schedule_updated.connect(self._update_all_counters)
        layout.addWidget(self.calendar)
        
        group.setLayout(layout)
        return group
    
    def _create_smart_schedule_group(self):
        """Crea el grupo de programación inteligente."""
        group = QGroupBox("🧠 Programación Inteligente")
        layout = QVBoxLayout()
        layout.setSpacing(self.screen_adapter.get_spacing(14))
        
        # Explicación
        info = QLabel(
            "Define cuántos videos quieres subir por día y cuántos días.\n"
            "El sistema calculará automáticamente la distribución de horas."
        )
        info.setStyleSheet("color: #8ad6ff; font-size: 12px; padding: 8px; background-color: #1a2332; border-radius: 6px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Videos por día
        vpd_layout = QHBoxLayout()
        vpd_label = QLabel("Videos por día:")
        vpd_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.videos_per_day_spin = QSpinBox()
        self.videos_per_day_spin.setMinimum(1)
        self.videos_per_day_spin.setMaximum(50)
        self.videos_per_day_spin.setValue(10)
        self.videos_per_day_spin.setMinimumWidth(120)
        self.videos_per_day_spin.valueChanged.connect(self._on_schedule_params_changed)
        vpd_layout.addWidget(vpd_label)
        vpd_layout.addStretch()
        vpd_layout.addWidget(self.videos_per_day_spin)
        layout.addLayout(vpd_layout)
        
        # Cantidad de días
        days_layout = QHBoxLayout()
        days_label = QLabel("Cantidad de días:")
        days_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.days_spin = QSpinBox()
        self.days_spin.setMinimum(1)
        self.days_spin.setMaximum(365)
        self.days_spin.setValue(30)
        self.days_spin.setMinimumWidth(120)
        self.days_spin.valueChanged.connect(self._on_schedule_params_changed)
        days_layout.addWidget(days_label)
        days_layout.addStretch()
        days_layout.addWidget(self.days_spin)
        layout.addLayout(days_layout)
        
        # Cálculos automáticos
        calc_frame = QFrame()
        calc_frame.setStyleSheet("background-color: #1a2332; border-radius: 8px; padding: 12px;")
        calc_layout = QVBoxLayout(calc_frame)
        
        self.total_videos_label = QLabel("📊 Total a programar: 0 videos")
        self.total_videos_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.total_videos_label.setStyleSheet("color: #24eaff;")
        calc_layout.addWidget(self.total_videos_label)
        
        self.hour_distribution_label = QLabel("⏰ Distancia entre uploads: --")
        self.hour_distribution_label.setFont(QFont("Segoe UI", 11))
        self.hour_distribution_label.setStyleSheet("color: #8ad6ff;")
        calc_layout.addWidget(self.hour_distribution_label)
        
        self.validation_label = QLabel("")
        self.validation_label.setFont(QFont("Segoe UI", 11))
        self.validation_label.setWordWrap(True)
        calc_layout.addWidget(self.validation_label)
        
        layout.addWidget(calc_frame)
        
        # Botón aplicar programación
        self.apply_schedule_btn = QPushButton("✨ Aplicar Programación Automática")
        self.apply_schedule_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #43b680, stop:1 #3998ff);
                padding: 14px 24px;
                font-size: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #52c690, stop:1 #4fa8ff);
            }
        """)
        self.apply_schedule_btn.clicked.connect(self._apply_smart_schedule)
        layout.addWidget(self.apply_schedule_btn)
        
        # Botón limpiar programación
        clear_btn = QPushButton("🗑️ Limpiar Programación")
        clear_btn.setObjectName("cancelButton")
        clear_btn.clicked.connect(self._clear_schedule)
        layout.addWidget(clear_btn)
        
        group.setLayout(layout)
        self._on_schedule_params_changed()  # Calcular inicial
        return group
    
    def _create_settings_group(self):
        """Crea el grupo de ajustes adicionales."""
        group = QGroupBox("⚙️ Ajustes de Subida")
        layout = QVBoxLayout()
        layout.setSpacing(self.screen_adapter.get_spacing(12))
        
        # Estado del video
        status_layout = QHBoxLayout()
        status_label = QLabel("Estado del video:")
        status_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Público", "Privado", "No listado"])
        status_layout.addWidget(status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.status_combo)
        layout.addLayout(status_layout)
        
        # Limpieza tras upload
        cleanup_label = QLabel("Tras subir videos:")
        cleanup_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        cleanup_label.setStyleSheet("color: #24eaff; margin-top: 10px;")
        layout.addWidget(cleanup_label)
        
        self.delete_videos_btn = QPushButton("❌ Eliminar definitivamente")
        self.delete_videos_btn.setCheckable(True)
        self.delete_videos_btn.clicked.connect(self._on_cleanup_option_changed)
        layout.addWidget(self.delete_videos_btn)
        
        self.trash_videos_btn = QPushButton("🗑️ Mover a papelera")
        self.trash_videos_btn.setCheckable(True)
        self.trash_videos_btn.clicked.connect(self._on_cleanup_option_changed)
        layout.addWidget(self.trash_videos_btn)
        
        info = QLabel("ℹ️ Los títulos usados siempre se eliminan automáticamente")
        info.setStyleSheet("color: #8ad6ff; font-size: 11px; font-style: italic; margin-top: 8px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        group.setLayout(layout)
        return group
    
    def _create_buttons(self):
        """Crea los botones de acción."""
        layout = QHBoxLayout()
        layout.setSpacing(self.screen_adapter.get_spacing(12))
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setMinimumWidth(150)
        layout.addWidget(cancel_btn)
        
        layout.addStretch()
        
        save_btn = QPushButton("💾 Guardar Configuración")
        save_btn.clicked.connect(self._save_and_close)
        save_btn.setMinimumWidth(200)
        layout.addWidget(save_btn)
        
        return layout
    
    def _update_all_counters(self):
        """Actualiza todos los contadores."""
        # Videos disponibles
        videos = 0
        if os.path.isdir(VIDEOS_DIR):
            videos = len([f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith('.mp4')])
        self.videos_count.setText(str(videos))
        
        # Títulos disponibles
        titles = 0
        if os.path.isfile(TITLES_PATH):
            with open(TITLES_PATH, 'r', encoding='utf-8') as f:
                titles = len([l for l in f.readlines() if l.strip()])
        self.titles_count.setText(str(titles))
        
        # Descripciones (0 o 1)
        desc_count = 0
        if os.path.isfile(DESCRIPTION_PATH):
            with open(DESCRIPTION_PATH, 'r', encoding='utf-8') as f:
                if f.read().strip():
                    desc_count = 1
        self.desc_count.setText(str(desc_count))
        
        # Videos programados y días
        self.scheduled_count.setText(str(self.calendar.get_total_scheduled()))
        self.days_count.setText(str(self.calendar.get_scheduled_days_count()))
    
    def _on_schedule_params_changed(self):
        """Se llama cuando cambian los parámetros de programación."""
        videos_per_day = self.videos_per_day_spin.value()
        days = self.days_spin.value()
        total_videos = videos_per_day * days
        
        # Actualizar label de total
        self.total_videos_label.setText(f"📊 Total a programar: {total_videos} videos")
        
        # Calcular distribución de horas (24 horas / videos por día)
        if videos_per_day > 0:
            hours_between = 24.0 / videos_per_day
            if hours_between >= 1:
                self.hour_distribution_label.setText(
                    f"⏰ Distancia entre uploads: {hours_between:.1f} horas"
                )
            else:
                minutes_between = hours_between * 60
                self.hour_distribution_label.setText(
                    f"⏰ Distancia entre uploads: {minutes_between:.0f} minutos"
                )
        
        # Validación inteligente
        videos_available = int(self.videos_count.text())
        titles_available = int(self.titles_count.text())
        
        if total_videos > videos_available:
            self.validation_label.setText(
                f"⚠️ Necesitas {total_videos - videos_available} videos más"
            )
            self.validation_label.setStyleSheet("color: #ff9500;")
            self.apply_schedule_btn.setEnabled(False)
        elif total_videos > titles_available:
            self.validation_label.setText(
                f"⚠️ Necesitas {total_videos - titles_available} títulos más"
            )
            self.validation_label.setStyleSheet("color: #ff9500;")
            self.apply_schedule_btn.setEnabled(False)
        else:
            self.validation_label.setText(
                f"✅ Perfecto! Tienes suficientes videos y títulos"
            )
            self.validation_label.setStyleSheet("color: #43b680;")
            self.apply_schedule_btn.setEnabled(True)
    
    def _apply_smart_schedule(self):
        """Aplica la programación automática."""
        videos_per_day = self.videos_per_day_spin.value()
        days = self.days_spin.value()
        
        # Limpiar programación anterior
        self.calendar.clear_schedule()
        
        # Programar días consecutivos desde hoy
        current_date = QDate.currentDate()
        for i in range(days):
            date = current_date.addDays(i)
            self.calendar.set_videos_for_date(date, videos_per_day)
        
        self._update_all_counters()
    
    def _clear_schedule(self):
        """Limpia toda la programación."""
        self.calendar.clear_schedule()
        self._update_all_counters()
    
    def _on_cleanup_option_changed(self):
        """Asegura que solo una opción de limpieza esté activa."""
        sender = self.sender()
        if sender == self.delete_videos_btn and self.delete_videos_btn.isChecked():
            self.trash_videos_btn.setChecked(False)
        elif sender == self.trash_videos_btn and self.trash_videos_btn.isChecked():
            self.delete_videos_btn.setChecked(False)
    
    def _edit_description(self):
        """Abre el editor de descripción."""
        dialog = QDialog(self)
        dialog.setWindowTitle("✏️ Editar Descripción de Videos")
        dialog.setModal(True)
        dialog.setMinimumSize(700, 600)
        dialog.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dialog)
        margin = self.screen_adapter.get_margin(20)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(self.screen_adapter.get_spacing(14))
        
        title = QLabel("📝 Descripción que se usará para todos los videos:")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #24eaff;")
        layout.addWidget(title)
        
        text_edit = QTextEdit()
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1a2332;
                color: #f4f8ff;
                border: 2px solid #23304a;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
            }
        """)
        
        # Cargar descripción actual
        if os.path.isfile(DESCRIPTION_PATH):
            with open(DESCRIPTION_PATH, 'r', encoding='utf-8') as f:
                text_edit.setPlainText(f.read())
        
        layout.addWidget(text_edit)
        
        # Botones
        buttons = QHBoxLayout()
        buttons.setSpacing(12)
        
        cancel = QPushButton("Cancelar")
        cancel.setObjectName("cancelButton")
        cancel.clicked.connect(dialog.reject)
        buttons.addWidget(cancel)
        
        buttons.addStretch()
        
        save = QPushButton("💾 Guardar")
        save.clicked.connect(lambda: self._save_description(text_edit.toPlainText(), dialog))
        buttons.addWidget(save)
        
        layout.addLayout(buttons)
        dialog.exec()
    
    def _save_description(self, text, dialog):
        """Guarda la descripción."""
        os.makedirs(os.path.dirname(DESCRIPTION_PATH), exist_ok=True)
        with open(DESCRIPTION_PATH, 'w', encoding='utf-8') as f:
            f.write(text)
        self._update_all_counters()
        dialog.accept()
    
    def _save_and_close(self):
        """Guarda la configuración y cierra el diálogo."""
        # Guardar programación del calendario
        self.calendar.save_schedule()
        
        # Guardar configuración de upload
        status_map = {"Público": "publico", "Privado": "privado", "No listado": "no_listado"}
        config = {
            "subida": {
                "modo": "programado",
                "estado": status_map.get(self.status_combo.currentText(), "publico"),
                "autoborrado_videos": self.delete_videos_btn.isChecked(),
                "papelera_videos": self.trash_videos_btn.isChecked(),
                "contenido_niños": False,
                "videos_por_dia": self.videos_per_day_spin.value(),
                "dias_programados": self.days_spin.value()
            }
        }
        
        schema = {"subida": {}}
        config_manager = ConfigManager(UPLOAD_CONFIG_PATH, schema)
        config_manager.config = config
        config_manager.save()
        
        self.accept()


__all__ = ["UploadSettingsDialogV2"]
