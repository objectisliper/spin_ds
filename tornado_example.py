import tornado.ioloop
import tornado.web
from bokeh.embed import autoload_static, standalone
from bokeh.resources import CDN, INLINE

from bokeh_example import get_figure

port = 8888


def render_plot():

    figure = get_figure()

    js, tag = autoload_static(figure, INLINE, f"http://localhost:{port}/plot.js")

    return tag, js


html, js = render_plot()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('example_html_template.html', embed_bokeh_html=html)


class JsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(js)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/plot.js", JsHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()