import argparse

import aiohttp_jinja2
import jinja2
from aiohttp import web

from app.settings import PORT, STATIC_FOLDER
from app.urls import url_list
from app.utils import set_environment


parser = argparse.ArgumentParser(description="aiohttp server example")
parser.add_argument('--path')
parser.add_argument('--port')
parser.add_argument('--live', action='store_true')


def make_app():
    set_environment()
    app = web.Application()

    app.router.add_routes(url_list)

    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(STATIC_FOLDER))

    return app


if __name__ == "__main__":
    app = make_app()
    args = parser.parse_args()

    if args.live:
        web.run_app(app, path=args.path, port=args.port)
    else:
        web.run_app(app, host="127.0.0.1", port=PORT)
