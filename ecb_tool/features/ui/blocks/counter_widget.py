import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt
from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.shared.paths import ROOT_DIR

SVG_DIR = os.path.join(ROOT_DIR, 'ui', 'pieces', 'svg')


class ClickableSvg(QSvgWidget):
	def __init__(self, svg_path, width, height, on_click=None):
		super().__init__()
		self.setFixedSize(width, height)
		self.on_click = on_click
		self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		if svg_path and os.path.isfile(svg_path):
			self.load(svg_path)

	def mousePressEvent(self, event):
		if self.on_click:
			self.on_click()


class CounterWidget(QWidget):
	def __init__(self, label, path_to_open=None):
		super().__init__()
		self.screen_adapter = get_screen_adapter()
		self.label = label
		self.path = path_to_open
		self._last_value = None  # Cache para evitar actualizaciones innecesarias
		self._init_ui()
		self.refresh()

	def _init_ui(self):
		self.setStyleSheet("""
			QWidget {
				background: #141c2c;
				border-radius: 14px;
				padding: 0px;
			}
			QWidget:hover {
				background: #1a2332;
				border: 1px solid #24eaff40;
			}
		""")
		layout = QVBoxLayout(self)
		margin = self.screen_adapter.get_margin(20)
		spacing = self.screen_adapter.get_spacing(10)
		layout.setContentsMargins(margin, margin, margin, margin)
		layout.setSpacing(spacing)

		row1 = QHBoxLayout()
		row1.setSpacing(spacing)

		icon_name = "carpeta.svg"
		if self.label.lower() in ["titles", "desc.", "description"]:
			icon_name = "archivo.svg"

		icon_size = self.screen_adapter.scale(32)
		self.folder_icon = ClickableSvg(os.path.join(SVG_DIR, icon_name), icon_size, icon_size, self.open_path)
		row1.addWidget(self.folder_icon, alignment=Qt.AlignmentFlag.AlignVCenter)

		self.label_text = QLabel(self.label)
		font_size = self.screen_adapter.get_font_size(18)
		self.label_text.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
		self.label_text.setStyleSheet("color: #f4f8ff;")
		self.label_text.setAlignment(Qt.AlignmentFlag.AlignVCenter)
		row1.addWidget(self.label_text, alignment=Qt.AlignmentFlag.AlignVCenter)

		row1.addStretch()
		layout.addLayout(row1)

		row2 = QHBoxLayout()
		row2.setSpacing(spacing)

		trash_size = self.screen_adapter.scale(24)
		self.trash_icon = ClickableSvg(os.path.join(SVG_DIR, "papelera.svg"), trash_size, trash_size, self.clear)
		row2.addWidget(self.trash_icon, alignment=Qt.AlignmentFlag.AlignVCenter)

		self.value_label = QLabel("0")
		value_font = self.screen_adapter.get_font_size(16)
		self.value_label.setFont(QFont("Segoe UI", value_font, QFont.Weight.Bold))
		self.value_label.setStyleSheet("color: #f4f8ff;")
		self.value_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
		row2.addWidget(self.value_label, alignment=Qt.AlignmentFlag.AlignVCenter)

		self.check_icon = None
		if self.label.lower() in ["desc.", "description"]:
			self.check_icon = ClickableSvg(os.path.join(SVG_DIR, "x.svg"), trash_size, trash_size)
			row2.addWidget(self.check_icon, alignment=Qt.AlignmentFlag.AlignVCenter)
			self.value_label.hide()

		row2.addStretch()
		layout.addLayout(row2)

	def open_path(self):
		if not self.path or not os.path.exists(self.path):
			return
		os.startfile(self.path)

	def clear(self):
		if self.path:
			if os.path.isdir(self.path):
				import shutil
				for name in os.listdir(self.path):
					full = os.path.join(self.path, name)
					try:
						if os.path.isfile(full):
							os.remove(full)
						elif os.path.isdir(full):
							shutil.rmtree(full)
					except Exception:
						pass
			elif os.path.isfile(self.path):
				with open(self.path, "w", encoding="utf-8") as f:
					f.write("")
		self.refresh()

	def refresh(self):
		if not self.path or not os.path.exists(self.path):
			new_value = ("0", "x")
			if self._last_value == new_value:
				return  # No cambiar si ya está igual
			self._last_value = new_value
			
			self.value_label.setText("0")
			if self.check_icon:
				path = os.path.join(SVG_DIR, "x.svg")
				if os.path.isfile(path):
					self.check_icon.load(path)
				self.check_icon.show()
				self.value_label.hide()
			return

		if os.path.isdir(self.path):
			try:
				files = [f for f in os.listdir(self.path) if not f.startswith('.')]
				count = len(files)
				new_value = (str(count), None)
				
				if self._last_value == new_value:
					return  # No cambiar si ya está igual
				self._last_value = new_value
				
				self.value_label.setText(str(count))
				if self.check_icon:
					self.check_icon.hide()
					self.value_label.show()
			except Exception:
				self.value_label.setText("0")
		else:
			try:
				with open(self.path, "r", encoding="utf-8") as f:
					lines = f.readlines()
				if self.label.lower() == "titles":
					count = len(lines)
					new_value = (str(count), None)
					
					if self._last_value == new_value:
						return
					self._last_value = new_value
					
					self.value_label.setText(str(count))
					if self.check_icon:
						self.check_icon.hide()
						self.value_label.show()
				elif self.label.lower() in ["desc.", "description"]:
					has_text = any(line.strip() for line in lines)
					icon = "check.svg" if has_text else "x.svg"
					new_value = (None, icon)
					
					if self._last_value == new_value:
						return
					self._last_value = new_value
					
					if self.check_icon:
						path = os.path.join(SVG_DIR, icon)
						if os.path.isfile(path):
							self.check_icon.load(path)
						self.check_icon.show()
					self.value_label.hide()
				else:
					new_value = ("-", None)
					if self._last_value == new_value:
						return
					self._last_value = new_value
					
					self.value_label.setText("-")
					if self.check_icon:
						self.check_icon.hide()
						self.value_label.show()
			except Exception:
				new_value = ("0", "x")
				if self._last_value == new_value:
					return
				self._last_value = new_value
				
				self.value_label.setText("0")
				if self.check_icon:
					path = os.path.join(SVG_DIR, "x.svg")
					if os.path.isfile(path):
						self.check_icon.load(path)
					self.check_icon.show()
					self.value_label.hide()


__all__ = ["CounterWidget"]
