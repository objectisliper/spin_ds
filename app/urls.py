from app.views import MainView, PlotJsView

url_list = [
        (r"/", MainView),
        (r"/plot.js", PlotJsView)
    ]
