import os

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

DISEASES_LIST = {'Chlamydia': 0.01355, 'Gonorrhea': 0.00365, 'HBV': 0.01, 'HCV': 0.01, 'HIV': 0.0033,
                 'HSV-2': 0.19615, 'Mycoplasma genitalium': 0.01, 'Public lice': 0.004,
                 'Scabies': 0.003, 'Syphilis': 0.00005121004, 'Trichomoniasis': 0.00510}

POPULATION = 1000

TIME_INTERVAL_DAYS = 3652
