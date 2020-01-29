from random import randint

import numpy as np

# Bokeh libraries
from bokeh.embed import file_html, autoload_static
from bokeh.plotting import figure
from bokeh.resources import INLINE
from numpy import loadtxt

from .settings import PORT, DOMAIN, PROTOCOL


def get_figure():

    daily_disease = loadtxt('app/output.csv', delimiter=',')

    day_num = np.linspace(1, len(daily_disease), len(daily_disease))
    cumulative_words = np.cumsum(daily_disease)

    # Output the visualization directly in the notebook
    # output_server('hover')

    # Create a figure with a datetime type x-axis
    fig = figure(title='My Tutorial Progress',
                 plot_height=720, plot_width=1280,
                 x_axis_label='Day Number', y_axis_label='People with at least one disease',
                 x_minor_ticks=2, y_range=(0, 2000), x_range=(0, 3600),
                 toolbar_location=None)

    # The daily words will be represented as vertical bars (columns)
    fig.vbar(x=day_num, bottom=0, top=daily_disease,
             color='blue', width=0.75,
             legend_label='Daily')

    # The cumulative sum will be a trend line
    fig.line(x=day_num, y=[cumulative_word/1000 for cumulative_word in cumulative_words],
             color='gray', line_width=1,
             legend_label='Cumulative')

    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    return fig


def render_plot():

    fig = get_figure()

    js, tag = autoload_static(fig, INLINE, f"{PROTOCOL}://{DOMAIN}:{PORT}/plot.js")

    return tag, js
