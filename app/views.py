from abc import ABC

import tornado.web

from . import simulation_settings
from .utils import render_plot
from .settings import STATIC_FOLDER

html, js = render_plot()


class MainView(tornado.web.RequestHandler, ABC):
    def get(self):
        simulation_settings_vars = {settings_variable: vars(simulation_settings)[settings_variable]
                                   for settings_variable in vars(simulation_settings) if '__' not in settings_variable}
        self.render(f'{STATIC_FOLDER}/example_html_template.html', embed_bokeh_html=html,
                    simulation_settings=simulation_settings_vars)


class PlotJsView(tornado.web.RequestHandler, ABC):
    def get(self):
        self.write(js)
