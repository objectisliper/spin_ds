import json
from random import randint

import numpy as np

# Bokeh libraries
from bokeh.embed import file_html, autoload_static
from bokeh.plotting import figure
from bokeh.resources import INLINE
from numpy import loadtxt

from .settings import PORT, DOMAIN, PROTOCOL, TIME_INTERVAL_DAYS, COLOR_BY_DISEASE


def get_figure():

    with open('app/output.json') as f:
        daily_diseases = json.load(f)

    # Create a figure with a datetime type x-axis
    fig = figure(title='Diseases Progress',
                 plot_height=900, plot_width=1900,
                 x_axis_label='Day Number', y_axis_label='People with at least one disease',
                 x_minor_ticks=2, y_range=(0, 100), x_range=(0, TIME_INTERVAL_DAYS),
                 toolbar_location=None)

    # The cumulative sum will be a trend line
    for disease in daily_diseases:
        fig.line(x=np.linspace(1, len(daily_diseases[disease]), len(daily_diseases[disease])),
                 y=daily_diseases[disease],
                 color=COLOR_BY_DISEASE[(disease.replace(' SPIN USER', '')).replace(' ALL POPULATION', '')],
                 line_width=4 if 'ALL POPULATION' in disease else 2,
                 legend_label=disease,
                 line_dash='dotted' if 'SPIN USER' in disease else 'dashed' if 'ALL POPULATION' in disease else 'solid')

    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    return fig


def render_plot():

    fig = get_figure()

    js, tag = autoload_static(fig, INLINE, f"{PROTOCOL}://{DOMAIN}:{PORT}/plot.js")

    return tag, js
