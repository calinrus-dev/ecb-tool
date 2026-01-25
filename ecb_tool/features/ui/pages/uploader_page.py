from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QCalendarWidget, QListView, QAbstractItemView, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QPainter, QTextCharFormat, QFont

from ecb_tool.features.ui.styles.theme import ThemeColors
from ecb_tool.features.ui.components.custom_widgets import ModernButton, ModernFrame, StatCard, ModernInput
from ecb_tool.core.scheduler_logic import SchedulerLogic

class CustomCalendar(QCalendarWidget):
    """Calendar with custom painting for dots."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGridVisible(False)
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.setStyleSheet(f"""
            QCalendarWidget QWidget {{ 
                background-color: {ThemeColors.Surface}; 
                color: {ThemeColors.TextPrimary};
            }}
            QCalendarWidget QToolButton {{
                color: {ThemeColors.TextPrimary};
                background-color: transparent;
                margin: 4px;
            }}
            QCalendarWidget QMenu {{
                background-color: {ThemeColors.SurfaceHighlight};
                color: {ThemeColors.TextPrimary};
            }}
            QCalendarWidget QSpinBox {{
                color: {ThemeColors.TextPrimary};
                background-color: {ThemeColors.SurfaceHighlight};
            }}
        """)
        
        # Data: Date -> Count
        self.schedule_data = {}

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        
        if date in self.schedule_data:
            count = self.schedule_data[date]
            
            # Determine Color
            color = QColor(ThemeColors.Success)
            
            # Draw Circle
            painter.save()
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            
            # Circle Size
            size = min(rect.width(), rect.height()) - 10
            # Center
            x = rect.x() + (rect.width() - size) / 2
            y = rect.y() + (rect.height() - size) / 2
            
            painter.drawEllipse(int(x), int(y), int(size), int(size))
            
            # Draw Number
            painter.setPen(QColor("#FFFFFF"))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(count))
            
            painter.restore()
            
    def set_data(self, date, count):
        self.schedule_data[date] = count
        self.updateCell(date)

class UploaderPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Left: Calendar & Stats
        left_panel = QVBoxLayout()
        
        header = QLabel("Uploader & Scheduler")
        header.setStyleSheet(f"color: {ThemeColors.TextPrimary}; font-size: 32px; font-weight: 700;")
        left_panel.addWidget(header)
        
        # Stats
        stats = QHBoxLayout()
        stats.addWidget(StatCard("Videos Ready", "0"))
        stats.addWidget(StatCard("Scheduled", "0"))
        left_panel.addLayout(stats)
        
        # Calendar
        self.calendar = CustomCalendar()
        self.calendar.clicked.connect(self.date_selected)
        left_panel.addWidget(self.calendar)
        
        # Distribution Logic UI
        dist_frame = ModernFrame()
        dist_layout = QVBoxLayout(dist_frame)
        dist_layout.addWidget(QLabel("Daily Scheduler"))
        
        self.lbl_selected_date = QLabel("Selected: Today")
        self.lbl_selected_date.setStyleSheet(f"color: {ThemeColors.Primary}; font-weight: 600;")
        dist_layout.addWidget(self.lbl_selected_date)
        
        input_layout = QHBoxLayout()
        self.input_videos = ModernInput("Num Videos (e.g. 2)")
        self.input_videos.setText("1")
        self.input_videos.textChanged.connect(self.calculate_slots)
        input_layout.addWidget(self.input_videos)
        
        btn_apply = ModernButton("Apply Schedule", "primary")
        btn_apply.clicked.connect(self.apply_schedule)
        input_layout.addWidget(btn_apply)
        
        dist_layout.addLayout(input_layout)
        
        self.lbl_slots = QLabel("Slots: -")
        self.lbl_slots.setStyleSheet(f"color: {ThemeColors.TextSecondary}; font-size: 12px;")
        dist_layout.addWidget(self.lbl_slots)
        
        left_panel.addWidget(dist_frame)
        layout.addLayout(left_panel, 1)
        
        # Right: Video List & Edit
        right_panel = QVBoxLayout()
        
        # Quick Edit
        edit_frame = ModernFrame()
        edit_layout = QVBoxLayout(edit_frame)
        edit_layout.addWidget(QLabel("Quick Edit Description"))
        
        # Title of video being edited
        self.lbl_edit_title = QLabel("Select a video from list to edit")
        self.lbl_edit_title.setStyleSheet(f"color: {ThemeColors.TextSecondary}; font-size: 12px;")
        edit_layout.addWidget(self.lbl_edit_title)
        
        self.txt_desc = QTextEdit()
        self.txt_desc.setPlaceholderText("Enter description here...")
        self.txt_desc.setStyleSheet(f"background: {ThemeColors.Surface}; border: 1px solid {ThemeColors.Border}; color: {ThemeColors.TextPrimary}; border-radius: 8px;")
        edit_layout.addWidget(self.txt_desc)
        
        btn_translate = ModernButton("Translate to English", "secondary")
        btn_translate.clicked.connect(self.translate_desc)
        edit_layout.addWidget(btn_translate)
        
        btn_save = ModernButton("Save Changes", "secondary")
        edit_layout.addWidget(btn_save)
        
        right_panel.addWidget(edit_frame)
        
        # List of scheduled
        lbl_list = QLabel("Scheduled Jobs")
        right_panel.addWidget(lbl_list)
        
        self.list_view = QListView()
        # Mock model would go here
        self.list_view.setStyleSheet(f"background: {ThemeColors.Surface}; border: 1px solid {ThemeColors.Border}; color: {ThemeColors.TextPrimary};")
        right_panel.addWidget(self.list_view)
        
        layout.addLayout(right_panel, 1) 
        
    def date_selected(self, date):
        self.lbl_selected_date.setText(f"Selected: {date.toString('yyyy-MM-dd')}")
        
    def calculate_slots(self):
        try:
            num = int(self.input_videos.text())
            slots = SchedulerLogic.calculate_slots(num)
            self.lbl_slots.setText(f"Slots: {', '.join(slots)}")
        except:
            self.lbl_slots.setText("Slots: -")

    def apply_schedule(self):
        try:
            num = int(self.input_videos.text())
            date = self.calendar.selectedDate()
            # Update Calendar Visual
            self.calendar.set_data(date, num)
            QMessageBox.information(self, "Scheduled", f"Scheduled {num} videos for {date.toString('dd/MM')}")
        except ValueError:
             QMessageBox.warning(self, "Error", "Invalid number.")

    def translate_desc(self):
        from ecb_tool.features.translation.service import get_translation_service
        text = self.txt_desc.toPlainText()
        if not text:
            return
            
        try:
            service = get_translation_service()
            # Translate to English by default or toggle
            translated = service.translate(text, dest_lang='en')
            self.txt_desc.setText(translated)
        except Exception as e:
            QMessageBox.warning(self, "Translation Error", str(e))
