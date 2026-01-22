import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox, 
                             QPushButton, QGroupBox, QGridLayout, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ecb_tool.core.shared.screen_utils import get_screen_adapter
from ecb_tool.core.config import ConfigManager
from ecb_tool.core.shared.paths import ROOT_DIR

CONVERSION_CONFIG_PATH = os.path.join(ROOT_DIR, 'config', 'ajustes_conversion.json')


class FFmpegSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen_adapter = get_screen_adapter()
        
        self.setWindowTitle("Configuración de Conversión FFMPEG")
        self.setModal(True)
        
        # Tamaño adaptativo
        width, height = self.screen_adapter.get_dialog_size(900, 700)
        self.setMinimumSize(int(width * 0.8), int(height * 0.8))
        self.resize(width, height)
        
        schema = {
            "conversion": {
                "bpv": 1,
                "lotes": 2,
                "resolucion": "1920x1080",
                "fps": 30,
                "bitrate_video": "2M",
                "formato_video": "mp4",
                "bitrate_audio": "192k",
                "formato_audio": "aac",
                "ajuste_volumen_db": 0.0,
                "fade_in_video": {"activo": True, "duracion": 2},
                "fade_out_video": {"activo": True, "duracion": 2},
                "fade_transicion_video": {"activo": True, "duracion": 1},
                "fade_in_audio": {"activo": True, "duracion": 2},
                "fade_out_audio": {"activo": True, "duracion": 2},
                "fade_transicion_audio": {"activo": False, "duracion": 0},
                "multiportada": False,
                "loop_portada": True,
                "autoborrado_beats": True,
                "autoborrado_portadas": False,
                "enviar_beats_papelera": False,
                "enviar_portadas_papelera": False,
                "codec_video": "libx264",
                "preset": "medium",
                "crf": 23,
                "audio_channels": 2,
                "audio_sample_rate": 44100
            }
        }
        
        self.config = ConfigManager(CONVERSION_CONFIG_PATH, schema)
        self.setStyleSheet("""
            QDialog {
                background-color: #101722;
            }
            QLabel {
                color: #f4f8ff;
                font-size: 14px;
            }
            QGroupBox {
                color: #24eaff;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #23304a;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 18px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0px 10px;
                color: #24eaff;
            }
            QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #1a2332;
                color: #f4f8ff;
                border: 1px solid #23304a;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
                min-width: 100px;
            }
            QSpinBox:hover, QDoubleSpinBox:hover, QComboBox:hover {
                border: 1px solid #3998ff;
            }
            QSpinBox::up-button, QDoubleSpinBox::up-button {
                background-color: #23304a;
                border-left: 1px solid #23304a;
                border-top-right-radius: 6px;
            }
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                background-color: #23304a;
                border-left: 1px solid #23304a;
                border-bottom-right-radius: 6px;
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
                background-color: #1a2332;
                color: #f4f8ff;
                selection-background-color: #3998ff;
                border: 1px solid #23304a;
                border-radius: 6px;
            }
            QCheckBox {
                color: #f4f8ff;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #23304a;
                border-radius: 5px;
                background-color: #1a2332;
            }
            QCheckBox::indicator:checked {
                background-color: #3998ff;
                border-color: #3998ff;
            }
            QCheckBox::indicator:hover {
                border-color: #3998ff;
            }
            QPushButton {
                background-color: #3998ff;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4fa8ff;
            }
            QPushButton:pressed {
                background-color: #2888ef;
            }
            QPushButton#cancelButton {
                background-color: #2a3544;
            }
            QPushButton#cancelButton:hover {
                background-color: #344152;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        self._init_ui()
        self._load_values()
    
    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Título
        title = QLabel("Configuración de Conversión FFMPEG")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #24eaff; margin-bottom: 10px;")
        main_layout.addWidget(title)
        
        # Área de scroll para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        
        # GRUPO 1: Configuración General
        general_group = QGroupBox("Configuración General")
        general_layout = QGridLayout()
        general_layout.setSpacing(12)
        
        # BPV (Beats Por Video)
        bpv_label = QLabel("BPV (Beats Por Video):")
        bpv_label.setToolTip("Número de audios que se juntarán por cada vídeo.\nEjemplo: 10 beats con BPV=2 → 5 vídeos de 2 beats cada uno")
        self.bpv_spin = QSpinBox()
        self.bpv_spin.setMinimum(1)
        self.bpv_spin.setMaximum(100)
        general_layout.addWidget(bpv_label, 0, 0)
        general_layout.addWidget(self.bpv_spin, 0, 1)
        
        # Lotes
        lotes_label = QLabel("Lotes paralelos:")
        self.lotes_spin = QSpinBox()
        self.lotes_spin.setMinimum(1)
        self.lotes_spin.setMaximum(10)
        general_layout.addWidget(lotes_label, 0, 2)
        general_layout.addWidget(self.lotes_spin, 0, 3)
        
        general_group.setLayout(general_layout)
        content_layout.addWidget(general_group)
        
        # GRUPO 2: Video
        video_group = QGroupBox("Configuración de Video")
        video_layout = QGridLayout()
        video_layout.setSpacing(12)
        
        # Resolución
        res_label = QLabel("Resolución:")
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems([
            "1920x1080", "1280x720", "2560x1440", "3840x2160",
            "854x480", "640x360"
        ])
        video_layout.addWidget(res_label, 0, 0)
        video_layout.addWidget(self.resolution_combo, 0, 1)
        
        # FPS
        fps_label = QLabel("FPS:")
        self.fps_spin = QSpinBox()
        self.fps_spin.setMinimum(15)
        self.fps_spin.setMaximum(120)
        video_layout.addWidget(fps_label, 0, 2)
        video_layout.addWidget(self.fps_spin, 0, 3)
        
        # Bitrate Video
        bitrate_v_label = QLabel("Bitrate Video:")
        self.bitrate_video_combo = QComboBox()
        self.bitrate_video_combo.addItems(["1M", "2M", "3M", "4M", "5M", "8M", "10M"])
        video_layout.addWidget(bitrate_v_label, 1, 0)
        video_layout.addWidget(self.bitrate_video_combo, 1, 1)
        
        # Formato Video
        formato_v_label = QLabel("Formato:")
        self.formato_video_combo = QComboBox()
        self.formato_video_combo.addItems(["mp4", "avi", "mkv", "mov"])
        video_layout.addWidget(formato_v_label, 1, 2)
        video_layout.addWidget(self.formato_video_combo, 1, 3)
        
        # Opciones de portada
        self.multiportada_check = QCheckBox("Multiportada (una diferente por beat)")
        video_layout.addWidget(self.multiportada_check, 2, 0, 1, 2)
        
        self.loop_portada_check = QCheckBox("Loop de portada")
        video_layout.addWidget(self.loop_portada_check, 2, 2, 1, 2)
        
        video_group.setLayout(video_layout)
        content_layout.addWidget(video_group)
        
        # GRUPO 3: Fades de Video
        fade_video_group = QGroupBox("Fades de Video")
        fade_video_layout = QGridLayout()
        fade_video_layout.setSpacing(12)
        
        # Fade In Video
        self.fade_in_video_check = QCheckBox("Fade In")
        fade_video_layout.addWidget(self.fade_in_video_check, 0, 0)
        fade_in_dur_label = QLabel("Duración (s):")
        self.fade_in_video_spin = QDoubleSpinBox()
        self.fade_in_video_spin.setMinimum(0)
        self.fade_in_video_spin.setMaximum(10)
        self.fade_in_video_spin.setSingleStep(0.5)
        fade_video_layout.addWidget(fade_in_dur_label, 0, 1)
        fade_video_layout.addWidget(self.fade_in_video_spin, 0, 2)
        
        # Fade Out Video
        self.fade_out_video_check = QCheckBox("Fade Out")
        fade_video_layout.addWidget(self.fade_out_video_check, 1, 0)
        fade_out_dur_label = QLabel("Duración (s):")
        self.fade_out_video_spin = QDoubleSpinBox()
        self.fade_out_video_spin.setMinimum(0)
        self.fade_out_video_spin.setMaximum(10)
        self.fade_out_video_spin.setSingleStep(0.5)
        fade_video_layout.addWidget(fade_out_dur_label, 1, 1)
        fade_video_layout.addWidget(self.fade_out_video_spin, 1, 2)
        
        # Fade Transición Video
        self.fade_trans_video_check = QCheckBox("Fade Transición")
        fade_video_layout.addWidget(self.fade_trans_video_check, 2, 0)
        fade_trans_dur_label = QLabel("Duración (s):")
        self.fade_trans_video_spin = QDoubleSpinBox()
        self.fade_trans_video_spin.setMinimum(0)
        self.fade_trans_video_spin.setMaximum(10)
        self.fade_trans_video_spin.setSingleStep(0.5)
        fade_video_layout.addWidget(fade_trans_dur_label, 2, 1)
        fade_video_layout.addWidget(self.fade_trans_video_spin, 2, 2)
        
        fade_video_group.setLayout(fade_video_layout)
        content_layout.addWidget(fade_video_group)
        
        # GRUPO 4: Audio
        audio_group = QGroupBox("Configuración de Audio")
        audio_layout = QGridLayout()
        audio_layout.setSpacing(12)
        
        # Bitrate Audio
        bitrate_a_label = QLabel("Bitrate Audio:")
        self.bitrate_audio_combo = QComboBox()
        self.bitrate_audio_combo.addItems(["128k", "192k", "256k", "320k"])
        audio_layout.addWidget(bitrate_a_label, 0, 0)
        audio_layout.addWidget(self.bitrate_audio_combo, 0, 1)
        
        # Formato Audio
        formato_a_label = QLabel("Formato:")
        self.formato_audio_combo = QComboBox()
        self.formato_audio_combo.addItems(["aac", "mp3", "opus", "vorbis"])
        audio_layout.addWidget(formato_a_label, 0, 2)
        audio_layout.addWidget(self.formato_audio_combo, 0, 3)
        
        # Ajuste de volumen
        vol_label = QLabel("Ajuste Volumen (dB):")
        self.volumen_spin = QDoubleSpinBox()
        self.volumen_spin.setMinimum(-20)
        self.volumen_spin.setMaximum(20)
        self.volumen_spin.setSingleStep(0.5)
        audio_layout.addWidget(vol_label, 1, 0)
        audio_layout.addWidget(self.volumen_spin, 1, 1)
        
        audio_group.setLayout(audio_layout)
        content_layout.addWidget(audio_group)
        
        # GRUPO 5: Fades de Audio
        fade_audio_group = QGroupBox("Fades de Audio")
        fade_audio_layout = QGridLayout()
        fade_audio_layout.setSpacing(12)
        
        # Fade In Audio
        self.fade_in_audio_check = QCheckBox("Fade In")
        fade_audio_layout.addWidget(self.fade_in_audio_check, 0, 0)
        fade_in_a_dur_label = QLabel("Duración (s):")
        self.fade_in_audio_spin = QDoubleSpinBox()
        self.fade_in_audio_spin.setMinimum(0)
        self.fade_in_audio_spin.setMaximum(10)
        self.fade_in_audio_spin.setSingleStep(0.5)
        fade_audio_layout.addWidget(fade_in_a_dur_label, 0, 1)
        fade_audio_layout.addWidget(self.fade_in_audio_spin, 0, 2)
        
        # Fade Out Audio
        self.fade_out_audio_check = QCheckBox("Fade Out")
        fade_audio_layout.addWidget(self.fade_out_audio_check, 1, 0)
        fade_out_a_dur_label = QLabel("Duración (s):")
        self.fade_out_audio_spin = QDoubleSpinBox()
        self.fade_out_audio_spin.setMinimum(0)
        self.fade_out_audio_spin.setMaximum(10)
        self.fade_out_audio_spin.setSingleStep(0.5)
        fade_audio_layout.addWidget(fade_out_a_dur_label, 1, 1)
        fade_audio_layout.addWidget(self.fade_out_audio_spin, 1, 2)
        
        # Fade Transición Audio
        self.fade_trans_audio_check = QCheckBox("Fade Transición")
        fade_audio_layout.addWidget(self.fade_trans_audio_check, 2, 0)
        fade_trans_a_dur_label = QLabel("Duración (s):")
        self.fade_trans_audio_spin = QDoubleSpinBox()
        self.fade_trans_audio_spin.setMinimum(0)
        self.fade_trans_audio_spin.setMaximum(10)
        self.fade_trans_audio_spin.setSingleStep(0.5)
        fade_audio_layout.addWidget(fade_trans_a_dur_label, 2, 1)
        fade_audio_layout.addWidget(self.fade_trans_audio_spin, 2, 2)
        
        fade_audio_group.setLayout(fade_audio_layout)
        content_layout.addWidget(fade_audio_group)
        
        # GRUPO 6: Auto-borrado y Papelera
        auto_group = QGroupBox("Limpieza Automática")
        auto_layout = QGridLayout()
        auto_layout.setSpacing(12)
        
        # Beats
        beats_label = QLabel("Beats tras convertir:")
        beats_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        beats_label.setStyleSheet("color: #24eaff;")
        auto_layout.addWidget(beats_label, 0, 0, 1, 2)
        
        self.autoborrado_beats_check = QCheckBox("Borrar completamente")
        auto_layout.addWidget(self.autoborrado_beats_check, 1, 0)
        
        self.papelera_beats_check = QCheckBox("Enviar a papelera")
        auto_layout.addWidget(self.papelera_beats_check, 1, 1)
        
        # Portadas
        covers_label = QLabel("Portadas tras convertir:")
        covers_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        covers_label.setStyleSheet("color: #24eaff;")
        auto_layout.addWidget(covers_label, 2, 0, 1, 2)
        
        self.autoborrado_portadas_check = QCheckBox("Borrar completamente")
        auto_layout.addWidget(self.autoborrado_portadas_check, 3, 0)
        
        self.papelera_portadas_check = QCheckBox("Enviar a papelera")
        auto_layout.addWidget(self.papelera_portadas_check, 3, 1)
        
        auto_group.setLayout(auto_layout)
        content_layout.addWidget(auto_group)
        
        # GRUPO 7: Opciones Avanzadas FFMPEG
        advanced_group = QGroupBox("Opciones Avanzadas FFMPEG")
        advanced_layout = QGridLayout()
        advanced_layout.setSpacing(12)
        
        # Codec Video
        codec_label = QLabel("Codec Video:")
        self.codec_combo = QComboBox()
        self.codec_combo.addItems(["libx264", "libx265", "libvpx-vp9", "mpeg4"])
        advanced_layout.addWidget(codec_label, 0, 0)
        advanced_layout.addWidget(self.codec_combo, 0, 1)
        
        # Preset
        preset_label = QLabel("Preset:")
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"])
        advanced_layout.addWidget(preset_label, 0, 2)
        advanced_layout.addWidget(self.preset_combo, 0, 3)
        
        # CRF (Calidad)
        crf_label = QLabel("CRF (Calidad):")
        crf_label.setToolTip("0-51: menor valor = mejor calidad. Recomendado: 18-28")
        self.crf_spin = QSpinBox()
        self.crf_spin.setMinimum(0)
        self.crf_spin.setMaximum(51)
        advanced_layout.addWidget(crf_label, 1, 0)
        advanced_layout.addWidget(self.crf_spin, 1, 1)
        
        # Canales de Audio
        channels_label = QLabel("Canales Audio:")
        self.channels_combo = QComboBox()
        self.channels_combo.addItems(["1 (Mono)", "2 (Estéreo)"])
        advanced_layout.addWidget(channels_label, 1, 2)
        advanced_layout.addWidget(self.channels_combo, 1, 3)
        
        # Sample Rate
        sample_label = QLabel("Sample Rate:")
        self.sample_combo = QComboBox()
        self.sample_combo.addItems(["44100 Hz", "48000 Hz", "96000 Hz"])
        advanced_layout.addWidget(sample_label, 2, 0)
        advanced_layout.addWidget(self.sample_combo, 2, 1)
        
        advanced_group.setLayout(advanced_layout)
        content_layout.addWidget(advanced_group)
        
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_btn)
        
        main_layout.addLayout(buttons_layout)
    
    def _load_values(self):
        """Carga los valores actuales de la configuración"""
        conv = self.config.get("conversion", {})
        
        self.bpv_spin.setValue(conv.get("bpv", 1))
        self.lotes_spin.setValue(conv.get("lotes", 2))
        
        # Video
        res = conv.get("resolucion", "1920x1080")
        idx = self.resolution_combo.findText(res)
        if idx >= 0:
            self.resolution_combo.setCurrentIndex(idx)
        
        self.fps_spin.setValue(conv.get("fps", 30))
        
        bitrate_v = conv.get("bitrate_video", "2M")
        idx = self.bitrate_video_combo.findText(bitrate_v)
        if idx >= 0:
            self.bitrate_video_combo.setCurrentIndex(idx)
        
        formato_v = conv.get("formato_video", "mp4")
        idx = self.formato_video_combo.findText(formato_v)
        if idx >= 0:
            self.formato_video_combo.setCurrentIndex(idx)
        
        self.multiportada_check.setChecked(conv.get("multiportada", False))
        self.loop_portada_check.setChecked(conv.get("loop_portada", True))
        
        # Fades Video
        fade_in_v = conv.get("fade_in_video", {"activo": True, "duracion": 2})
        self.fade_in_video_check.setChecked(fade_in_v.get("activo", True))
        self.fade_in_video_spin.setValue(fade_in_v.get("duracion", 2))
        
        fade_out_v = conv.get("fade_out_video", {"activo": True, "duracion": 2})
        self.fade_out_video_check.setChecked(fade_out_v.get("activo", True))
        self.fade_out_video_spin.setValue(fade_out_v.get("duracion", 2))
        
        fade_trans_v = conv.get("fade_transicion_video", {"activo": True, "duracion": 1})
        self.fade_trans_video_check.setChecked(fade_trans_v.get("activo", True))
        self.fade_trans_video_spin.setValue(fade_trans_v.get("duracion", 1))
        
        # Audio
        bitrate_a = conv.get("bitrate_audio", "192k")
        idx = self.bitrate_audio_combo.findText(bitrate_a)
        if idx >= 0:
            self.bitrate_audio_combo.setCurrentIndex(idx)
        
        formato_a = conv.get("formato_audio", "aac")
        idx = self.formato_audio_combo.findText(formato_a)
        if idx >= 0:
            self.formato_audio_combo.setCurrentIndex(idx)
        
        self.volumen_spin.setValue(conv.get("ajuste_volumen_db", 0.0))
        
        # Fades Audio
        fade_in_a = conv.get("fade_in_audio", {"activo": True, "duracion": 2})
        self.fade_in_audio_check.setChecked(fade_in_a.get("activo", True))
        self.fade_in_audio_spin.setValue(fade_in_a.get("duracion", 2))
        
        fade_out_a = conv.get("fade_out_audio", {"activo": True, "duracion": 2})
        self.fade_out_audio_check.setChecked(fade_out_a.get("activo", True))
        self.fade_out_audio_spin.setValue(fade_out_a.get("duracion", 2))
        
        fade_trans_a = conv.get("fade_transicion_audio", {"activo": False, "duracion": 0})
        self.fade_trans_audio_check.setChecked(fade_trans_a.get("activo", False))
        self.fade_trans_audio_spin.setValue(fade_trans_a.get("duracion", 0))
        
        # Auto-borrado
        self.autoborrado_beats_check.setChecked(conv.get("autoborrado_beats", True))
        self.autoborrado_portadas_check.setChecked(conv.get("autoborrado_portadas", False))
        
        # Papelera
        self.papelera_beats_check.setChecked(conv.get("enviar_beats_papelera", False))
        self.papelera_portadas_check.setChecked(conv.get("enviar_portadas_papelera", False))
        
        # Opciones Avanzadas
        codec = conv.get("codec_video", "libx264")
        idx = self.codec_combo.findText(codec)
        if idx >= 0:
            self.codec_combo.setCurrentIndex(idx)
        
        preset = conv.get("preset", "medium")
        idx = self.preset_combo.findText(preset)
        if idx >= 0:
            self.preset_combo.setCurrentIndex(idx)
        
        self.crf_spin.setValue(conv.get("crf", 23))
        
        channels = conv.get("audio_channels", 2)
        self.channels_combo.setCurrentIndex(0 if channels == 1 else 1)
        
        sample = conv.get("audio_sample_rate", 44100)
        sample_map = {44100: 0, 48000: 1, 96000: 2}
        self.sample_combo.setCurrentIndex(sample_map.get(sample, 0))
    
    def save_settings(self):
        """Guarda la configuración"""
        new_config = {
            "bpv": self.bpv_spin.value(),
            "lotes": self.lotes_spin.value(),
            "resolucion": self.resolution_combo.currentText(),
            "fps": self.fps_spin.value(),
            "bitrate_video": self.bitrate_video_combo.currentText(),
            "formato_video": self.formato_video_combo.currentText(),
            "multiportada": self.multiportada_check.isChecked(),
            "loop_portada": self.loop_portada_check.isChecked(),
            "fade_in_video": {
                "activo": self.fade_in_video_check.isChecked(),
                "duracion": self.fade_in_video_spin.value()
            },
            "fade_out_video": {
                "activo": self.fade_out_video_check.isChecked(),
                "duracion": self.fade_out_video_spin.value()
            },
            "fade_transicion_video": {
                "activo": self.fade_trans_video_check.isChecked(),
                "duracion": self.fade_trans_video_spin.value()
            },
            "bitrate_audio": self.bitrate_audio_combo.currentText(),
            "formato_audio": self.formato_audio_combo.currentText(),
            "ajuste_volumen_db": self.volumen_spin.value(),
            "fade_in_audio": {
                "activo": self.fade_in_audio_check.isChecked(),
                "duracion": self.fade_in_audio_spin.value()
            },
            "fade_out_audio": {
                "activo": self.fade_out_audio_check.isChecked(),
                "duracion": self.fade_out_audio_spin.value()
            },
            "fade_transicion_audio": {
                "activo": self.fade_trans_audio_check.isChecked(),
                "duracion": self.fade_trans_audio_spin.value()
            },
            "autoborrado_beats": self.autoborrado_beats_check.isChecked(),
            "autoborrado_portadas": self.autoborrado_portadas_check.isChecked(),
            "enviar_beats_papelera": self.papelera_beats_check.isChecked(),
            "enviar_portadas_papelera": self.papelera_portadas_check.isChecked(),
            "codec_video": self.codec_combo.currentText(),
            "preset": self.preset_combo.currentText(),
            "crf": self.crf_spin.value(),
            "audio_channels": 1 if self.channels_combo.currentIndex() == 0 else 2,
            "audio_sample_rate": [44100, 48000, 96000][self.sample_combo.currentIndex()],
            "nombre_salida_auto": True
        }
        
        # Actualizar configuración usando el método correcto
        self.config.config["conversion"] = new_config
        self.config.save()
        self.accept()


__all__ = ["FFmpegSettingsDialog"]
