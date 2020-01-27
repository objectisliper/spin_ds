from random import randint

import numpy as np

# Bokeh libraries
from bokeh.embed import file_html
from bokeh.plotting import figure


def get_figure():
    ITERATION_NUMBER = 3600
    MIN_VALUE = 200
    MAX_VALUE = 600

    daily_words = []
    # My word count data
    for i in range(ITERATION_NUMBER):
        daily_words.append(randint(MIN_VALUE, MAX_VALUE))
    day_num = np.linspace(1, ITERATION_NUMBER, ITERATION_NUMBER)
    cumulative_words = np.cumsum(daily_words)

    # Output the visualization directly in the notebook
    # output_server('hover')

    # Create a figure with a datetime type x-axis
    fig = figure(title='My Tutorial Progress',
                 plot_height=720, plot_width=1280,
                 x_axis_label='Day Number', y_axis_label='Words Written',
                 x_minor_ticks=2, y_range=(0, 6000), x_range=(0, 1200),
                 toolbar_location=None)

    # The daily words will be represented as vertical bars (columns)
    fig.vbar(x=day_num, bottom=0, top=daily_words,
             color='blue', width=0.75,
             legend_label='Daily')

    # The cumulative sum will be a trend line
    fig.line(x=day_num, y=cumulative_words,
             color='gray', line_width=1,
             legend_label='Cumulative')

    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    return fig



