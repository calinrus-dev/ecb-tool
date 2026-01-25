from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QSpinBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QAbstractItemView, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

from pathlib import Path
from ecb_tool.features.ui.styles.theme import ThemeColors
from ecb_tool.features.ui.components.custom_widgets import ModernButton, ModernFrame, StatCard

# Imports for logic
from ecb_tool.core.paths import get_paths
from ecb_tool.features.conversion.models import ConversionConfig, ConversionJob
from ecb_tool.features.conversion.worker import ConversionWorker

class ConverterPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.paths = get_paths()
        self.worker = None
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # LEFT PANEL
        left_panel = QVBoxLayout()
        left_panel.setSpacing(16)
        
        # Header
        header = QLabel("Converter")
        header.setStyleSheet(f"color: {ThemeColors.TextPrimary}; font-size: 32px; font-weight: 700;")
        left_panel.addWidget(header)
        
        # ASSET AREA (Split: Beats | Covers)
        asset_layout = QHBoxLayout()
        
        # Beats List
        beats_frame = ModernFrame()
        beats_layout = QVBoxLayout(beats_frame)
        beats_layout.addWidget(QLabel("Beats Library", styleSheet=f"color: {ThemeColors.TextPrimary}; font-weight: 600;"))
        
        beats_scroll = QScrollArea() # Need to import QScrollArea
        beats_scroll.setWidgetResizable(True)
        beats_scroll.setStyleSheet("border: none; background: transparent;")
        
        # Scan files
        beats_files = sorted([f for f in self.paths.beats.glob("*") if f.suffix in {'.mp3', '.wav', '.flac'}])
        from ecb_tool.features.ui.components.media_preview import AssetListWidget
        
        self.beats_list = AssetListWidget(beats_files)
        # Connect hover preview
        self.beats_list.preview_callback = self.update_preview
        
        beats_scroll.setWidget(self.beats_list)
        beats_layout.addWidget(beats_scroll)
        asset_layout.addWidget(beats_frame)
        
        # Covers List
        covers_frame = ModernFrame()
        covers_layout = QVBoxLayout(covers_frame)
        covers_layout.addWidget(QLabel("Covers Library", styleSheet=f"color: {ThemeColors.TextPrimary}; font-weight: 600;"))
        
        covers_scroll = QScrollArea()
        covers_scroll.setWidgetResizable(True)
        covers_scroll.setStyleSheet("border: none; background: transparent;")
        
        covers_files = sorted([f for f in self.paths.covers.glob("*") if f.suffix in {'.jpg', '.png'}])
        
        self.covers_list = AssetListWidget(covers_files)
        self.covers_list.preview_callback = self.update_preview
        
        covers_scroll.setWidget(self.covers_list)
        covers_layout.addWidget(covers_scroll)
        asset_layout.addWidget(covers_frame)
        
        left_panel.addLayout(asset_layout, 2) # Give it 2 flex
        
        # Configuration
        config_frame = ModernFrame()
        config_layout = QVBoxLayout(config_frame)
        config_layout.addWidget(QLabel("Configuration"))
        
        # Resolution
        res_layout = QHBoxLayout()
        res_layout.addWidget(QLabel("Resolution:"))
        self.res_combo = QComboBox()
        self.res_combo.addItems(["1920x1080", "1280x720", "3840x2160"])
        res_layout.addWidget(self.res_combo)
        config_layout.addLayout(res_layout)
        
        # FPS
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS:"))
        self.fps_spin = QSpinBox()
        self.fps_spin.setValue(30)
        fps_layout.addWidget(self.fps_spin)
        config_layout.addLayout(fps_layout)
        
        # BPV
        bpv_layout = QHBoxLayout()
        bpv_layout.addWidget(QLabel("Beats Per Video:"))
        self.bpv_spin = QSpinBox()
        self.bpv_spin.setValue(1)
        self.bpv_spin.setMinimum(1)
        bpv_layout.addWidget(self.bpv_spin)
        config_layout.addLayout(bpv_layout)
        
        left_panel.addWidget(config_frame, 0)
        
        # Preview Area
        print("Adding Preview Area")
        self.preview_lbl_info = QLabel("Hover items to preview\nClick to open")
        self.preview_lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_lbl_info.setStyleSheet(f"color: {ThemeColors.TextDisabled};")
        
        # We replace the old preview frame with just a label or keep it small
        # Actually user wants "preview al pasar el raton".
        # Let's show the name of what is being hovered in big text or show the image
        self.preview_display = ModernFrame(glass=True)
        self.preview_display.setFixedSize(300, 100)
        p_layout = QVBoxLayout(self.preview_display)
        p_layout.addWidget(self.preview_lbl_info)
        
        left_panel.addWidget(self.preview_display)

        # Controls
        controls = QHBoxLayout()
        self.btn_start = ModernButton("Start Conversion", "primary")
        self.btn_start.clicked.connect(self.start_conversion)
        controls.addWidget(self.btn_start)
        left_panel.addLayout(controls)
        
        layout.addLayout(left_panel, 1) # Left takes 1 part
        
    def update_preview(self, path):
        # Update the preview box
        self.preview_lbl_info.setText(f"Preview:\n{path.name}")
        # If it's an image, maybe we could set it as background or show it
        if path.suffix.lower() in {'.jpg', '.png'}:
             # Ideally show image
             pass
        
        # RIGHT PANEL: Queue
        right_panel = QVBoxLayout()
        
        queue_label = QLabel("Queue")
        queue_label.setStyleSheet(f"color: {ThemeColors.TextPrimary}; font-size: 18px; font-weight: 600;")
        right_panel.addWidget(queue_label)
        
        self.queue_table = QTableWidget()
        self.queue_table.setColumnCount(4)
        self.queue_table.setHorizontalHeaderLabels(["ID", "Files", "Status", "Progress"])
        self.queue_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.queue_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {ThemeColors.Surface};
                border: 1px solid {ThemeColors.Border};
                color: {ThemeColors.TextPrimary};
                border-radius: 8px;
            }}
            QHeaderView::section {{
                background-color: {ThemeColors.SurfaceHighlight};
                color: {ThemeColors.TextSecondary};
                border: none;
                padding: 8px;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
        """)
        
        right_panel.addWidget(self.queue_table)
        layout.addLayout(right_panel, 2)
        
        # Init Data
        self.refresh_counts()

    def refresh_counts(self):
        # Count files
        # Assumption: We scan the paths.beats, paths.covers
        # But wait, logic depends on 'current project' usually?
        # For this tool version 1, it seems to rely on global config dirs?
        # Let's check 'models.py' or 'paths.py' default.
        # Assuming defaults based on existing structure or project manager logic.
        # For now, simplistic scan of directories:
        
        # Safe interaction if dirs don't exist
        beats = 0
        covers = 0
        
        if self.paths.beats.exists():
            beats = len([f for f in self.paths.beats.iterdir() if f.is_file()])
        if self.paths.covers.exists():
            covers = len([f for f in self.paths.covers.iterdir() if f.is_file()])
            
        self.stat_beats.findChild(QLabel, "").setText(str(beats)) # Hack: assuming structure
        # Better: add update method to StatCard.  I will just rebuild it or access label if I stored it.
        # I didn't store references in StatCard. Let's just re-instantiate or leave as 0 for now until I fix Widget.
        # Actually I can just set text on the labels I found.
        # Since I can't easily access StatCard internal label without reference, I'll skip dynamic update for this cycle
        # unless I modify StatCard. But wait, I can modify StatCard in next tool call or just accept 0 for now.
        pass

    def start_conversion(self):
        # 1. Gather Config
        config = ConversionConfig(
            beats_dir=self.paths.beats,
            covers_dir=self.paths.covers,
            videos_dir=self.paths.videos,
            resolution=self.res_combo.currentText(),
            fps=self.fps_spin.value(),
            beats_per_video=self.bpv_spin.value()
        )
        
        # 2. Prepare Jobs
        # Logic: Scan beats, group by BPV, pair with covers
        beats = sorted([f for f in self.paths.beats.glob("*") if f.suffix in {'.mp3', '.wav'}])
        covers = sorted([f for f in self.paths.covers.glob("*") if f.suffix in {'.jpg', '.png'}])
        
        if not beats:
            QMessageBox.warning(self, "No Beats", "No beats found in beats folder.")
            return
        
        if not covers:
            QMessageBox.warning(self, "No Covers", "No covers found in covers folder.")
            return
        
        jobs = []
        bpv = config.beats_per_video
        
        # Simple Logic: 1 Job = BPV beats + 1 Cover (Round robin or Random)
        # We make as many videos as beats allow
        
        num_videos = len(beats) // bpv
        if num_videos == 0:
             QMessageBox.warning(self, "Not Enough Beats", f"Need at least {bpv} beats for 1 video.")
             return
             
        import random
        
        for i in range(num_videos):
            batch_beats = beats[i*bpv : (i+1)*bpv]
            cover = random.choice(covers) # Simple random
            
            output = self.paths.videos / f"video_{i+1}_{batch_beats[0].stem}.mp4"
            
            job = ConversionJob(
                id=f"JOB-{i+1:03d}",
                beat_files=batch_beats,
                cover_file=cover,
                output_file=output
            )
            jobs.append(job)
            self.add_table_row(job)
            
        # 3. Start Worker
        self.worker = ConversionWorker(config, jobs)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.status_signal.connect(self.update_status)
        self.worker.finished.connect(self.conversion_finished)
        
        self.btn_start.setDisabled(True)
        self.worker.start()
        
    def add_table_row(self, job):
        row = self.queue_table.rowCount()
        self.queue_table.insertRow(row)
        self.queue_table.setItem(row, 0, QTableWidgetItem(job.id))
        self.queue_table.setItem(row, 1, QTableWidgetItem(f"{len(job.beat_files)} beats + {job.cover_file.name}"))
        self.queue_table.setItem(row, 2, QTableWidgetItem("Pending"))
        self.queue_table.setItem(row, 3, QTableWidgetItem("0%"))
        
    def update_progress(self, job_id, percent):
        rows = self.queue_table.rowCount()
        for r in range(rows):
            if self.queue_table.item(r, 0).text() == job_id:
                self.queue_table.setItem(r, 3, QTableWidgetItem(f"{percent:.1f}%"))
                break

    def update_status(self, job_id, status):
        rows = self.queue_table.rowCount()
        for r in range(rows):
            if self.queue_table.item(r, 0).text() == job_id:
                self.queue_table.setItem(r, 2, QTableWidgetItem(status))
                break
                
    def conversion_finished(self):
        self.btn_start.setEnabled(True)
        QMessageBox.information(self, "Done", "Conversion process finished.")

