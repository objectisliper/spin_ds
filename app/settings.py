import os

from .simulation_settings import *

PORT = 8888
DOMAIN = 'localhost'
PROTOCOL = 'http'
STATIC_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/templates'

TORNADO_SETTINGS = {
    "static_path": STATIC_FOLDER,
    "autoreload": True,
    "debug": True,
    "compiled_template_cache": False,
    "static_hash_cache": False,
    "serve_traceback": True,
}


