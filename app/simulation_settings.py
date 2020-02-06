DISEASES_LIST = {'Chlamydia': 0.03, "HPV": 0.426,
                 'HSV-2': 0.1205}

POPULATION = 300000

TIME_INTERVAL_DAYS = 6000

USER_DAYS_DELAY_BEFORE_USE_SPIN = 2000

DISEASES_DETECT_LIST = {'Chlamydia': [], 'HSV-2': [], 'HPV': []}

DISEASES_LUCK_LIST = {'Chlamydia': 0.83, 'HSV-2': 0.1, 'HPV': 0.08}

DISEASES_LUCK_HEAL_LIST = {'Chlamydia': 0.6, 'HSV-2': 0, 'HPV': 0.25}

DISEASES_DAILY_LUCK_HEAL_LIST = {'Chlamydia': 0.02, 'HSV-2': 0, 'HPV': 0.0015}

UNHEALABLE_DISEASES = ['HSV-2']

VACCINATION = {'HPV': 0.215}

SPIN_USERS = 0.1

REACT_LUCKY = 0.9

NEW_PEOPLE_DAY_LUCK = 1, 1

EXIT_PEOPLE_DAY_LUCK = 1, 1

TOTAL_INFECTED_PEOPLE_OUTPUT_FILE = 'output.json'

PERCENT_OF_INFECTIONS_BY_DAY_OUTPUT_FILE = 'output2.json'

SPIN_USER_CONNECT_SIMPLE_USER_LUCK = 0.9

COLOR_BY_DISEASE = {
    'HIV': 'blue', 'Chlamydia': 'red', 'HSV-2': 'green', 'Gonorrhea': 'yellow', 'HBV': 'violet',
    'HPV': 'orange'
}

COLOR_BY_USER_TYPE = {
    'spin_user': 'red', 'simple_user': 'orange'
}
