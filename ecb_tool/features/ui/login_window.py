from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap

from ecb_tool.features.ui.styles.theme import ThemeColors
from ecb_tool.features.ui.components.custom_widgets import ModernButton, ModernInput, ModernFrame

class LoginWindow(QWidget):
    """Modern Login Screen."""
    login_successful = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ECB Tool - Login")
        self.resize(400, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Main Card
        card = ModernFrame(parent=self, glass=False)
        card.setFixedSize(360, 450)
        card.setStyleSheet(f"""
            ModernFrame {{
                background-color: {ThemeColors.Surface};
                border: 1px solid {ThemeColors.Border};
                border-radius: 16px;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 48, 32, 48)
        card_layout.setSpacing(16)
        
        # Logo
        title = QLabel("Welcome Back")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {ThemeColors.TextPrimary}; font-size: 24px; font-weight: 700; margin-bottom: 8px;")
        card_layout.addWidget(title)
        
        subtitle = QLabel("Sign in to continue to ECB Tool")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {ThemeColors.TextSecondary}; font-size: 14px; margin-bottom: 24px;")
        card_layout.addWidget(subtitle)
        
        # Inputs (Mock for now, as OAuth is usually a browser flow, but we add this for visual completeness)
        self.email = ModernInput("Email Address")
        card_layout.addWidget(self.email)
        
        self.password = ModernInput("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.password)
        
        # Button
        btn_login = ModernButton("Sign In", "primary")
        btn_login.clicked.connect(self.handle_login)
        card_layout.addWidget(btn_login)
        
        # Google OAuth Button
        btn_google = ModernButton("Continue with Google", "secondary")
        # btn_google.setIcon(...) # TODO ADD ICON
        btn_google.clicked.connect(self.handle_login)
        card_layout.addWidget(btn_google)

        card_layout.addStretch()

        # Footer
        footer = QLabel("Protected by reCAPTCHA")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet(f"color: {ThemeColors.TextDisabled}; font-size: 10px;")
        card_layout.addWidget(footer)
        
        layout.addWidget(card)
        
    def handle_login(self):
        # Mock login success
        self.login_successful.emit()
        self.close()
