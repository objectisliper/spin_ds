import aiohttp_jinja2
import jinja2
from aiohttp import web

from app.settings import PORT, STATIC_FOLDER
from app.urls import url_list
from app.utils import set_environment


def make_app():
    set_environment()
    app = web.Application()

    app.router.add_routes(url_list)

    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(STATIC_FOLDER))

    return app


if __name__ == "__main__":
    app = make_app()
    web.run_app(app, host="127.0.0.1", port=PORT)
