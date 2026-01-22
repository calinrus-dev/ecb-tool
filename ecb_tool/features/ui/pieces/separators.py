from PyQt6.QtWidgets import QFrame, QWidget
from PyQt6.QtCore import QSize


def spacer_horizontal(height=10):
	widget = QWidget()
	widget.setFixedHeight(height)
	return widget


def spacer_vertical(width=10):
	widget = QWidget()
	widget.setFixedWidth(width)
	return widget


def separator_horizontal(thickness=1, color="#FFFFFF"):
	line = QFrame()
	line.setFrameShape(QFrame.Shape.HLine)
	line.setFrameShadow(QFrame.Shadow.Plain)
	line.setStyleSheet(f"background-color: {color};")
	line.setFixedHeight(thickness)
	return line


def separator_vertical(thickness=1, color="#FFFFFF"):
	line = QFrame()
	line.setFrameShape(QFrame.Shape.VLine)
	line.setFrameShadow(QFrame.Shadow.Plain)
	line.setStyleSheet(f"background-color: {color};")
	line.setFixedWidth(thickness)
	return line


def frame_box(width=200, height=100, border=1, radius=12, color="#FFFFFF"):
	widget = QWidget()
	widget.setFixedSize(QSize(width, height))
	widget.setStyleSheet(
		f"border: {border}px solid {color}; border-radius: {radius}px; background-color: transparent;"
	)
	return widget


def top_bar(width=800, height=40):
	widget = QWidget()
	widget.setFixedSize(QSize(width, height))
	widget.setStyleSheet(
		"background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0A0A0A, stop:1 #111111);"
		"border: none;"
	)
	return widget


__all__ = [
	"spacer_horizontal",
	"spacer_vertical",
	"separator_horizontal",
	"separator_vertical",
	"frame_box",
	"top_bar",
]
