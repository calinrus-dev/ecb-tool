import os
import json
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QTimer

from ecb_tool.features.ui.legacy_src.application.process_controller import ProcessController


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
ORDER_PATH = os.path.join(CONFIG_DIR, "orden.json")

if not os.path.isdir(CONFIG_DIR):
	CONFIG_DIR = os.path.join(ROOT_DIR, "configuracion")
	ORDER_PATH = os.path.join(CONFIG_DIR, "orden.json")


def read_process_state():
	if not os.path.exists(ORDER_PATH):
		return False
	try:
		with open(ORDER_PATH, encoding="utf-8") as f:
			data = json.load(f)
		return data.get("proceso", False)
	except Exception:
		return False


def read_mode():
	if not os.path.exists(ORDER_PATH):
		return "convertir"
	try:
		with open(ORDER_PATH, encoding="utf-8") as f:
			data = json.load(f)
		return data.get("modo", "convertir")
	except Exception:
		return "convertir"


class RunStopButton(QPushButton):
	def __init__(self):
		super().__init__()
		self.setObjectName("run_stop_button")
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.setMinimumSize(230, 50)
		self.setMaximumSize(350, 60)
		self.setStyleSheet(
			"QPushButton#run_stop_button { background-color: #2196F3; color: #fff; font-size: 22px; font-weight: bold; "
			"border-radius: 14px; padding: 12px 25px; }"
			"QPushButton#run_stop_button:hover { background-color: #1976D2; color: #e3eefd; }"
			"QPushButton#run_stop_button[active='true'] { background-color: #F44336; color: #fff; }"
			"QPushButton#run_stop_button[active='true']:hover { background-color: #D32F2F; color: #ffeaea; }"
		)
		self.controller = ProcessController()
		self.clicked.connect(self.toggle_state)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_state)
		self.timer.start(400)
		self.update_state()

	def update_state(self):
		active = read_process_state()
		self.setProperty("active", active)
		self.setText("STOP" if active else "RUN")
		self.style().unpolish(self)
		self.style().polish(self)

	def toggle_state(self):
		active = read_process_state()
		if active:
			self.controller.stop()
		else:
			# Pasar self como parent para mostrar diálogos
			self.controller.start(read_mode(), parent_widget=self)
		QTimer.singleShot(600, self.update_state)


__all__ = ["RunStopButton"]

