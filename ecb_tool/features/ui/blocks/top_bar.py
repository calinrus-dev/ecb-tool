from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QMenu, QLineEdit, QPushButton
from PyQt6.QtGui import QFont, QDesktopServices, QAction, QCursor, QPainter, QColor
from PyQt6.QtCore import Qt, QEvent, QUrl, QSize
from ecb_tool.core.shared.screen_utils import get_screen_adapter
import os
import json
from ecb_tool.core.shared.paths import ROOT_DIR


def bar_label(text, bold=False):
	screen = get_screen_adapter()
	font_size = screen.get_font_size(15)
	padding = screen.get_spacing(14)
	label = QLabel(text)
	label.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold if bold else QFont.Weight.Normal))
	label.setStyleSheet(
		f"color: #fff; background: {'#161616' if bold else 'transparent'}; border-radius: 8px; padding: 4px {padding}px;"
	)
	label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
	label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
	return label


class SignInButton(QPushButton):
	"""Botón circular de Sign In."""
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.screen_adapter = get_screen_adapter()
		self.authenticated = False
		
		# Tamaño del círculo
		size = self.screen_adapter.scale(40)
		self.setFixedSize(size, size)
		
		self._update_style()
		self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		
		# Verificar estado de autenticación
		self._check_auth_status()
	
	def _check_auth_status(self):
		"""Verifica si el usuario está autenticado."""
		credentials_path = os.path.join(ROOT_DIR, 'oauth', 'credentials.json')
		if os.path.exists(credentials_path):
			try:
				with open(credentials_path, 'r', encoding='utf-8') as f:
					creds = json.load(f)
					if creds.get("token"):
						self.authenticated = True
						self._update_style()
			except:
				pass
	
	def set_authenticated(self, authenticated):
		"""Actualiza el estado de autenticación."""
		self.authenticated = authenticated
		self._update_style()
	
	def _update_style(self):
		"""Actualiza el estilo según el estado."""
		if self.authenticated:
			bg_color = "#43b680"  # Verde cuando está autenticado
			text = "✓"
			tooltip = "Autenticado con YouTube"
		else:
			bg_color = "#3998ff"  # Azul cuando no está autenticado
			text = "👤"
			tooltip = "Sign In con Google"
		
		self.setText(text)
		self.setToolTip(tooltip)
		self.setStyleSheet(f"""
			QPushButton {{
				background-color: {bg_color};
				color: #fff;
				border: 2px solid #fff;
				border-radius: {self.width() // 2}px;
				font-size: {self.screen_adapter.get_font_size(16)}px;
				font-weight: bold;
			}}
			QPushButton:hover {{
				background-color: {"#52c690" if self.authenticated else "#4fa8ff"};
				border: 2px solid #24eaff;
			}}
		""")


class TopBar(QWidget):
	def __init__(self, open_advanced_settings_callback=None, open_upload_settings_callback=None, open_general_settings_callback=None, toggle_fullscreen_callback=None):
		super().__init__()
		self.screen_adapter = get_screen_adapter()
		height = self.screen_adapter.scale(50)
		self.setFixedHeight(height)
		self.setStyleSheet("background-color: #070c13;")
		layout = QHBoxLayout(self)
		margin = self.screen_adapter.get_margin(12)
		layout.setContentsMargins(margin, int(margin*0.6), margin, int(margin*0.6))
		layout.setSpacing(0)

		self.menus = {
			"Management": ["Import", "Generate", "History", "Trash"],
			"View": ["Show Layout", "Console", "Toggle Fullscreen"],
			"Settings": [
				"General Settings", "Import Settings", "Generation Settings", 
				"Conversion Settings", "Upload Settings", "Advanced Settings"
			],
			"Credits": [
				("Instagram: @c4linrus", "https://www.instagram.com/c4linrus?igsh=aTFkcXpzOGJzaWE="),
				("YouTube: El Conde Beats", "https://youtube.com/@elcondebeats?si=42qBahGjfYk1oG3a"),
				("Email: contact@calinrus.com", "mailto:contact@calinrus.com"),
			]
		}
		self.labels = {}
		self.menu_widgets = {}
		self.open_advanced_settings_callback = open_advanced_settings_callback
		self.open_upload_settings_callback = open_upload_settings_callback
		self.open_general_settings_callback = open_general_settings_callback
		self.toggle_fullscreen_callback = toggle_fullscreen_callback

		for idx, (menu, options) in enumerate(self.menus.items()):
			label = bar_label(menu, bold=(menu == "Management"))
			label.installEventFilter(self)
			layout.addWidget(label)
			if idx < len(self.menus) - 1:
				layout.addSpacerItem(QSpacerItem(18, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
			self.labels[label] = menu

		layout.addStretch()

		self.search = QLineEdit()
		self.search.setPlaceholderText("Search")
		self.search.setFixedWidth(210)
		self.search.setStyleSheet(
			"background: #232c39; color: #f2f7ff; border: none; border-radius: 15px; "
			"font-size: 15px; padding: 7px 18px;"
		)
		layout.addWidget(self.search, alignment=Qt.AlignmentFlag.AlignVCenter)
		
		# Botón Sign In
		self.sign_in_btn = SignInButton(self)
		self.sign_in_btn.clicked.connect(self._open_oauth_dialog)
		layout.addSpacerItem(QSpacerItem(12, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
		layout.addWidget(self.sign_in_btn, alignment=Qt.AlignmentFlag.AlignVCenter)

		self._init_menus()

	def _init_menus(self):
		for label, menu in self.labels.items():
			options = self.menus[menu]
			menu_widget = QMenu(self)
			menu_widget.setStyleSheet(
				"QMenu { background-color: #151d30; border: 1px solid #283654; border-radius: 9px; padding: 7px 0px; }"
				"QMenu::item { color: #eaf2ff; padding: 7px 30px 7px 18px; font-size: 15px; }"
				"QMenu::item:selected { background: #223a61; color: #71beff; }"
			)
			if menu != "Credits":
				for option in options:
					if isinstance(option, tuple):
						text, url = option
						action = QAction(text, self)
						action.triggered.connect(lambda checked=False, link=url: QDesktopServices.openUrl(QUrl(link)))
					else:
						action = QAction(option, self)
					if option == "General Settings" and self.open_general_settings_callback:
						action.triggered.connect(self.open_general_settings_callback)
					elif option == "Advanced Settings" and self.open_advanced_settings_callback:
						action.triggered.connect(self.open_advanced_settings_callback)
					elif option == "Conversion Settings":
						# Open conversion settings dialog
						action.triggered.connect(self._open_conversion_settings)
					elif option == "Upload Settings":
						# Open upload settings dialog V2
						action.triggered.connect(self._open_upload_settings)
					elif option == "Toggle Fullscreen" and self.toggle_fullscreen_callback:
						action.triggered.connect(self.toggle_fullscreen_callback)
					menu_widget.addAction(action)
			else:
				for option, url in options:
					action = QAction(option, self)
					action.triggered.connect(lambda checked=False, u=url: QDesktopServices.openUrl(QUrl(u)))
					menu_widget.addAction(action)
			self.menu_widgets[label] = menu_widget
	
	def _open_conversion_settings(self):
		"""Open conversion settings dialog."""
		from ecb_tool.features.ui.blocks.ffmpeg_settings_dialog import FFmpegSettingsDialog
		dialog = FFmpegSettingsDialog(self)
		dialog.exec()
	
	def _open_upload_settings(self):
		"""Abre el nuevo diálogo de configuración de uploads."""
		from ecb_tool.features.ui.blocks.upload_settings_dialog_v2 import UploadSettingsDialogV2
		dialog = UploadSettingsDialogV2(self)
		dialog.exec()
	
	def _open_oauth_dialog(self):
		"""Abre el diálogo de autenticación OAuth."""
		from ecb_tool.features.ui.blocks.oauth_dialog import OAuthDialog
		dialog = OAuthDialog(self)
		dialog.authenticated.connect(self.sign_in_btn.set_authenticated)
		dialog.exec()

	def eventFilter(self, obj, event):
		if not hasattr(self, "menu_widgets"):
			return super().eventFilter(obj, event)
		if obj in self.menu_widgets:
			if event.type() == QEvent.Type.Enter:
				self.menu_widgets[obj].popup(obj.mapToGlobal(obj.rect().bottomLeft()))
		return super().eventFilter(obj, event)


__all__ = ["TopBar"]
