import json
import os
from random import randint, random
from functools import lru_cache

import numpy as np

import pandas as pd

# Bokeh libraries
from bokeh.embed import file_html, autoload_static
from bokeh.layouts import column
from bokeh.models import Span, Scale, FixedTicker
from bokeh.plotting import figure
from bokeh.resources import INLINE
from numpy import loadtxt

from . import simulation_settings
from .settings import PORT, DOMAIN, PROTOCOL


def decision(probability: float) -> bool:
    return random() < probability


def get_total_infected_people_figure(daily_diseases):

    # Create a figure with a datetime type x-axis
    fig = figure(title='Diseases Progress',
                 plot_height=900, plot_width=1800,
                 x_axis_label='Day Number', y_axis_label='People with at least one disease',
                 x_minor_ticks=5, y_range=(0, 100), x_range=(0, get_setting('TIME_INTERVAL_DAYS')), y_minor_ticks=5,
                 y_scale=Scale(),
                 toolbar_location=None)

    fig.yaxis.ticker = FixedTicker(ticks=[i for i in range(0, 101, 5)], minor_ticks=[i for i in range(0, 101, 1)])

    # The cumulative sum will be a trend line
    for disease in daily_diseases:
        fig.line(x=np.linspace(1, len(daily_diseases[disease]), len(daily_diseases[disease])),
                 y=daily_diseases[disease],
                 color=get_setting('COLOR_BY_DISEASE')[disease.replace(' SPIN USER', '').replace(' ALL POPULATION', '').replace(' SIMPLE USER', '')],
                 line_width=4 if 'ALL POPULATION' in disease else 2,
                 legend_label=disease,
                 line_dash='dotted' if 'SPIN USER' in disease else 'dashed' if 'ALL POPULATION' in disease else 'solid')

    vline = Span(location=get_setting('USER_DAYS_DELAY_BEFORE_USE_SPIN'), dimension='height', line_color='black', line_width=3)
    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    fig.renderers.extend([vline])

    return fig


def get_percent_of_infections_by_day_figure(daily_percent):

    # Create a figure with a datetime type x-axis
    fig = figure(title='Percent of infections by day',
                 plot_height=900, plot_width=1800,
                 x_axis_label='Day Number', y_axis_label='Percent of infections via connection',
                 x_minor_ticks=5, y_range=(0, 2), x_range=(0, get_setting('TIME_INTERVAL_DAYS')), y_minor_ticks=5,
                 y_scale=Scale(),
                 toolbar_location=None)

    fig.yaxis.ticker = FixedTicker(ticks=[i for i in range(0, 3, 1)], minor_ticks=[i/10 for i in range(0, 30, 1)])

    df_simple = pd.DataFrame(daily_percent['simple_user'])

    df_spin = pd.DataFrame(daily_percent['spin_user'])

    # The cumulative sum will be a trend line
    for disease in get_setting('DISEASES_DETECT_LIST'):
        fig.line(x=np.linspace(1, len(daily_percent['simple_user'][disease]),
                               len(daily_percent['simple_user'][disease])),
                 y=df_simple[disease].expanding(min_periods=4).mean(),
                 color=get_setting('COLOR_BY_DISEASE')[disease],
                 line_width=2,
                 legend_label=f'Simple user {disease}',
                 line_dash='solid')

        fig.line(x=np.linspace(1, len(daily_percent['spin_user'][disease]), len(daily_percent['spin_user'][disease])),
                 y=df_spin[disease].expanding(min_periods=4).mean(),
                 color=get_setting('COLOR_BY_DISEASE')[disease],
                 line_width=2,
                 legend_label=f'Spin user {disease}',
                 line_dash='dotted')

    vline = Span(location=get_setting('USER_DAYS_DELAY_BEFORE_USE_SPIN'), dimension='height', line_color='black', line_width=3)
    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    fig.renderers.extend([vline])

    return fig


def get_total_infected_people_by_spin_user_percent_figure():

    with open(f'app/{get_setting("SPIN_INFLUENCE_OUTPUT_FILE")}') as f:
        infected_percent = json.load(f)

    # Create a figure with a datetime type x-axis
    fig = figure(title='Percent of infections by percent of spin  user',
                 plot_height=900, plot_width=1800,
                 x_axis_label='Percent of infections', y_axis_label='Percent of spin user',
                 x_minor_ticks=5, y_range=(0, 100), x_range=(0, 51), y_minor_ticks=5,
                 y_scale=Scale(),
                 toolbar_location=None)

    fig.yaxis.ticker = FixedTicker(ticks=[i for i in range(0, 101, 5)], minor_ticks=[i for i in range(0, 101, 1)])

    # The cumulative sum will be a trend line
    for disease in infected_percent:
        fig.line(x=np.linspace(0, len(infected_percent[disease]), len(infected_percent[disease])),
                 y=infected_percent[disease],
                 color=get_setting('COLOR_BY_DISEASE')[disease],
                 line_width=2,
                 legend_label=disease,
                 line_dash='solid')

    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    return fig


def render_plot():

    with open(f'app/{get_setting("TOTAL_INFECTED_PEOPLE_OUTPUT_FILE")}') as f:
        daily_diseases = json.load(f)

    with open(f'app/{get_setting("PERCENT_OF_INFECTIONS_BY_DAY_OUTPUT_FILE")}') as f:
        daily_percent = json.load(f)

    fig = column(get_total_infected_people_figure(daily_diseases), get_percent_of_infections_by_day_figure(daily_percent),
                 get_total_infected_people_by_spin_user_percent_figure())

    js, tag = autoload_static(fig, INLINE, f"{PROTOCOL}://{DOMAIN}:{PORT}/plot.js")

    return tag, js


def live_render_plot(daily_diseases, daily_percent):
    def remap_keys(mapping):
        return {" ".join(k): v for k, v in mapping.items()}

    fig = column(get_total_infected_people_figure(remap_keys(daily_diseases)),
                 get_percent_of_infections_by_day_figure(daily_percent))

    js, tag = autoload_static(fig, INLINE, f"{PROTOCOL}://{DOMAIN}:{PORT}/plot.js")

    return tag, js


def set_environment():
    simulation_settings_vars = {settings_variable: vars(simulation_settings)[settings_variable]
                                for settings_variable in vars(simulation_settings) if '__' not in settings_variable}
    for setting in simulation_settings_vars:
        os.environ[setting] = json.dumps(simulation_settings_vars[setting])


def set_simulation_setting(key, value):
    os.environ[key] = json.dumps(value)


@lru_cache(maxsize=32)
def get_setting(key):
    try:
        return json.loads(os.getenv(key, None))
    except TypeError:
        raise ValueError('Wrong setting key was given')
