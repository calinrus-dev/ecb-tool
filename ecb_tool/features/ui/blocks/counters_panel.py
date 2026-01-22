import os
from PyQt6.QtWidgets import QWidget, QGridLayout, QSizePolicy, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
import json

from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.features.ui.blocks.counter_widget import CounterWidget
from ecb_tool.core.config import ConfigManager
from ecb_tool.core.legacy import StateManager
from ecb_tool.core.shared.paths import ROOT_DIR, ROUTES_CONFIG_PATH, ORDER_PATH
from ecb_tool.core.shared.language_manager import get_language_manager


class CountersPanel(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.screen_adapter = get_screen_adapter()
		self.lang = get_language_manager()
		self.setObjectName("CountersPanel")
		self.setStyleSheet("background-color: #141b28; border-radius: 18px; border: 1px solid #23304a;")
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

		schema = {"rutas": {"beats_entrada": "beats/", "portadas_entrada": "covers/", "titulos": "data/titles.txt"}}
		self.config = ConfigManager(ROUTES_CONFIG_PATH, schema)
		self.state = StateManager()
		self.state.mode_changed.connect(self.refresh_counters)

		layout = QGridLayout(self)
		h_spacing = self.screen_adapter.get_spacing(20)
		v_spacing = self.screen_adapter.get_spacing(16)
		margin = self.screen_adapter.get_margin(16)
		layout.setHorizontalSpacing(h_spacing)
		layout.setVerticalSpacing(v_spacing)
		layout.setContentsMargins(margin, margin, margin, margin)

		routes = self.config.get("rutas", {})

		self.counters = {}

		beats_path = os.path.join(ROOT_DIR, routes.get("beats_entrada", "beats/"))
		self.counters["beats"] = CounterWidget(self.lang.get_text('beats'), path_to_open=beats_path)
		layout.addWidget(self.counters["beats"], 0, 0)

		covers_path = os.path.join(ROOT_DIR, routes.get("portadas_entrada", "covers/"))
		if not os.path.isdir(covers_path):
			covers_path = os.path.join(ROOT_DIR, 'portadas')
		self.counters["covers"] = CounterWidget(self.lang.get_text('covers'), path_to_open=covers_path)
		layout.addWidget(self.counters["covers"], 0, 1)
		
		# Videos
		videos_path = os.path.join(ROOT_DIR, "workspace/videos")
		self.counters["videos"] = CounterWidget(self.lang.get_text('videos'), path_to_open=videos_path)
		layout.addWidget(self.counters["videos"], 0, 2)

		titles_path = os.path.join(ROOT_DIR, routes.get("titulos", "data/titles.txt"))
		self.counters["titles"] = CounterWidget(self.lang.get_text('titles'), path_to_open=titles_path)
		layout.addWidget(self.counters["titles"], 1, 0)
		
		# Selector de modo de portadas
		cover_mode_container = QWidget()
		cover_mode_layout = QVBoxLayout(cover_mode_container)
		cover_mode_layout.setContentsMargins(0, 0, 0, 0)
		cover_mode_layout.setSpacing(6)

		self.mode_label = QLabel(self.lang.get_text('cover_mode'))
		self.mode_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
		self.mode_label.setStyleSheet("color: #8ad6ff;")
		cover_mode_layout.addWidget(self.mode_label)

		self.cover_mode_combo = QComboBox()
		self.cover_mode_combo.addItems([
			self.lang.get_text('random'),
			self.lang.get_text('random_no_repeat'),
			self.lang.get_text('select_one'),
			self.lang.get_text('sequential')
		])
		self.cover_mode_combo.setFont(QFont("Segoe UI", 12))
		self.cover_mode_combo.setStyleSheet("""
			QComboBox {
				background-color: #1a2332;
				color: #f4f8ff;
				border: 1px solid #23304a;
				border-radius: 6px;
				padding: 5px 10px;
			}
			QComboBox::drop-down {
				border: none;
				width: 28px;
			}
			QComboBox::down-arrow {
				image: none;
				border-left: 4px solid transparent;
				border-right: 4px solid transparent;
				border-top: 5px solid #3998ff;
				margin-right: 6px;
			}
			QComboBox QAbstractItemView {
				background-color: #1a2332;
				color: #f4f8ff;
				selection-background-color: #3998ff;
				border: 1px solid #23304a;
			}
		""")
		self.cover_mode_combo.currentTextChanged.connect(self._on_cover_mode_change)
		cover_mode_layout.addWidget(self.cover_mode_combo)

		layout.addWidget(cover_mode_container, 1, 1)
		
		# Descripción
		desc_path = os.path.join(ROOT_DIR, "data/description.txt")
		self.counters["description"] = CounterWidget(self.lang.get_text('description'), path_to_open=desc_path)
		layout.addWidget(self.counters["description"], 1, 2)

		self.setLayout(layout)

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.refresh_all)
		self.timer.start(1000)

		self._load_cover_mode()
		
		# Conectar cambio de idioma
		self.lang.language_changed.connect(self._update_language)

	def _load_cover_mode(self):
		"""Cargar el modo de portada guardado"""
		if os.path.exists(ORDER_PATH):
			try:
				with open(ORDER_PATH, "r", encoding="utf-8") as f:
					data = json.load(f)
				mode = data.get("cover_mode", "Random")
				idx = self.cover_mode_combo.findText(mode)
				if idx >= 0:
					self.cover_mode_combo.setCurrentIndex(idx)
			except Exception:
				pass

	def _on_cover_mode_change(self, new_mode):
		"""Guardar el modo de portada seleccionado"""
		if not os.path.exists(ORDER_PATH):
			os.makedirs(os.path.dirname(ORDER_PATH), exist_ok=True)
			data = {}
		else:
			try:
				with open(ORDER_PATH, "r", encoding="utf-8") as f:
					data = json.load(f)
			except Exception:
				data = {}
		
		data["cover_mode"] = new_mode
		
		with open(ORDER_PATH, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=4, ensure_ascii=False)

	def refresh_all(self):
		for counter in self.counters.values():
			counter.refresh()

	def refresh_counters(self, _new_mode):
		for counter in self.counters.values():
			counter.refresh()
	
	def _update_language(self):
		"""Actualiza textos al cambiar idioma."""
		self.mode_label.setText(self.lang.get_text('cover_mode'))
		# Actualizar combo manteniendo selección
		current_idx = self.cover_mode_combo.currentIndex()
		self.cover_mode_combo.clear()
		self.cover_mode_combo.addItems([
			self.lang.get_text('random'),
			self.lang.get_text('random_no_repeat'),
			self.lang.get_text('select_one'),
			self.lang.get_text('sequential')
		])
		self.cover_mode_combo.setCurrentIndex(current_idx)
		
		# Actualizar labels de contadores
		self.counters["beats"].label_text.setText(self.lang.get_text('beats'))
		self.counters["covers"].label_text.setText(self.lang.get_text('covers'))
		self.counters["videos"].label_text.setText(self.lang.get_text('videos'))
		self.counters["titles"].label_text.setText(self.lang.get_text('titles'))
		self.counters["description"].label_text.setText(self.lang.get_text('description'))


__all__ = ["CountersPanel"]

