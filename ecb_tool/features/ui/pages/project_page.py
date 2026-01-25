from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QScrollArea, QDialog, QMessageBox, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal

from ecb_tool.features.ui.styles.theme import ThemeColors
from ecb_tool.features.ui.components.custom_widgets import ModernButton, ModernInput, ModernFrame, StatCard
from ecb_tool.core.project_manager import project_manager

class NewProjectDialog(QDialog):
    """Dialog to create a new project."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Project")
        self.setFixedSize(400, 300)
        self.setStyleSheet(f"background-color: {ThemeColors.Background}; color: {ThemeColors.TextPrimary};")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        layout.addWidget(QLabel("Create New Workspace"))
        
        self.name_input = ModernInput("Project Name (e.g., 'Trap Beats 2026')")
        layout.addWidget(self.name_input)
        
        self.desc_input = ModernInput("Description (Optional)")
        layout.addWidget(self.desc_input)
        
        btn_box = QHBoxLayout()
        btn_cancel = ModernButton("Cancel", "ghost")
        btn_cancel.clicked.connect(self.reject)
        
        btn_create = ModernButton("Create Project", "primary")
        btn_create.clicked.connect(self.create)
        
        btn_box.addWidget(btn_cancel)
        btn_box.addWidget(btn_create)
        layout.addLayout(btn_box)
        
    def create(self):
        name = self.name_input.text()
        if not name:
            return
        
        try:
            project_manager.create_project(name, self.desc_input.text())
            self.accept()
        except Exception as e:
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText(str(e))
            msg.exec()

class ProjectCard(ModernFrame):
    """Card representing a single project."""
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        title = QLabel(data.get("name", "Untitled"))
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {ThemeColors.Primary};")
        
        date = QLabel(data.get("created_at", "")[:10])
        date.setStyleSheet(f"color: {ThemeColors.TextDisabled}; font-size: 12px;")
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(date)
        layout.addLayout(header)
        
        # Desc
        desc = QLabel(data.get("description", "No description"))
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {ThemeColors.TextSecondary};")
        layout.addWidget(desc)
        
        layout.addStretch()
        
        # Actions
        actions = QHBoxLayout()
        btn_open = ModernButton("Open", "secondary")
        btn_open.setFixedHeight(30)
        actions.addWidget(btn_open)
        actions.addStretch()
        layout.addLayout(actions)

class ProjectPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Projects")
        title.setStyleSheet(f"font-size: 32px; font-weight: 700; color: {ThemeColors.TextPrimary};")
        
        btn_new = ModernButton("+ New Project", "primary")
        btn_new.clicked.connect(self.open_new_dialog)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(btn_new)
        
        layout.addLayout(header_layout)
        
        # Project Grid
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        self.scroll.setWidget(self.grid_widget)
        layout.addWidget(self.scroll)
        
        self.load_projects()
        
    def open_new_dialog(self):
        dialog = NewProjectDialog(self)
        if dialog.exec():
            self.load_projects()
            
    def load_projects(self):
        # Clear existing
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
            
        projects = project_manager.list_projects()
        
        row, col = 0, 0
        for p in projects:
            card = ProjectCard(p)
            self.grid_layout.addWidget(card, row, col)
            col += 1
            if col > 2: # 3 columns
                col = 0
                row += 1
