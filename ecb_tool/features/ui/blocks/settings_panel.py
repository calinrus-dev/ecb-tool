from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from ecb_tool.features.ui.pieces.text import body_text
from ecb_tool.features.ui.pieces.actions import ToggleSwitch


class DropdownField(QWidget):
	def __init__(self, label: str, options: list, max_rows: int = 5):
		super().__init__()
		self.setStyleSheet("background-color: transparent;")
		layout = QVBoxLayout(self)

		self.label = body_text(label, color="#ffffff", alignment=Qt.AlignmentFlag.AlignLeft)
		layout.addWidget(self.label)

		self.combo_box = QComboBox()
		self.combo_box.addItems(options)
		self.combo_box.setFixedHeight(32)
		self.combo_box.setFont(QFont("Segoe UI", 14))
		self.combo_box.setStyleSheet(
			"QComboBox { background-color: #222b40; color: #f4f8ff; border-radius: 7px; "
			"border: 1px solid #23304a; padding: 2px 12px; }"
			"QComboBox::drop-down { border: none; width: 30px; }"
			"QComboBox QAbstractItemView { background-color: #2C2C2C; color: white; selection-background-color: #2196F3; }"
		)
		self.combo_box.setMaxCount(max_rows)
		layout.addWidget(self.combo_box)


class ValueField(QWidget):
	def __init__(self, label: str, numeric: bool = False, limit: int = 999):
		super().__init__()
		self.setStyleSheet("background-color: transparent;")
		layout = QVBoxLayout(self)

		self.label = body_text(label, color="#ffffff", alignment=Qt.AlignmentFlag.AlignLeft)
		layout.addWidget(self.label)

		self.input = QLineEdit()
		self.input.setFixedHeight(32)
		self.input.setFont(QFont("Segoe UI", 14))
		self.input.setStyleSheet(
			"background: #232c39; color: #f4f8ff; border-radius: 7px; border: 1px solid #23304a; padding: 2px 12px;"
		)

		if numeric:
			from PyQt6.QtGui import QIntValidator
			self.input.setValidator(QIntValidator(0, limit))

		layout.addWidget(self.input)


class ToggleField(QWidget):
	def __init__(self, label: str, enabled: bool = False):
		super().__init__()
		self.setStyleSheet("background-color: transparent;")
		layout = QVBoxLayout(self)

		self.label = body_text(label, color="#ffffff", alignment=Qt.AlignmentFlag.AlignLeft)
		layout.addWidget(self.label)

		self.toggle = ToggleSwitch(enabled=enabled)
		layout.addWidget(self.toggle)


__all__ = ["DropdownField", "ValueField", "ToggleField"]

