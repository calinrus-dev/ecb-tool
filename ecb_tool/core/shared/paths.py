"""Legacy paths - compatibility exports"""
from ecb_tool.core.paths import get_paths
_p = get_paths()
ROOT_DIR = str(_p.root)
CONFIG_DIR = str(_p.config)
DATA_DIR = str(_p.data)
VIDEOS_DIR = str(_p.videos)
ORDER_PATH = str(_p.order_config)
CONVERSION_STATE_CSV = str(_p.conversion_state)
UPLOAD_STATE_CSV = str(_p.upload_state)
ROUTES_CONFIG_PATH = str(_p.routes_config)
PARAR_PATH = str(_p.stop_flag)
