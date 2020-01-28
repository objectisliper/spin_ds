import tornado.ioloop
import tornado.web

from app.settings import PORT
from app.urls import url_list


def make_app():
    return tornado.web.Application(url_list)


if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
