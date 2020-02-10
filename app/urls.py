from app.views import MainView, SetUpSimulationView, ParametrizedSimulationView

url_list = [
        (r"/", MainView),
        (r"/setup", SetUpSimulationView),
        (r"/parametrized", ParametrizedSimulationView)
    ]
