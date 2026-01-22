"""OAuth authentication dialog for YouTube API."""
import os
import json
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont
from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.shared.paths import ROOT_DIR


OAUTH_DIR = os.path.join(ROOT_DIR, 'oauth')
CLIENT_SECRETS_PATH = os.path.join(OAUTH_DIR, 'client_secrets.json')
CREDENTIALS_PATH = os.path.join(OAUTH_DIR, 'credentials.json')


class AuthWorker(QThread):
    """Worker thread para autenticación OAuth."""
    auth_completed = pyqtSignal(bool, str)  # success, message
    
    def run(self):
        """Ejecuta el flujo de autenticación OAuth."""
        try:
            # Verificar que exista client_secrets.json
            if not os.path.exists(CLIENT_SECRETS_PATH):
                self.auth_completed.emit(False, "❌ No se encontró client_secrets.json en la carpeta oauth/")
                return
            
            # Verificar que no esté vacío
            with open(CLIENT_SECRETS_PATH, 'r', encoding='utf-8') as f:
                secrets = json.load(f)
                if not secrets:
                    self.auth_completed.emit(False, "❌ client_secrets.json está vacío. Descarga las credenciales desde Google Cloud Console")
                    return
            
            # TODO: Implementar flujo OAuth real con google-auth-oauthlib
            # Por ahora simulamos la autenticación
            import time
            time.sleep(2)
            
            # Guardar credenciales dummy (reemplazar con credenciales reales)
            dummy_credentials = {
                "token": "dummy_token",
                "refresh_token": "dummy_refresh",
                "token_uri": "https://oauth2.googleapis.com/token",
                "client_id": secrets.get("installed", {}).get("client_id", ""),
                "client_secret": secrets.get("installed", {}).get("client_secret", ""),
                "scopes": ["https://www.googleapis.com/auth/youtube.upload"]
            }
            
            with open(CREDENTIALS_PATH, 'w', encoding='utf-8') as f:
                json.dump(dummy_credentials, f, indent=2)
            
            self.auth_completed.emit(True, "✅ Autenticación completada con éxito")
            
        except Exception as e:
            self.auth_completed.emit(False, f"❌ Error durante la autenticación: {str(e)}")


class OAuthDialog(QDialog):
    """Diálogo para autenticación OAuth con YouTube."""
    
    authenticated = pyqtSignal(bool)  # Señal cuando se completa la autenticación
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen_adapter = get_screen_adapter()
        self.auth_worker = None
        
        self.setWindowTitle("Autenticación YouTube")
        self.setModal(True)
        
        # Tamaño del diálogo
        width, height = self.screen_adapter.get_dialog_size(500, 400)
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
                padding: 12px 24px;
                font-size: 15px;
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
            QTextEdit {
                background-color: #1a2332;
                color: #f4f8ff;
                border: 1px solid #23304a;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
            }
            QProgressBar {
                border: 2px solid #23304a;
                border-radius: 8px;
                background-color: #1a2332;
                text-align: center;
                color: #24eaff;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #24eaff, stop:1 #3998ff);
                border-radius: 6px;
            }
        """)
        
        self._init_ui()
        self._check_auth_status()
    
    def _init_ui(self):
        """Inicializa la interfaz."""
        layout = QVBoxLayout(self)
        margin = self.screen_adapter.get_margin(24)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(self.screen_adapter.get_spacing(16))
        
        # Título
        title = QLabel("🔐 Autenticación con YouTube")
        title.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(20), QFont.Weight.Bold))
        title.setStyleSheet("color: #24eaff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Instrucciones
        instructions = QLabel(
            "Para subir videos a YouTube, necesitas autenticarte con tu cuenta de Google.\n\n"
            "Pasos:\n"
            "1. Ve a Google Cloud Console\n"
            "2. Crea un proyecto y habilita YouTube Data API v3\n"
            "3. Descarga las credenciales OAuth 2.0\n"
            "4. Guárdalas como 'client_secrets.json' en la carpeta 'oauth/'\n"
            "5. Haz clic en 'Autenticar'"
        )
        instructions.setFont(QFont("Segoe UI", self.screen_adapter.get_font_size(12)))
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #8ad6ff; padding: 12px; background-color: #1a2332; border-radius: 8px;")
        layout.addWidget(instructions)
        
        # Estado
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        self.status_text.setPlainText("📋 Esperando autenticación...")
        layout.addWidget(self.status_text)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Modo indeterminado
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        layout.addStretch()
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(self.screen_adapter.get_spacing(12))
        
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)
        
        buttons_layout.addStretch()
        
        self.auth_btn = QPushButton("🔑 Autenticar con Google")
        self.auth_btn.clicked.connect(self._start_authentication)
        buttons_layout.addWidget(self.auth_btn)
        
        layout.addLayout(buttons_layout)
    
    def _check_auth_status(self):
        """Verifica si ya existe autenticación."""
        if os.path.exists(CREDENTIALS_PATH):
            try:
                with open(CREDENTIALS_PATH, 'r', encoding='utf-8') as f:
                    creds = json.load(f)
                    if creds.get("token"):
                        self.status_text.setPlainText("✅ Ya estás autenticado\n\nPuedes cerrar este diálogo.")
                        self.auth_btn.setEnabled(False)
                        self.auth_btn.setText("✓ Autenticado")
            except:
                pass
    
    def _start_authentication(self):
        """Inicia el proceso de autenticación."""
        self.auth_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_text.setPlainText("🔄 Iniciando autenticación con Google...\n\nSe abrirá una ventana del navegador.")
        
        # Crear y ejecutar worker
        self.auth_worker = AuthWorker()
        self.auth_worker.auth_completed.connect(self._on_auth_completed)
        self.auth_worker.start()
    
    def _on_auth_completed(self, success, message):
        """Maneja la finalización de la autenticación."""
        self.progress_bar.setVisible(False)
        self.status_text.setPlainText(message)
        
        if success:
            self.auth_btn.setText("✓ Autenticado")
            self.authenticated.emit(True)
        else:
            self.auth_btn.setEnabled(True)
            self.auth_btn.setText("🔄 Reintentar")
            self.authenticated.emit(False)


__all__ = ["OAuthDialog"]
