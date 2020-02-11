from aiohttp import web

from app.views import MainView, SetUpSimulationView, ParametrizedSimulationView

url_list = [
        web.view("/", MainView),
        web.view("/setup", SetUpSimulationView),
        web.view("/parametrized", ParametrizedSimulationView)
    ]