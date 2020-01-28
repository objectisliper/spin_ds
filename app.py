import tornado.ioloop
import tornado.web

from app.settings import PORT, TORNADO_SETTINGS
from app.urls import url_list


def make_app():
    return tornado.web.Application(url_list, **TORNADO_SETTINGS)


if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
