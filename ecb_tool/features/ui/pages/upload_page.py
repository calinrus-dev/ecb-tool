"""
Upload Page.
Handles video selection, metadata editing, translation, and YouTube upload.
"""
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QListWidget, QGroupBox, QFormLayout, QLineEdit, QTextEdit,
    QCheckBox, QMessageBox, QSplitter, QProgressBar
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap

from ecb_tool.core.paths import get_paths
from ecb_tool.features.upload.worker import UploadWorker
from ecb_tool.features.upload.models import UploadConfig, UploadJob
from ecb_tool.features.upload.uploader import YouTubeAuth
from ecb_tool.features.translation.service import get_translation_service

class UploadPage(QWidget):
    def __init__(self):
        super().__init__()
        self.paths = get_paths()
        self.worker = None
        self.translation_service = get_translation_service()
        self.auth = YouTubeAuth()
        self.init_ui()
        self.refresh_videos()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # --- Left Panel: Videos ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.addWidget(QLabel("📂 Videos Listos"))
        self.video_list = QListWidget()
        self.video_list.currentItemChanged.connect(self.on_video_selected)
        left_layout.addWidget(self.video_list)
        
        btn_refresh = QPushButton("🔄 Actualizar Lista")
        btn_refresh.clicked.connect(self.refresh_videos)
        left_layout.addWidget(btn_refresh)
        
        splitter.addWidget(left_panel)
        
        # --- Right Panel: Metadata & Actions ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # OAuth Status
        auth_group = QGroupBox("🔑 Cuenta YouTube")
        auth_layout = QHBoxLayout(auth_group)
        self.lbl_auth_status = QLabel("Estado: Desconocido")
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.clicked.connect(self.login)
        auth_layout.addWidget(self.lbl_auth_status)
        auth_layout.addWidget(self.btn_login)
        right_layout.addWidget(auth_group)
        
        # Metadata Form
        meta_group = QGroupBox("📝 Metadatos")
        form = QFormLayout(meta_group)
        
        self.inp_title = QLineEdit()
        form.addRow("Título:", self.inp_title)
        
        self.inp_desc = QTextEdit()
        self.inp_desc.setMaximumHeight(100)
        form.addRow("Descripción:", self.inp_desc)
        
        # Translation
        self.chk_translate = QCheckBox("Traducción Automática (Inglés/Español)")
        form.addRow("", self.chk_translate)
        
        right_layout.addWidget(meta_group)
        
        # Actions
        self.progress = QProgressBar()
        right_layout.addWidget(self.progress)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(100)
        right_layout.addWidget(self.log_output)
        
        self.btn_upload = QPushButton("☁️ Subir Seleccionados")
        self.btn_upload.setProperty("class", "primary")
        self.btn_upload.setMinimumHeight(50)
        self.btn_upload.clicked.connect(self.start_upload)
        right_layout.addWidget(self.btn_upload)
        
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        layout.addWidget(splitter)
        
        self.check_auth_status()

    def check_auth_status(self):
        """Check if we have valid credentials."""
        token_path = self.paths.oauth / 'token.pickle'
        if token_path.exists():
            self.lbl_auth_status.setText("Estado: ✅ Conectado")
            self.lbl_auth_status.setStyleSheet("color: #6CCB5F")
            self.btn_login.setText("Re-conectar")
        else:
            self.lbl_auth_status.setText("Estado: ❌ Desconectado")
            self.lbl_auth_status.setStyleSheet("color: #FF99A4")

    def login(self):
        """Trigger OAuth flow."""
        try:
            self.auth.authenticate()
            self.check_auth_status()
            QMessageBox.information(self, "Login", "Autenticación exitosa")
        except Exception as e:
            QMessageBox.critical(self, "Error Login", str(e))

    def refresh_videos(self):
        """Load videos from workspace."""
        self.video_list.clear()
        if self.paths.videos.exists():
            for f in self.paths.videos.iterdir():
                if f.suffix == '.mp4':
                    self.video_list.addItem(f.name)
        
    def on_video_selected(self, current, previous):
        if not current:
            return
        
        # Auto-fill title from filename
        filename = current.text()
        title = Path(filename).stem.replace('_', ' ').replace('video', '').strip()
        self.inp_title.setText(title.title())
        
    def start_upload(self):
        selected_items = self.video_list.selectedItems()
        if not selected_items:
            # If none selected, maybe select all? For now require selection
             # Or select current
             if self.video_list.currentItem():
                 selected_items = [self.video_list.currentItem()]
             else:
                 QMessageBox.warning(self, "Aviso", "Selecciona al menos un video")
                 return
                 
        # Create jobs
        jobs = []
        base_title = self.inp_title.text()
        description = self.inp_desc.toPlainText()
        
        for item in selected_items:
            video_file = self.paths.videos / item.text()
            
            # Translation Logic
            final_title = base_title
            final_desc = description
            
            if self.chk_translate.isChecked():
                # Append translated version
                # Example: "Title ES | Title EN"
                translated = self.translation_service.translate_metadata(
                    base_title, description, ['en']
                )
                en_data = translated.get('en', {})
                if en_data:
                    final_title = f"{base_title} | {en_data['title']}"
                    final_desc = f"{description}\n\n--- English ---\n{en_data['description']}"
            
            job = UploadJob(
                id=f"up-{item.text()}",
                video_file=video_file,
                title=final_title,
                description=final_desc,
                tags=["beat", "instrumental"],
                privacy_status="private" # Default to private for safety
            )
            jobs.append(job)
            
        # Config
        config = UploadConfig(
            videos_dir=self.paths.videos,
            privacy_status="private"
        )
        
        self.btn_upload.setEnabled(False)
        self.worker = UploadWorker(jobs, config)
        self.worker.log_signal.connect(self.log_output.append)
        self.worker.finished_signal.connect(self.on_upload_finished)
        self.worker.start()
        
    def on_upload_finished(self):
        self.log_output.append("🏁 Carga finalizada.")
        self.btn_upload.setEnabled(True)
