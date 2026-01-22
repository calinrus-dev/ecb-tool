import os
import sys
import json
from PyQt6.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QComboBox, QLineEdit, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIntValidator, QPixmap
from PyQt6.QtSvgWidgets import QSvgWidget

from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.features.ui.legacy_src.application.process_controller import ProcessController
from ecb_tool.core.legacy import StateManager
from ecb_tool.core.shared.paths import ROOT_DIR, CONFIG_DIR, ORDER_PATH, PARAR_PATH
from ecb_tool.core.shared.file_validator import get_file_validator
from ecb_tool.features.ui.pieces.blink_animator import ModuleStateAnimator
from ecb_tool.core.shared.language_manager import get_language_manager

# SVG directory - usar ruta relativa al archivo actual
SVG_DIR = os.path.join(os.path.dirname(__file__), '..', 'pieces', 'svg')


def svg_pixmap(name, width=20, height=20):
	path = os.path.join(SVG_DIR, name)
	pixmap = QPixmap(width, height)
	pixmap.fill(Qt.GlobalColor.transparent)
	if not os.path.isfile(path):
		return pixmap
	svg = QSvgWidget(path)
	svg.setFixedSize(width, height)
	svg.render(pixmap)
	return pixmap


def read_process_state():
	if not os.path.exists(ORDER_PATH):
		return False
	try:
		with open(ORDER_PATH, encoding="utf-8") as f:
			data = json.load(f)
		return data.get("proceso", False)
	except Exception:
		return False


def write_process_state(state):
	try:
		with open(ORDER_PATH, 'r+', encoding="utf-8") as f:
			data = json.load(f)
			data["proceso"] = state
			f.seek(0)
			json.dump(data, f, indent=4)
			f.truncate()
	except Exception:
		pass


class ModulesPanel(QWidget):
	def __init__(self):
		super().__init__()
		self.screen_adapter = get_screen_adapter()
		self.setStyleSheet("background: transparent;")

		self.state = StateManager()
		self.controller = ProcessController()
		self.lang = get_language_manager()

		layout = QVBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		spacing = self.screen_adapter.get_spacing(20)
		layout.setSpacing(spacing)

		top_row = QHBoxLayout()
		top_row.setSpacing(32)

		panel_modules = QFrame()
		panel_modules.setStyleSheet("background-color: #181f2c; border-radius: 18px; border: 1px solid #23304a;")
		min_height = self.screen_adapter.scale(120)
		panel_modules.setMinimumHeight(min_height)
		panel_modules.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
		v_modules = QVBoxLayout(panel_modules)
		margin_h = self.screen_adapter.get_margin(32)
		margin_v = self.screen_adapter.get_margin(20)
		v_modules.setContentsMargins(margin_h, margin_v, margin_h, margin_v)
		v_modules.setSpacing(self.screen_adapter.get_spacing(16))

		# Convertidor
		self.conv_container = QFrame()
		self.conv_container.setStyleSheet("""
			QFrame {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
					stop:0 rgba(36, 234, 255, 0.05), 
					stop:1 rgba(36, 234, 255, 0.02));
				border: 2px solid rgba(36, 234, 255, 0.3);
				border-radius: 12px;
				padding: 12px;
			}
			QFrame:hover {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
					stop:0 rgba(36, 234, 255, 0.12), 
					stop:1 rgba(36, 234, 255, 0.05));
				border: 2px solid rgba(36, 234, 255, 0.6);
			}
		""")
		conv_layout = QHBoxLayout(self.conv_container)
		conv_layout.setContentsMargins(12, 10, 12, 10)
		conv_layout.setSpacing(16)
		
		self._icon_conv = QLabel()
		icon_size = self.screen_adapter.scale(32)
		self._icon_conv.setFixedSize(icon_size, icon_size)
		conv_layout.addWidget(self._icon_conv)
		
		self.lbl_conv = QLabel(self.lang.get_text('converter'))
		font_size = self.screen_adapter.get_font_size(20)
		self.lbl_conv.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
		self.lbl_conv.setStyleSheet("""
			color: #24eaff; 
			letter-spacing: 1.5px;
			text-transform: uppercase;
		""")
		self.lbl_conv.setVisible(True)
		conv_layout.addWidget(self.lbl_conv)
		conv_layout.addStretch()
		
		# Indicador de estado
		self.conv_status = QLabel("●")
		self.conv_status.setStyleSheet("color: #666; font-size: 16px;")
		conv_layout.addWidget(self.conv_status)
		
		v_modules.addWidget(self.conv_container)

		# Subidor
		self.up_container = QFrame()
		self.up_container.setStyleSheet("""
			QFrame {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
					stop:0 rgba(57, 152, 255, 0.05), 
					stop:1 rgba(57, 152, 255, 0.02));
				border: 2px solid rgba(57, 152, 255, 0.3);
				border-radius: 12px;
				padding: 12px;
			}
			QFrame:hover {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
					stop:0 rgba(57, 152, 255, 0.12), 
					stop:1 rgba(57, 152, 255, 0.05));
				border: 2px solid rgba(57, 152, 255, 0.6);
			}
		""")
		up_layout = QHBoxLayout(self.up_container)
		up_layout.setContentsMargins(12, 10, 12, 10)
		up_layout.setSpacing(16)
		
		self._icon_up = QLabel()
		icon_size = self.screen_adapter.scale(32)
		self._icon_up.setFixedSize(icon_size, icon_size)
		up_layout.addWidget(self._icon_up)
		
		self.lbl_up = QLabel(self.lang.get_text('uploader'))
		font_size = self.screen_adapter.get_font_size(20)
		self.lbl_up.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
		self.lbl_up.setStyleSheet("""
			color: #3998ff;
			letter-spacing: 1.5px;
			text-transform: uppercase;
		""")
		self.lbl_up.setVisible(True)
		up_layout.addWidget(self.lbl_up)
		up_layout.addStretch()
		
		# Indicador de estado
		self.up_status = QLabel("●")
		self.up_status.setStyleSheet("color: #666; font-size: 16px;")
		up_layout.addWidget(self.up_status)
		
		v_modules.addWidget(self.up_container)
		
		# Generador (no seleccionable por ahora)
		self.gen_container = QFrame()
		self.gen_container.setStyleSheet("""
			QFrame {
				background: rgba(50, 50, 50, 0.2);
				border: 2px dashed rgba(100, 100, 100, 0.3);
				border-radius: 12px;
				padding: 12px;
			}
		""")
		gen_layout = QHBoxLayout(self.gen_container)
		gen_layout.setContentsMargins(12, 10, 12, 10)
		gen_layout.setSpacing(16)
		
		self._icon_gen = QLabel()
		icon_size = self.screen_adapter.scale(32)
		self._icon_gen.setFixedSize(icon_size, icon_size)
		self._icon_gen.setPixmap(svg_pixmap("modulo_seleccionado.svg"))
		gen_layout.addWidget(self._icon_gen)
		
		self.lbl_gen = QLabel(self.lang.get_text('generator'))
		font_size = self.screen_adapter.get_font_size(20)
		self.lbl_gen.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
		self.lbl_gen.setStyleSheet("""
			color: #666;
			letter-spacing: 1.5px;
			text-transform: uppercase;
		""")
		self.lbl_gen.setVisible(True)
		gen_layout.addWidget(self.lbl_gen)
		gen_layout.addStretch()
		
		# Badge "Próximamente"
		coming_soon = QLabel("SOON")
		coming_soon.setStyleSheet("""
			background: rgba(255, 165, 0, 0.2);
			color: #ffa500;
			border: 1px solid rgba(255, 165, 0, 0.5);
			border-radius: 6px;
			padding: 4px 12px;
			font-size: 11px;
			font-weight: bold;
		""")
		gen_layout.addWidget(coming_soon)
		
		v_modules.addWidget(self.gen_container)

		top_row.addWidget(panel_modules, 2)

		panel_right = QFrame()
		panel_right.setStyleSheet("background-color: #181f2c; border-radius: 18px; border: 1px solid #23304a;")
		panel_right.setMinimumHeight(120)
		panel_right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
		v_right = QVBoxLayout(panel_right)
		v_right.setContentsMargins(32, 20, 32, 20)
		v_right.setSpacing(18)

		self.mode_selector = ModeSelector()
		v_right.addWidget(self.mode_selector)
		self.mode_selector.mode_combo.currentTextChanged.connect(self.on_mode_change)
		self.mode_selector.orders_input.editingFinished.connect(self.on_orders_change)
		self.mode_selector.bpv_input.editingFinished.connect(self.on_bpv_change)

		self.run_button = self._create_run_button()
		v_right.addWidget(self.run_button)
		self.run_button.clicked.connect(self._toggle_run)

		v_right.addStretch()
		top_row.addWidget(panel_right, 1)
		layout.addLayout(top_row)

		# Inicializar animadores
		self.conv_animator = ModuleStateAnimator(self.conv_container)
		self.up_animator = ModuleStateAnimator(self.up_container)
		self.file_validator = get_file_validator()
		
		self._update_states()
		self._sync_button_state()
		
		# Timer para actualizar estado reactivo
		self.update_timer = QTimer()
		self.update_timer.timeout.connect(self._update_states)
		self.update_timer.start(1000)  # Actualizar cada segundo
		
		# Conectar cambio de idioma
		self.lang.language_changed.connect(self._update_language)

	def _create_run_button(self):
		button = QPushButton(self.lang.get_text('execute'))
		button.setObjectName("run_button")
		button.setCursor(Qt.CursorShape.PointingHandCursor)
		min_height = self.screen_adapter.scale(50)
		button.setMinimumHeight(min_height)
		button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
		font_size = self.screen_adapter.get_font_size(18)
		button.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
		button.setStyleSheet("""
			QPushButton#run_button {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
					stop:0 #24eaff, stop:1 #3998ff);
				color: #fff;
				border-radius: 14px;
				border: 2px solid rgba(36, 234, 255, 0.5);
				letter-spacing: 2px;
				padding: 14px 28px;
				text-transform: uppercase;
			}
			QPushButton#run_button:hover {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
					stop:0 #3998ff, stop:1 #5aa8ff);
				border: 2px solid #24eaff;
			}
			QPushButton#run_button:pressed {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
					stop:0 #1976D2, stop:1 #2196F3);
				padding-top: 16px;
				padding-bottom: 12px;
			}
			QPushButton#run_button[active="true"] {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
					stop:0 #F44336, stop:1 #E53935);
				border: 2px solid rgba(244, 67, 54, 0.5);
			}
			QPushButton#run_button[active="true"]:hover {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
					stop:0 #E53935, stop:1 #D32F2F);
				border: 2px solid #ff6b6b;
			}
			QPushButton#run_button[disabled="true"] {
				background: #4a4a4a;
				color: #888;
				border: 2px solid #3a3a3a;
			}
		""")
		return button

	def on_mode_change(self, new_mode):
		self.state.modo = new_mode
		mapping = {
			"convertir": "convertir",
			"subir": "subir",
			"alternar": "alternar",
			"simultáneo": "simultaneo",
		}
		self._update_order_json({"modo": mapping.get(new_mode.lower(), "convertir")})
		self._update_states()  # Actualizar inmediatamente

	def on_orders_change(self):
		try:
			orders = int(self.mode_selector.orders_input.text().strip())
		except ValueError:
			orders = 1
		
		# Validar límites inteligentes basados en recursos
		max_orders = self._calculate_max_orders()
		orders = max(1, min(max_orders, orders))
		
		self.mode_selector.orders_input.setText(str(orders))
		self._update_order_json({"ordenes": orders})

	def on_bpv_change(self):
		try:
			bpv = int(self.mode_selector.bpv_input.text().strip())
		except ValueError:
			bpv = 1
		
		# Validar límites inteligentes basados en recursos
		max_bpv = self._calculate_max_bpv()
		bpv = max(1, min(max_bpv, bpv))
		
		self.mode_selector.bpv_input.setText(str(bpv))
		self._update_order_json({"bpv": bpv})

	def _toggle_run(self):
		active = read_process_state()
		if active:
			# Detener proceso
			self.controller.stop()
			write_process_state(False)
			# Parpadeo verde al terminar
			mode = self.mode_selector.mode_combo.currentText().lower()
			if "convertir" in mode or "alternar" in mode or "simult" in mode:
				self.conv_animator.set_state('completed', blink=True)
			if "subir" in mode or "alternar" in mode or "simult" in mode:
				self.up_animator.set_state('completed', blink=True)
		else:
			# Iniciar proceso
			validation = self.file_validator.check_all()
			mode = self.mode_selector.mode_combo.currentText().lower()
			
			# Verificar si puede ejecutar
			can_run = True
			if "convertir" in mode or "alternar" in mode or "simult" in mode:
				if not validation['conversion']['ready']:
					can_run = False
			if "subir" in mode or "alternar" in mode or "simult" in mode:
				if not validation['upload']['ready']:
					can_run = False
			
			if not can_run:
				print("No se puede ejecutar: faltan archivos")
				return
			
			if os.path.exists(PARAR_PATH):
				os.remove(PARAR_PATH)
			
			mapping = {
				"convertir": "convertir",
				"subir": "subir",
				"alternar": "alternar",
				"simultáneo": "simultaneo",
			}
			normalized = mapping.get(mode, "convertir")
			self._update_order_json({"modo": normalized, "proceso": True})
			print(f"Iniciando proceso: {normalized}")
			
			# Pasar self como parent para mostrar diálogos si es necesario
			self.controller.start(normalized, parent_widget=self)
		
		self._sync_button_state()
		self._update_states()

	def _sync_button_state(self):
		active = read_process_state()
		validation = self.file_validator.check_all()
		mode = self.mode_selector.mode_combo.currentText().lower()
		
		# Verificar si puede ejecutar
		can_run = True
		if "convertir" in mode and not validation['conversion']['ready']:
			can_run = False
		if "subir" in mode and not validation['upload']['ready']:
			can_run = False
		
		self.run_button.setProperty("active", active)
		self.run_button.setProperty("disabled", not can_run and not active)
		self.run_button.setEnabled(can_run or active)
		self.run_button.setText(self.lang.get_text('stop') if active else self.lang.get_text('execute'))
		self.run_button.style().unpolish(self.run_button)
		self.run_button.style().polish(self.run_button)

	def _update_order_json(self, updates):
		data = {}
		if os.path.exists(ORDER_PATH):
			try:
				with open(ORDER_PATH, "r", encoding="utf-8") as f:
					data = json.load(f)
			except Exception:
				data = {}
			order_dir = os.path.dirname(ORDER_PATH)
			if order_dir:
				os.makedirs(order_dir, exist_ok=True)
		data.update(updates)
		with open(ORDER_PATH, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=4, ensure_ascii=False)

	def _update_states(self):
		"""Actualiza estados visuales según validación y modo."""
		mode = self.mode_selector.mode_combo.currentText().lower()
		is_running = read_process_state()
		validation = self.file_validator.check_all()
		
		conv_active = mode in ["convertir", "alternar", "simultáneo"]
		up_active = mode in ["subir", "alternar", "simultáneo"]
		
		# Estado del convertidor
		if conv_active:
			if not validation['conversion']['ready']:
				# Faltan archivos - parpadeo rojo
				self._icon_conv.setPixmap(svg_pixmap("modulo_seleccionado.svg"))
				self.conv_animator.set_state('warning', blink=True)
			elif is_running:
				# En ejecución - borde blanco sólido
				self._icon_conv.setPixmap(svg_pixmap("modulo_activo.svg"))
				self.conv_animator.set_state('running', blink=False)
			else:
				# Listo - un parpadeo
				self._icon_conv.setPixmap(svg_pixmap("modulo_seleccionado.svg"))
				self.conv_animator.set_state('ready', blink=True)
		else:
			self._icon_conv.setPixmap(svg_pixmap("modulo_seleccionado.svg"))
			self.conv_animator.set_state('idle', blink=False)
		
		# Estado del subidor
		if up_active:
			if not validation['upload']['ready']:
				# Faltan archivos - parpadeo rojo
				self._icon_up.setPixmap(svg_pixmap("modulo_seleccionado.svg"))
				self.up_animator.set_state('warning', blink=True)
			elif is_running:
				# En ejecución - borde blanco sólido
				self._icon_up.setPixmap(svg_pixmap("modulo_activo.svg"))
				self.up_animator.set_state('running', blink=False)
			else:
				# Listo - un parpadeo
				self._icon_up.setPixmap(svg_pixmap("modulo_seleccionado.svg"))
				self.up_animator.set_state('ready', blink=True)
		else:
			self._icon_up.setPixmap(svg_pixmap("modulo_seleccionado.svg"))
			self.up_animator.set_state('idle', blink=False)
		
		self._icon_conv.setVisible(True)
		self._icon_up.setVisible(True)
	
	def _calculate_max_orders(self):
		"""Calcula el máximo de órdenes basado en recursos disponibles."""
		validation = self.file_validator.check_all()
		mode = self.mode_selector.mode_combo.currentText().lower()
		
		try:
			bpv = int(self.mode_selector.bpv_input.text().strip())
		except ValueError:
			bpv = 1
		
		if "convertir" in mode or "alternar" in mode or "simult" in mode:
			# Para conversión: beats / bpv = videos posibles
			beats_count = validation['conversion']['beats']
			covers_count = validation['conversion']['covers']
			
			if beats_count == 0 or covers_count == 0:
				return 1
			
			# Máximo de videos que se pueden crear
			max_from_beats = beats_count // max(1, bpv)
			max_from_covers = covers_count  # Cada video necesita 1 cover
			
			return min(max_from_beats, max_from_covers, 999)
		
		elif "subir" in mode:
			# Para subida: depende de videos y títulos disponibles
			videos_count = validation['upload']['videos']
			titles_count = validation['upload']['titles']
			
			if videos_count == 0 or titles_count == 0:
				return 1
			
			return min(videos_count, titles_count, 999)
		
		return 999
	
	def _calculate_max_bpv(self):
		"""Calcula el máximo BPV basado en beats disponibles y órdenes."""
		validation = self.file_validator.check_all()
		
		try:
			orders = int(self.mode_selector.orders_input.text().strip())
		except ValueError:
			orders = 1
		
		beats_count = validation['conversion']['beats']
		
		if beats_count == 0 or orders == 0:
			return 1
		
		# BPV máximo = beats disponibles / órdenes
		max_bpv = beats_count // orders
		
		return max(1, min(max_bpv, 100))
	
	def _update_language(self):
		"""Actualiza textos al cambiar idioma."""
		self.lbl_conv.setText(self.lang.get_text('converter'))
		self.lbl_up.setText(self.lang.get_text('uploader'))
		self.lbl_gen.setText(self.lang.get_text('generator'))
		self._sync_button_state()


class ModeSelector(QWidget):
	def __init__(self):
		super().__init__()
		self.lang = get_language_manager()
		layout = QHBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(10)

		self.mode_combo = QComboBox()
		self.mode_combo.addItems([
			self.lang.get_text('convert'),
			self.lang.get_text('upload'),
			self.lang.get_text('alternate'),
			self.lang.get_text('simultaneous')
		])
		self.mode_combo.setFixedHeight(32)
		self.mode_combo.setFixedWidth(140)
		self.mode_combo.setFont(QFont("Segoe UI", 15))
		self.mode_combo.setStyleSheet("""
			QComboBox {
				background-color: #222b40;
				color: #f4f8ff;
				border-radius: 8px;
				border: 1px solid #23304a;
				padding: 2px 12px;
				font-size: 15px;
			}
			QComboBox:hover {
				background-color: #2a3550;
				border: 1px solid #3998ff;
			}
			QComboBox::drop-down {
				border: none;
				width: 30px;
			}
			QComboBox::down-arrow {
				image: none;
				border-left: 5px solid transparent;
				border-right: 5px solid transparent;
				border-top: 6px solid #3998ff;
				margin-right: 8px;
			}
			QComboBox QAbstractItemView {
				background-color: #222b40;
				color: #f4f8ff;
				selection-background-color: #3998ff;
				border: 1px solid #23304a;
				outline: none;
			}
		""")
		layout.addWidget(self.mode_combo)

		# Label para órdenes
		self.orders_label = QLabel(self.lang.get_text('orders'))
		self.orders_label.setFont(QFont("Segoe UI", 13))
		self.orders_label.setStyleSheet("color: #8ad6ff; margin-left: 8px;")
		layout.addWidget(self.orders_label)

		self.orders_input = QLineEdit("1")
		self.orders_input.setFixedHeight(30)
		self.orders_input.setFixedWidth(54)
		self.orders_input.setFont(QFont("Segoe UI", 14))
		self.orders_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.orders_input.setValidator(QIntValidator(1, 999))
		self.orders_input.setStyleSheet("""
			QLineEdit {
				background: #232c39;
				color: #f4f8ff;
				border-radius: 8px;
				border: 1px solid #23304a;
				padding: 4px;
			}
			QLineEdit:hover {
				border: 1px solid #3998ff;
				background: #2a3545;
			}
			QLineEdit:focus {
				border: 2px solid #24eaff;
				background: #2a3545;
			}
		""")
		layout.addWidget(self.orders_input)

		# Label para BPV
		self.bpv_label = QLabel(self.lang.get_text('bpv'))
		self.bpv_label.setFont(QFont("Segoe UI", 13))
		self.bpv_label.setStyleSheet("color: #8ad6ff; margin-left: 12px;")
		self.bpv_label.setToolTip("Beats Por Video: cuántos beats juntar en cada vídeo")
		layout.addWidget(self.bpv_label)

		self.bpv_input = QLineEdit("1")
		self.bpv_input.setFixedHeight(30)
		self.bpv_input.setFixedWidth(54)
		self.bpv_input.setFont(QFont("Segoe UI", 14))
		self.bpv_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.bpv_input.setValidator(QIntValidator(1, 100))
		self.bpv_input.setStyleSheet("""
			QLineEdit {
				background: #232c39;
				color: #f4f8ff;
				border-radius: 8px;
				border: 1px solid #23304a;
				padding: 4px;
			}
			QLineEdit:hover {
				border: 1px solid #3998ff;
				background: #2a3545;
			}
			QLineEdit:focus {
				border: 2px solid #24eaff;
				background: #2a3545;
			}
		""")
		layout.addWidget(self.bpv_input)

		self._load_initial_state()
		
		# Conectar cambio de idioma
		self.lang.language_changed.connect(self._update_language)

	def _load_initial_state(self):
		if os.path.exists(ORDER_PATH):
			try:
				with open(ORDER_PATH, "r", encoding="utf-8") as f:
					data = json.load(f)
				raw = data.get("modo", "convertir")
				mapping = {
					"convertir": "Convert",
					"subir": "Upload",
					"alternar": "Alternate",
					"simultaneo": "Simultaneous",
					"convert": "Convert",
					"upload": "Upload",
					"alternate": "Alternate",
					"simultaneous": "Simultaneous",
				}
				mode = mapping.get(str(raw).lower(), "Convert")
				idx = self.mode_combo.findText(mode)
				if idx >= 0:
					self.mode_combo.setCurrentIndex(idx)
				self.orders_input.setText(str(data.get("ordenes", 1)))
				self.bpv_input.setText(str(data.get("bpv", 1)))
			except Exception:
				pass
	
	def _update_language(self):
		"""Actualiza textos al cambiar idioma."""
		self.orders_label.setText(self.lang.get_text('orders'))
		self.bpv_label.setText(self.lang.get_text('bpv'))
		# Actualizar items del combo
		current_idx = self.mode_combo.currentIndex()
		self.mode_combo.clear()
		self.mode_combo.addItems([
			self.lang.get_text('convert'),
			self.lang.get_text('upload'),
			self.lang.get_text('alternate'),
			self.lang.get_text('simultaneous')
		])
		self.mode_combo.setCurrentIndex(current_idx)
__all__ = ["ModulesPanel", "ModeSelector"]


