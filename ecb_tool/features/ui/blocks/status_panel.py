import os
import sys
import csv
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QFrame, QSizePolicy, QProgressBar, QScrollArea
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from ecb_tool.core.legacy import StateManager
from ecb_tool.features.ui.pieces.text import bar_text
from ecb_tool.features.ui.pieces.progress_bar import SmartProgressBar
from ecb_tool.core.shared.paths import DATA_DIR, CONVERSION_STATE_CSV, UPLOAD_STATE_CSV
from ecb_tool.core.shared.language_manager import get_language_manager


class StatusPanel(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setMinimumWidth(280)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.setStyleSheet("""
			QWidget {
				background-color: #181f2c;
				border-radius: 18px;
				border: 1px solid #23304a;
			}
			QWidget:hover {
				border: 1px solid #2a4060;
			}
		""")
		
		main_layout = QVBoxLayout(self)
		main_layout.setContentsMargins(16, 14, 16, 14)
		main_layout.setSpacing(10)

		self.lang = get_language_manager()

		self.title = bar_text(self.lang.get_text('status'), color="#24eaff", bold=True)
		self.title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
		self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.title.setStyleSheet("color: #24eaff;")
		main_layout.addWidget(self.title)

		self.state = StateManager()
		self.label_state = QLabel(self.lang.get_text('ready'))
		self.label_state.setStyleSheet("color: #8ad6ff; font-size: 16px; font-weight: bold; margin-top: 4px;")
		self.label_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
		main_layout.addWidget(self.label_state)

		# Contenedor para barras dinámicas
		self.bars_container = QWidget()
		self.bars_layout = QVBoxLayout(self.bars_container)
		self.bars_layout.setContentsMargins(0, 8, 0, 0)
		self.bars_layout.setSpacing(8)
		main_layout.addWidget(self.bars_container)
		
		# Barras de progreso (ocultas por defecto)
		self.conversion_bar = SmartProgressBar(self.lang.get_text('conversion'), show_percentage=True, animate=True)
		self.conversion_bar.hide()
		self.bars_layout.addWidget(self.conversion_bar)
		
		self.upload_bar = SmartProgressBar(self.lang.get_text('uploads'), show_percentage=True, animate=True)
		self.upload_bar.hide()
		self.bars_layout.addWidget(self.upload_bar)
		
		# Scroll area para las tareas
		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
		scroll.setStyleSheet("""
			QScrollArea {
				border: none;
				background: transparent;
			}
			QScrollBar:vertical {
				background: rgba(35, 48, 74, 0.3);
				width: 8px;
				border-radius: 4px;
				margin: 0px;
			}
			QScrollBar::handle:vertical {
				background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
					stop:0 #24eaff, stop:1 #3998ff);
				border-radius: 4px;
				min-height: 20px;
			}
			QScrollBar::handle:vertical:hover {
				background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
					stop:0 #3998ff, stop:1 #5aa8ff);
			}
			QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
				height: 0px;
			}
			QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
				background: none;
			}
		""")
		
		# Contenedor de tareas
		self.tasks_container = QWidget()
		self.tasks_layout = QVBoxLayout(self.tasks_container)
		self.tasks_layout.setContentsMargins(0, 0, 0, 0)
		self.tasks_layout.setSpacing(4)
		self.tasks_layout.addStretch()
		
		scroll.setWidget(self.tasks_container)
		main_layout.addWidget(scroll, 1)  # El scroll toma el espacio restante
		
		self.scroll_area = scroll
		self.rows = []

		self.state.mode_changed.connect(self.update_state)
		self.state.action_requested.connect(self.show_action)

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.refresh)
		self.timer.start(1000)
		self.refresh()
		
		# Conectar cambio de idioma
		self.lang.language_changed.connect(self._update_language)

	def _tail_rows(self, path, n=6):
		try:
			if not os.path.isfile(path):
				return []
			with open(path, encoding="utf-8") as f:
				rows = list(csv.reader(f))
				return rows[-n:]
		except Exception:
			return []

	def refresh(self):
		self._clear_rows()
		conv_rows = self._tail_rows(CONVERSION_STATE_CSV, 10)
		upload_rows = self._tail_rows(UPLOAD_STATE_CSV, 10)
		
		# Barras de conversión
		if conv_rows:
			conv_rows_valid = [r for r in conv_rows if r and len(r) >= 5]
			if conv_rows_valid:
				total_conv = len(conv_rows_valid)
				completed_conv = sum(1 for r in conv_rows_valid if "completado" in r[4].lower() or "convertido" in r[4].lower() or "completed" in r[4].lower() or "converted" in r[4].lower())
				active_conv = any("convirtiendo" in r[4].lower() or "converting" in r[4].lower() for r in conv_rows_valid)
				
				if active_conv or completed_conv < total_conv:
					self.conversion_bar.show()
					progress_conv = int((completed_conv / total_conv) * 100)
					mode = "success" if progress_conv == 100 else "converting"
					self.conversion_bar.set_value(progress_conv, mode)
					if active_conv:
						self.conversion_bar.set_indeterminate(False)
				else:
					self.conversion_bar.hide()
			else:
				self.conversion_bar.hide()
		else:
			self.conversion_bar.hide()
		
		# Barras de subida
		if upload_rows:
			upload_rows_valid = [r for r in upload_rows if r and len(r) >= 5]
			if upload_rows_valid:
				total_up = len(upload_rows_valid)
				completed_up = sum(1 for r in upload_rows_valid if "completado" in r[4].lower() or "subido" in r[4].lower() or "completed" in r[4].lower() or "uploaded" in r[4].lower())
				active_up = any("subiendo" in r[4].lower() or "uploading" in r[4].lower() for r in upload_rows_valid)
				
				if active_up or completed_up < total_up:
					self.upload_bar.show()
					progress_up = int((completed_up / total_up) * 100)
					mode = "success" if progress_up == 100 else "uploading"
					self.upload_bar.set_value(progress_up, mode)
					if active_up:
						self.upload_bar.set_indeterminate(False)
				else:
					self.upload_bar.hide()
			else:
				self.upload_bar.hide()
		else:
			self.upload_bar.hide()
		
		# Combinar y mostrar tareas
		rows = conv_rows + upload_rows
		rows = [r for r in rows if r and len(r) >= 5]
		try:
			rows.sort(key=lambda x: x[0], reverse=True)
		except Exception:
			pass
		rows = rows[:10]  # Máximo 10 tareas
		
		for row in rows:
			self._add_row(row[0], row[4])
		
		# Auto-scroll al final si hay nuevas tareas
		QTimer.singleShot(100, self._auto_scroll)

	def _add_row(self, text, status):
		"""Crea una fila con barra de progreso inteligente para cada proceso."""
		row_widget = QFrame()
		row_widget.setStyleSheet("""
			QFrame {
				background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
					stop:0 rgba(35, 48, 74, 0.3), stop:1 rgba(35, 48, 74, 0.1));
				border-radius: 8px;
				border: 1px solid rgba(42, 64, 96, 0.4);
				padding: 6px;
			}
			QFrame:hover {
				background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
					stop:0 rgba(36, 234, 255, 0.08), stop:1 rgba(57, 152, 255, 0.05));
				border: 1px solid rgba(36, 234, 255, 0.4);
			}
		""")
		row_layout = QVBoxLayout(row_widget)
		row_layout.setContentsMargins(8, 6, 8, 6)
		row_layout.setSpacing(6)

		# Línea superior: icono tipo + texto
		top_row = QHBoxLayout()
		top_row.setSpacing(10)

		status_clean = status.strip().lower()
		is_converting = "convirtiendo" in status_clean or "converting" in status_clean
		is_uploading = "subiendo" in status_clean or "uploading" in status_clean
		is_processing = is_converting or is_uploading
		is_completed = "completado" in status_clean or "convertido" in status_clean or "subido" in status_clean or "completed" in status_clean or "converted" in status_clean or "uploaded" in status_clean
		is_error = "error" in status_clean or "failed" in status_clean

		# Icono de tipo de proceso
		type_icon = QLabel()
		type_icon.setFont(QFont("Segoe UI", 14))
		if is_converting:
			type_icon.setText("⚙")
			type_icon.setStyleSheet("color: #24eaff;")
			type_icon.setToolTip("Conversión")
		elif is_uploading:
			type_icon.setText("▲")
			type_icon.setStyleSheet("color: #3998ff;")
			type_icon.setToolTip("Subida")
		elif is_completed:
			type_icon.setText("✓")
			type_icon.setStyleSheet("color: #43b680;")
			type_icon.setToolTip("Completado")
		elif is_error:
			type_icon.setText("✗")
			type_icon.setStyleSheet("color: #e05353;")
			type_icon.setToolTip("Error")
		else:
			type_icon.setText("○")
			type_icon.setStyleSheet("color: #9faab8;")
			type_icon.setToolTip("Pendiente")
		type_icon.setFixedWidth(24)
		top_row.addWidget(type_icon)

		# Texto del archivo
		label_text = QLabel(text[:40] + "..." if len(text) > 40 else text)
		label_text.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold if is_processing else QFont.Weight.Normal))
		if is_completed:
			label_text.setStyleSheet("color: #8a8a8a;")
		elif is_error:
			label_text.setStyleSheet("color: #e05353;")
		elif is_processing:
			label_text.setStyleSheet("color: #ffffff;")
		else:
			label_text.setStyleSheet("color: #b0b8c0;")
		label_text.setWordWrap(False)
		top_row.addWidget(label_text, 1)

		# Estado texto
		status_label = QLabel(status[:20] + "..." if len(status) > 20 else status)
		status_label.setFont(QFont("Segoe UI", 9))
		if is_completed:
			status_label.setStyleSheet("color: #43b680; font-weight: bold;")
		elif is_error:
			status_label.setStyleSheet("color: #e05353; font-weight: bold;")
		elif is_processing:
			status_label.setStyleSheet("color: #24eaff; font-weight: bold;")
		else:
			status_label.setStyleSheet("color: #6a7380;")
		top_row.addWidget(status_label)

		row_layout.addLayout(top_row)

		# Barra de progreso individual (solo si está procesando)
		if is_processing:
			progress_bar = QProgressBar()
			progress_bar.setRange(0, 0)  # Modo indeterminado
			progress_bar.setTextVisible(False)
			progress_bar.setFixedHeight(6)
			
			# Color según tipo
			if is_converting:
				gradient_color = "stop:0 #24eaff, stop:0.5 #3998ff, stop:1 #24eaff"
			else:  # uploading
				gradient_color = "stop:0 #3998ff, stop:0.5 #5aa8ff, stop:1 #3998ff"
			
			progress_bar.setStyleSheet(f"""
				QProgressBar {{
					border: none;
					border-radius: 3px;
					background-color: rgba(13, 17, 23, 0.6);
				}}
				QProgressBar::chunk {{
					background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
						{gradient_color});
					border-radius: 3px;
				}}
			""")
			row_layout.addWidget(progress_bar)

		self.rows.append(row_widget)
		# Insertar antes del stretch
		self.tasks_layout.insertWidget(self.tasks_layout.count() - 1, row_widget)
	
	def _auto_scroll(self):
		"""Auto-scroll inteligente: solo al final si hay procesos activos."""
		scrollbar = self.scroll_area.verticalScrollBar()
		
		# Verificar si hay procesos activos (no completados)
		has_active = False
		for row in self.rows[-3:]:  # Verificar últimas 3 filas
			labels = row.findChildren(QLabel)
			for label in labels:
				text = label.text().lower()
				if "convirtiendo" in text or "subiendo" in text or "converting" in text or "uploading" in text:
					has_active = True
					break
			if has_active:
				break
		
		# Auto-scroll solo si hay procesos activos o usuario está al final
		current_pos = scrollbar.value()
		max_pos = scrollbar.maximum()
		is_at_bottom = (max_pos - current_pos) < 50  # Tolerancia de 50px
		
		if has_active or is_at_bottom:
			scrollbar.setValue(max_pos)

	def _clear_rows(self):
		for row in self.rows:
			self.tasks_layout.removeWidget(row)
			row.deleteLater()
		self.rows = []

	def update_state(self, new_mode):
		self.label_state.setText(f"{self.lang.get_text('mode')}: {new_mode}")

	def show_action(self, action):
		self.label_state.setText(f"{self.lang.get_text('executing')}: {action}")
	
	def _update_language(self):
		"""Actualiza textos al cambiar idioma."""
		self.title.setText(self.lang.get_text('status'))
		self.label_state.setText(self.lang.get_text('ready'))
		self.conversion_bar.label.setText(self.lang.get_text('conversion'))
		self.upload_bar.label.setText(self.lang.get_text('uploads'))


__all__ = ["StatusPanel"]

