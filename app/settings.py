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

DISEASES_LIST = {'Chlamydia': 0.03, "HPV": 0.426,
                 'HSV-2': 0.1205}

POPULATION = 1000

TIME_INTERVAL_DAYS = 6000

USER_DAYS_DELAY_BEFORE_USE_SPIN = 2000

DISEASES_DETECT_LIST = {'Chlamydia': [], 'HSV-2': [], 'HPV': []}

DISEASES_LUCK_LIST = {'Chlamydia': 0.83, 'HSV-2': 0.1, 'HPV': 0.08}

DISEASES_LUCK_HEAL_LIST = {'Chlamydia': 0.6, 'HSV-2': 0, 'HPV': 0.25}

DISEASES_DAILY_LUCK_HEAL_LIST = {'Chlamydia': 0.02, 'HSV-2': 0, 'HPV': 0.0015}

UNHEALABLE_DISEASES = ['HSV-2']

VACCINATION = {'HPV': 0.215}

SPIN_USERS = 0.1

DOCTOR_CHECK_TIME_INTERVAL = 1100

REACT_LUCKY = 0.9

COLOR_BY_DISEASE = {
    'HIV': 'blue', 'Chlamydia': 'red', 'HSV-2': 'green', 'Gonorrhea': 'yellow', 'HBV': 'violet',
    'HPV': 'orange'
}
