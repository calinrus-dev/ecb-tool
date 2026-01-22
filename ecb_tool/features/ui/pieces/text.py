from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from ecb_tool.core.shared.screen_utils import get_screen_adapter


def title_text(
	text: str,
	color: str = "#2196F3",
	alignment=Qt.AlignmentFlag.AlignCenter,
	bold: bool = True,
):
	screen = get_screen_adapter()
	size = screen.get_font_size(28)
	label = QLabel(text)
	label.setFont(QFont("Segoe UI", size, QFont.Weight.Bold if bold else QFont.Weight.Normal))
	label.setStyleSheet(f"color: {color};")
	label.setAlignment(alignment)
	return label


def header_text(
	text: str,
	color: str = "#fff",
	alignment=Qt.AlignmentFlag.AlignCenter,
	bold: bool = True,
):
	screen = get_screen_adapter()
	size = screen.get_font_size(20)
	label = QLabel(text)
	label.setFont(QFont("Segoe UI", size, QFont.Weight.DemiBold if bold else QFont.Weight.Normal))
	label.setStyleSheet(f"color: {color};")
	label.setAlignment(alignment)
	return label


def body_text(
	text: str,
	color: str = "#fff",
	alignment=Qt.AlignmentFlag.AlignCenter,
	bold: bool = False,
):
	screen = get_screen_adapter()
	size = screen.get_font_size(14)
	label = QLabel(text)
	label.setFont(QFont("Segoe UI", size, QFont.Weight.Bold if bold else QFont.Weight.Normal))
	label.setStyleSheet(f"color: {color};")
	label.setAlignment(alignment)
	return label


def bar_text(
	text: str,
	color: str = "#fff",
	alignment=Qt.AlignmentFlag.AlignCenter,
	bold: bool = False,
	background: str | None = None,
):
	label = QLabel(text)
	label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold if bold else QFont.Weight.Normal))
	style = f"color: {color};"
	if background:
		style += f" background: {background}; border-radius: 8px; padding: 3px 16px;"
	label.setStyleSheet(style)
	label.setAlignment(alignment)
	return label


class TextLabel(QLabel):
	def __init__(self, text, size=16, color="#fff", bold=False, alignment=Qt.AlignmentFlag.AlignCenter, parent=None):
		super().__init__(text, parent)
		self.setFont(QFont("Segoe UI", size, QFont.Weight.Bold if bold else QFont.Weight.Normal))
		self.setStyleSheet(f"color: {color};")
		self.setAlignment(alignment)


__all__ = ["title_text", "header_text", "body_text", "bar_text", "TextLabel"]
