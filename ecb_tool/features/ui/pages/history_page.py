"""
History Page.
Displays conversion and upload logs from CSV files.
"""
import csv
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QTabWidget, QPushButton, QHBoxLayout, QHeaderView
)
from ecb_tool.core.paths import get_paths

class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.paths = get_paths()
        self.init_ui()
        self.refresh_data()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Actions
        top_bar = QHBoxLayout()
        btn_refresh = QPushButton("🔄 Actualizar Historial")
        btn_refresh.clicked.connect(self.refresh_data)
        top_bar.addWidget(btn_refresh)
        top_bar.addStretch()
        layout.addLayout(top_bar)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Conversions
        self.table_conv = QTableWidget()
        self.table_conv.setColumnCount(6)
        self.table_conv.setHorizontalHeaderLabels(["Fecha", "Job ID", "Beat", "Cover", "Output", "Estado"])
        header = self.table_conv.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabs.addTab(self.table_conv, "🎬 Conversiones")
        
        # Tab 2: Uploads
        self.table_upload = QTableWidget()
        self.table_upload.setColumnCount(5)
        self.table_upload.setHorizontalHeaderLabels(["Fecha", "Video", "ID YouTube", "Título", "Estado"])
        header_up = self.table_upload.horizontalHeader()
        header_up.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabs.addTab(self.table_upload, "☁️ Subidas")
        
        layout.addWidget(self.tabs)
        
    def refresh_data(self):
        """Load data from CSVs."""
        self._load_csv(self.paths.conversion_state, self.table_conv)
        self._load_csv(self.paths.upload_state, self.table_upload)
        
    def _load_csv(self, path, table: QTableWidget):
        table.setRowCount(0)
        if not path.exists():
            return
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, None) # Skip header
                
                rows = list(reader)
                table.setRowCount(len(rows))
                
                for i, row in enumerate(rows):
                    # Filter relevant columns or show all? 
                    # Conversion CSV: time, id, beat, cover, output, status, error
                    # Upload CSV: time, id, video, videoid, title, status, error
                    
                    # Truncate row to match table columns count if necessary
                    display_row = row[:table.columnCount()]
                    
                    for j, val in enumerate(display_row):
                        item = QTableWidgetItem(str(val))
                        table.setItem(i, j, item)
        except Exception as e:
            print(f"Error loading history {path}: {e}")
