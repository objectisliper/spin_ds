from abc import ABC

import tornado.web

from . import simulation_settings
from .utils import render_plot
from .settings import STATIC_FOLDER, DISEASES_LIST, UNHEALABLE_DISEASES


class MainView(tornado.web.RequestHandler, ABC):
    def get(self):
        html, js = render_plot()
        simulation_settings_vars = {settings_variable: vars(simulation_settings)[settings_variable]
                                    for settings_variable in vars(simulation_settings) if '__' not in settings_variable}
        self.render(f'{STATIC_FOLDER}/example_html_template.html', embed_bokeh_html=html,
                    simulation_settings=simulation_settings_vars, embed_js=js)


class SetUpSimulationView(tornado.web.RequestHandler, ABC):
    def get(self):
        diseases = [disease for disease in DISEASES_LIST]
        self.render(f'{STATIC_FOLDER}/set_up_simulation_template.html', diseases=diseases,
                    diseases_prevalence=DISEASES_LIST, unhelable_diseases=UNHEALABLE_DISEASES)


class ParametrizedSimulationView(tornado.web.RequestHandler, ABC):
    def get(self):
        # self.get_query_argument('DISEASES_LIST')
        pass
