"""
Legacy compatibility module - core.core wrapper

Este módulo mantiene compatibilidad con el código legacy que usa core.core
"""
import os
import json
from PyQt6.QtCore import QObject, pyqtSignal
from ecb_tool.core.paths import get_paths

# Get paths
paths = get_paths()


class StateManager(QObject):
    """
    Gestor de estado de la aplicación
    Mantiene el modo actual y beats por video
    """
    mode_changed = pyqtSignal(str)
    bpv_changed = pyqtSignal(int)
    action_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._mode = "Convert"
        self._bpv = 1

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value in ["Convert", "Upload", "Alternate", "Simultaneous"]:
            self._mode = value
            self.mode_changed.emit(value)

    @property
    def bpv(self):
        return self._bpv

    @bpv.setter
    def bpv(self, value):
        if 1 <= value <= 10:
            self._bpv = value
            self.bpv_changed.emit(value)

    def request_action(self, action: str):
        self.action_requested.emit(action)


def load_order():
    """Carga el archivo de orden"""
    try:
        if paths.order_config.exists():
            with open(paths.order_config, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def check_stop_flag():
    """Verifica si existe el flag de parar"""
    return paths.stop_flag.exists()


def clear_stop_flag():
    """Limpia el flag de parar"""
    if paths.stop_flag.exists():
        paths.stop_flag.unlink()


def create_stop_flag():
    """Crea el flag de parar"""
    paths.stop_flag.parent.mkdir(parents=True, exist_ok=True)
    paths.stop_flag.write_text("STOP")


def update_process_state(active: bool):
    """Actualiza el estado del proceso en orden.json"""
    data = load_order()
    data["proceso"] = active
    
    paths.order_config.parent.mkdir(parents=True, exist_ok=True)
    with open(paths.order_config, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def _log_core(message: str):
    """Log interno"""
    try:
        paths.app_log.parent.mkdir(parents=True, exist_ok=True)
        with open(paths.app_log, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    except Exception:
        pass


# Log module load
_log_core("ecb_tool.core.legacy loaded")
