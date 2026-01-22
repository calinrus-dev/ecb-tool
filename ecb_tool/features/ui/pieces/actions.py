from PyQt6.QtWidgets import QWidget, QLineEdit, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen


class ToggleSwitch(QWidget):
	changed = pyqtSignal(bool)

	def __init__(self, enabled=True):
		super().__init__()
		self.setFixedSize(60, 30)
		self._enabled = bool(enabled)
		self.setCursor(Qt.CursorShape.PointingHandCursor)

	def is_enabled(self):
		return self._enabled

	def set_active(self, active: bool):
		self._enabled = bool(active)
		self.update()
		self.changed.emit(self._enabled)

	def mousePressEvent(self, event):
		self._enabled = not self._enabled
		self.update()
		self.changed.emit(self._enabled)

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		bg = QColor("#2196F3") if self._enabled else QColor("#555555")
		painter.setBrush(QBrush(bg))
		painter.setPen(QPen(Qt.PenStyle.NoPen))
		painter.drawRoundedRect(self.rect(), 15, 15)
		x = self.width() - 28 if self._enabled else 4
		painter.setBrush(QBrush(Qt.GlobalColor.white))
		painter.drawEllipse(QRect(x, 3, 24, 24))


def text_input(value: str = ""):
	field = QLineEdit()
	field.setText(value)
	field.setStyleSheet(
		"background-color: #232c39; color: #f2f7ff; border: 1px solid #283654; "
		"border-radius: 5px; font-size: 14px; padding: 6px 12px;"
	)
	return field


def combo_box(options, selected=""):
	combo = QComboBox()
	combo.addItems(options)
	if selected:
		combo.setCurrentText(selected)
	combo.setStyleSheet(
		"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4F4F4F, stop:1 #2C2C2C);"
		"color: white; padding: 6px 12px; border: none; border-radius: 10px; font-size: 16px;"
	)
	return combo


__all__ = ["ToggleSwitch", "text_input", "combo_box"]
