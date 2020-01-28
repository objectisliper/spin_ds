from abc import ABC

import tornado.web

from .utils import render_plot
from .settings import STATIC_FOLDER

html, js = render_plot()


class MainView(tornado.web.RequestHandler, ABC):
    def get(self):
        self.render(f'{STATIC_FOLDER}/example_html_template.html', embed_bokeh_html=html)


class PlotJsView(tornado.web.RequestHandler, ABC):
    def get(self):
        self.write(js)