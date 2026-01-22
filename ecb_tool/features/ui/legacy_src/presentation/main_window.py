from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QScrollArea
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeyEvent, QResizeEvent

from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.shared.theme_manager import get_theme_manager
from ecb_tool.core.shared.navigation import get_navigation_manager
from ecb_tool.features.ui.blocks.top_bar import TopBar
from ecb_tool.features.ui.screens.home_screen import HomeScreen
from ecb_tool.features.ui.screens.general_settings_screen import GeneralSettingsScreen
from ecb_tool.features.ui.screens.ffmpeg_settings_screen import FFmpegSettingsScreen
from ecb_tool.features.ui.screens.upload_settings_screen import UploadSettingsScreen

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.screen_adapter = get_screen_adapter()
        self.theme_manager = get_theme_manager()
        self.navigation = get_navigation_manager()
        self.is_fullscreen = False
        
        self.setWindowTitle("ECB TOOL")
        
        # Configurar ventana con constraints dinámicos
        self._apply_window_constraints()
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top bar
        self.top_bar = TopBar(
            self.open_advanced_settings, 
            self.open_upload_settings, 
            self.open_general_settings,
            self.toggle_fullscreen
        )
        main_layout.addWidget(self.top_bar)
        
        # Scroll area para el contenido con smooth scrolling
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Habilitar smooth scrolling
        scroll.setProperty("smoothScroll", True)
        scroll.verticalScrollBar().setSingleStep(20)
        scroll.horizontalScrollBar().setSingleStep(20)
        
        main_layout.addWidget(scroll)
        
        # Stack de pantallas
        self.screen_stack = QStackedWidget()
        scroll.setWidget(self.screen_stack)
        
        # Crear pantallas
        self.screens = {}
        self._create_screens()
        
        # Navegación inicial
        self.navigation.navigate("home")
        
        # Conectar señales de navegación
        self.navigation.navigate_to.connect(self._on_navigate)
        
        # Aplicar tema inicial
        self._apply_theme()
        self.theme_manager.theme_changed.connect(self._apply_theme)
        
        # Timer para detectar cambios de resolución
        self.resize_timer = QTimer()
        self.resize_timer.timeout.connect(self._on_resize_finished)
        self.resize_timer.setSingleShot(True)
    
    def _apply_window_constraints(self):
        """Aplica constraints de tamaño de ventana."""
        constraints = self.screen_adapter.get_window_constraints()
        self.setMinimumSize(constraints['min_width'], constraints['min_height'])
        self.setMaximumSize(constraints['max_width'], constraints['max_height'])
    
    def resizeEvent(self, event: QResizeEvent):
        """Manejar redimensionamiento de ventana."""
        super().resizeEvent(event)
        # Reiniciar timer - solo actualizaremos después de que termine el resize
        self.resize_timer.stop()
        self.resize_timer.start(300)  # 300ms de delay
    
    def _on_resize_finished(self):
        """Llamado cuando termina el redimensionamiento."""
        # Aquí podríamos recargar elementos si fuera necesario
        pass
    
    def toggle_fullscreen(self):
        """Alterna entre fullscreen y windowed."""
        # Obtener la ventana principal (QWidget top-level se comporta como ventana)
        if self.windowState() & Qt.WindowState.WindowFullScreen:
            self.setWindowState(self.windowState() & ~Qt.WindowState.WindowFullScreen)
            self.is_fullscreen = False
        else:
            self.setWindowState(self.windowState() | Qt.WindowState.WindowFullScreen)
            self.is_fullscreen = True
    
    def keyPressEvent(self, event: QKeyEvent):
        """Manejar teclas especiales."""
        if event.key() == Qt.Key.Key_Escape:
            current_screen = self.screen_stack.currentWidget()
            # Si estamos en fullscreen, salir de fullscreen
            if self.is_fullscreen:
                self.toggle_fullscreen()
                event.accept()
            # Si no estamos en home, volver atrás
            elif current_screen != self.screens.get('home'):
                self.navigation.back()
                event.accept()
            else:
                event.ignore()
        elif event.key() == Qt.Key.Key_F11:
            # F11 para toggle fullscreen
            self.toggle_fullscreen()
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def _create_screens(self):
        """Crea todas las pantallas."""
        # Pantalla principal
        self.screens['home'] = HomeScreen()
        self.screen_stack.addWidget(self.screens['home'])
        
        # Configuración general
        self.screens['general_settings'] = GeneralSettingsScreen()
        self.screen_stack.addWidget(self.screens['general_settings'])
        
        # Configuración FFMPEG
        self.screens['ffmpeg_settings'] = FFmpegSettingsScreen()
        self.screen_stack.addWidget(self.screens['ffmpeg_settings'])
        
        # Configuración Uploads
        self.screens['upload_settings'] = UploadSettingsScreen()
        self.screen_stack.addWidget(self.screens['upload_settings'])
    
    def _on_navigate(self, screen_name):
        """Navega a una pantalla."""
        if screen_name in self.screens:
            self.screen_stack.setCurrentWidget(self.screens[screen_name])
    
    def open_general_settings(self):
        """Abre configuración general."""
        self.navigation.navigate('general_settings')
    
    def open_advanced_settings(self):
        """Abre configuración de conversión."""
        self.navigation.navigate('ffmpeg_settings')
    
    def open_upload_settings(self):
        """Abre configuración de uploads."""
        self.navigation.navigate('upload_settings')
    
    def _apply_theme(self):
        """Aplica el tema actual."""
        stylesheet = self.theme_manager.get_stylesheet()
        self.setStyleSheet(stylesheet)
