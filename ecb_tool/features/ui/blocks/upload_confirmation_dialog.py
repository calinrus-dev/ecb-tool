"""Diálogo de confirmación de subida con resumen."""
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QCalendarWidget)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QTextCharFormat, QBrush, QColor
from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.shared.paths import ROOT_DIR


SCHEDULE_PATH = os.path.join(ROOT_DIR, 'config', 'programacion_subidas.json')


class UploadConfirmationDialog(QDialog):
    """Diálogo pequeño de confirmación antes de iniciar subida."""
    
    confirmed = pyqtSignal()
    modify_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen_adapter = get_screen_adapter()
        
        self.setWindowTitle("⚡ Confirmar Subida a YouTube")
        self.setModal(True)
        
        # Tamaño compacto
        width, height = self.screen_adapter.get_dialog_size(600, 700)
        self.setFixedSize(width, height)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #101722;
            }
            QLabel {
                color: #f4f8ff;
            }
            QPushButton {
                background-color: #3998ff;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
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
            QPushButton#confirmButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #43b680, stop:1 #3998ff);
                padding: 14px 24px;
                font-size: 15px;
            }
            QPushButton#confirmButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #52c690, stop:1 #4fa8ff);
            }
            QPushButton#modifyButton {
                background-color: #ff9500;
            }
            QPushButton#modifyButton:hover {
                background-color: #ffa620;
            }
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
            QCalendarWidget QMenu {
                background-color: #1a2332;
                color: #f4f8ff;
            }
            QCalendarWidget QSpinBox {
                background-color: #23304a;
                color: #f4f8ff;
                border: 1px solid #3998ff;
                border-radius: 4px;
            }
        """)
        
        self._init_ui()
        self._load_schedule()
    
    def _init_ui(self):
        """Inicializa la interfaz."""
        layout = QVBoxLayout(self)
        margin = self.screen_adapter.get_margin(20)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(self.screen_adapter.get_spacing(16))
        
        # Título
        title = QLabel("🚀 Resumen de Subida")
        title.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(20), QFont.Weight.Bold))
        title.setStyleSheet("color: #24eaff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Revisa la programación antes de iniciar la subida")
        subtitle.setStyleSheet("color: #8ad6ff; font-size: 12px; font-style: italic;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Separador
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setStyleSheet("background-color: #23304a;")
        layout.addWidget(sep1)
        
        # Estadísticas
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color: #1a2332; border-radius: 10px; padding: 16px;")
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setSpacing(12)
        
        self.total_videos_label = QLabel("📊 Total de videos: 0")
        self.total_videos_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.total_videos_label.setStyleSheet("color: #24eaff;")
        stats_layout.addWidget(self.total_videos_label)
        
        self.days_label = QLabel("📅 Días programados: 0")
        self.days_label.setFont(QFont("Segoe UI", 13))
        self.days_label.setStyleSheet("color: #43b680;")
        stats_layout.addWidget(self.days_label)
        
        self.per_day_label = QLabel("⏰ Promedio por día: 0")
        self.per_day_label.setFont(QFont("Segoe UI", 13))
        self.per_day_label.setStyleSheet("color: #8ad6ff;")
        stats_layout.addWidget(self.per_day_label)
        
        layout.addWidget(stats_frame)
        
        # Calendario compacto
        calendar_label = QLabel("📆 Vista de Calendario:")
        calendar_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        calendar_label.setStyleSheet("color: #24eaff;")
        layout.addWidget(calendar_label)
        
        info = QLabel("✨ Los días programados aparecen en verde")
        info.setStyleSheet("color: #8ad6ff; font-size: 11px; font-style: italic;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.setMinimumDate(QDate.currentDate())
        layout.addWidget(self.calendar)
        
        layout.addStretch()
        
        # Separador
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("background-color: #23304a;")
        layout.addWidget(sep2)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        # Cancelar
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setMinimumWidth(140)
        buttons_layout.addWidget(cancel_btn)
        
        buttons_layout.addStretch()
        
        # Modificar (vuelve a configuración)
        modify_btn = QPushButton("⚙️ Modificar")
        modify_btn.setObjectName("modifyButton")
        modify_btn.clicked.connect(self._on_modify)
        modify_btn.setMinimumWidth(140)
        buttons_layout.addWidget(modify_btn)
        
        # Confirmar
        confirm_btn = QPushButton("✅ Confirmar y Subir")
        confirm_btn.setObjectName("confirmButton")
        confirm_btn.clicked.connect(self._on_confirm)
        confirm_btn.setMinimumWidth(180)
        buttons_layout.addWidget(confirm_btn)
        
        layout.addLayout(buttons_layout)
    
    def _load_schedule(self):
        """Carga y muestra la programación."""
        if not os.path.exists(SCHEDULE_PATH):
            self.total_videos_label.setText("⚠️ No hay videos programados")
            self.days_label.setText("📅 Días programados: 0")
            self.per_day_label.setText("⏰ Promedio por día: 0")
            return
        
        try:
            with open(SCHEDULE_PATH, 'r', encoding='utf-8') as f:
                schedule = json.load(f)
            
            if not schedule:
                self.total_videos_label.setText("⚠️ No hay videos programados")
                return
            
            # Calcular estadísticas
            total_videos = sum(schedule.values())
            days_count = len(schedule)
            avg_per_day = total_videos / days_count if days_count > 0 else 0
            
            # Actualizar labels
            self.total_videos_label.setText(f"📊 Total de videos: {total_videos}")
            self.days_label.setText(f"📅 Días programados: {days_count}")
            self.per_day_label.setText(f"⏰ Promedio por día: {avg_per_day:.1f}")
            
            # Resaltar días en el calendario
            format_scheduled = QTextCharFormat()
            format_scheduled.setBackground(QBrush(QColor("#43b680")))
            format_scheduled.setForeground(QBrush(QColor("#fff")))
            format_scheduled.setFontWeight(QFont.Weight.Bold)
            
            for date_str, count in schedule.items():
                date = QDate.fromString(date_str, "yyyy-MM-dd")
                if date.isValid():
                    self.calendar.setDateTextFormat(date, format_scheduled)
        
        except Exception as e:
            print(f"Error loading schedule: {e}")
            self.total_videos_label.setText("❌ Error cargando programación")
    
    def _on_confirm(self):
        """Confirma y emite señal."""
        self.confirmed.emit()
        self.accept()
    
    def _on_modify(self):
        """Solicita modificación."""
        self.modify_requested.emit()
        self.reject()


__all__ = ["UploadConfirmationDialog"]
