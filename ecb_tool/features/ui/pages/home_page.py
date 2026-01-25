from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame, QGridLayout
from PyQt6.QtCore import Qt

from ecb_tool.features.ui.styles.theme import ThemeColors
from ecb_tool.features.ui.components.custom_widgets import StatCard, ModernButton, ModernFrame

class ActivityItem(ModernFrame):
    """Row item for recent activity."""
    def __init__(self, title, status, time, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        
        # Title
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"color: {ThemeColors.TextPrimary}; font-weight: 600;")
        
        # Status
        lbl_status = QLabel(status)
        color = ThemeColors.Success if status == "Completed" else ThemeColors.Info
        lbl_status.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: 600; background: {color}20; padding: 4px 8px; border-radius: 4px;")
        
        # Time
        lbl_time = QLabel(time)
        lbl_time.setStyleSheet(f"color: {ThemeColors.TextSecondary}; font-size: 12px;")
        
        layout.addWidget(lbl_title)
        layout.addStretch()
        layout.addWidget(lbl_status)
        layout.addWidget(lbl_time)

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Scroll Area for the whole page
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        content = QWidget()
        scroll.setWidget(content)
        
        # Main Layout
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Header
        header = QLabel("Dashboard")
        header.setStyleSheet(f"color: {ThemeColors.TextPrimary}; font-size: 32px; font-weight: 700;")
        layout.addWidget(header)
        
        # Stats Row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        stats_layout.addWidget(StatCard("Active Projects", "3"))
        stats_layout.addWidget(StatCard("Videos Scheduled", "12"))
        stats_layout.addWidget(StatCard("Beats Processed", "145"))
        stats_layout.addWidget(StatCard("Upload Errors", "0"))
        
        layout.addLayout(stats_layout)
        
        # Quick Actions
        actions_frame = ModernFrame(glass=True)
        actions_layout = QVBoxLayout(actions_frame)
        
        actions_label = QLabel("Quick Actions")
        actions_label.setStyleSheet(f"color: {ThemeColors.TextPrimary}; font-size: 18px; font-weight: 600; margin-bottom: 8px;")
        actions_layout.addWidget(actions_label)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        btn_layout.addWidget(ModernButton("New Project", "primary"))
        btn_layout.addWidget(ModernButton("Start Queue", "secondary"))
        btn_layout.addWidget(ModernButton("View Calendar", "secondary"))
        btn_layout.addStretch()
        
        actions_layout.addLayout(btn_layout)
        layout.addWidget(actions_frame)
        
        # Recent Activity
        activity_label = QLabel("Recent Activity")
        activity_label.setStyleSheet(f"color: {ThemeColors.TextPrimary}; font-size: 18px; font-weight: 600; margin-top: 16px;")
        layout.addWidget(activity_label)
        
        # Mock Data
        layout.addWidget(ActivityItem("Project: Future Beats", "Completed", "2 mins ago"))
        layout.addWidget(ActivityItem("Upload: Type Beat #4", "Uploading...", "Now"))
        layout.addWidget(ActivityItem("Conversion: Sad Vibes", "Pending", "In Queue"))
        
        layout.addStretch()
        
        # Set layout for main widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(scroll)
