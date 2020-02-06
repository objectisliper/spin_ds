import json
from random import randint, random

import numpy as np

# Bokeh libraries
from bokeh.embed import file_html, autoload_static
from bokeh.layouts import column
from bokeh.models import Span, Scale, FixedTicker
from bokeh.plotting import figure
from bokeh.resources import INLINE
from numpy import loadtxt

from .settings import PORT, DOMAIN, PROTOCOL, TIME_INTERVAL_DAYS, COLOR_BY_DISEASE, USER_DAYS_DELAY_BEFORE_USE_SPIN, \
    TOTAL_INFECTED_PEOPLE_OUTPUT_FILE, PERCENT_OF_INFECTIONS_BY_DAY_OUTPUT_FILE, COLOR_BY_USER_TYPE


def decision(probability: float) -> bool:
    return random() < probability


def get_total_infected_people_figure():

    with open(f'app/{TOTAL_INFECTED_PEOPLE_OUTPUT_FILE}') as f:
        daily_diseases = json.load(f)

    # Create a figure with a datetime type x-axis
    fig = figure(title='Diseases Progress',
                 plot_height=900, plot_width=1800,
                 x_axis_label='Day Number', y_axis_label='People with at least one disease',
                 x_minor_ticks=5, y_range=(0, 100), x_range=(0, TIME_INTERVAL_DAYS), y_minor_ticks=5,
                 y_scale=Scale(),
                 toolbar_location=None)

    fig.yaxis.ticker = FixedTicker(ticks=[i for i in range(0, 101, 5)], minor_ticks=[i for i in range(0, 101, 1)])

    # The cumulative sum will be a trend line
    for disease in daily_diseases:
        fig.line(x=np.linspace(1, len(daily_diseases[disease]), len(daily_diseases[disease])),
                 y=daily_diseases[disease],
                 color=COLOR_BY_DISEASE[((disease.replace(' SPIN USER', '')).replace(' ALL POPULATION', '')).replace(' SIMPLE USER', '')],
                 line_width=4 if 'ALL POPULATION' in disease else 2,
                 legend_label=disease,
                 line_dash='dotted' if 'SPIN USER' in disease else 'dashed' if 'ALL POPULATION' in disease else 'solid')

    vline = Span(location=USER_DAYS_DELAY_BEFORE_USE_SPIN, dimension='height', line_color='black', line_width=3)
    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    fig.renderers.extend([vline])

    return fig


def get_percent_of_infections_by_day_figure():

    with open(f'app/{PERCENT_OF_INFECTIONS_BY_DAY_OUTPUT_FILE}') as f:
        daily_percent = json.load(f)

    # Create a figure with a datetime type x-axis
    fig = figure(title='Percent of infections by day',
                 plot_height=900, plot_width=1800,
                 x_axis_label='Day Number', y_axis_label='Percent of infections via connection',
                 x_minor_ticks=5, y_range=(0, 5), x_range=(0, TIME_INTERVAL_DAYS), y_minor_ticks=5,
                 y_scale=Scale(),
                 toolbar_location=None)

    fig.yaxis.ticker = FixedTicker(ticks=[i for i in range(0, 6, 1)], minor_ticks=[i/10 for i in range(0, 60, 1)])

    # The cumulative sum will be a trend line
    for user_type in daily_percent:
        fig.line(x=np.linspace(1, len(daily_percent[user_type]), len(daily_percent[user_type])),
                 y=daily_percent[user_type],
                 color=COLOR_BY_USER_TYPE[user_type],
                 line_width=2,
                 legend_label=user_type.upper(),
                 line_dash='solid')

    vline = Span(location=USER_DAYS_DELAY_BEFORE_USE_SPIN, dimension='height', line_color='black', line_width=3)
    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    fig.renderers.extend([vline])

    return fig


def render_plot():

    fig = column(get_total_infected_people_figure(), get_percent_of_infections_by_day_figure())

    js, tag = autoload_static(fig, INLINE, f"{PROTOCOL}://{DOMAIN}:{PORT}/plot.js")

    return tag, js
