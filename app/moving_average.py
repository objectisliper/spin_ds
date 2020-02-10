import json

import pandas as pd
from app.simulation_settings import PERCENT_OF_INFECTIONS_BY_DAY_OUTPUT_FILE

with open(f'{PERCENT_OF_INFECTIONS_BY_DAY_OUTPUT_FILE}') as f:
    daily_percent = json.load(f)

print(daily_percent)

df = pd.DataFrame(daily_percent)

print(df['spin_user'])

print(df['spin_user'].expanding(min_periods=4).mean())
