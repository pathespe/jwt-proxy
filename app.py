# -*- coding: utf-8 -*-
"""app.py docstring
entry point for jwt proxy
"""
import time

from dotenv import load_dotenv
from aiohttp import web
from jwt_proxy.jwt_proxy import handle_post, handle_status


load_dotenv(dotenv_path=".env", verbose=True)


def create_app():
    """returns configured app"""
    app = web.Application()
    app["num_requests"] = 0
    app["start_time"] = time.time()
    app.add_routes([
        web.get("/status", handle_status),
        web.post(r"/{path:\w*}", handle_post)
    ])
    return app

if __name__ == "__main__":
    web.run_app(create_app(), port=8000)
