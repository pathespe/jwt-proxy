# -*- coding: utf-8 -*-
"""server.py docstring

"""
import os
import json

import jwt
from dotenv import load_dotenv
from aiohttp import web


load_dotenv(dotenv_path=".env", verbose=True)


async def handle_post(request):
    """handles post requests"""

    data = jwt.decode(
        request.headers["x-my-jwt"],
        os.environ["SECRET"],
        algorithm="HS512",
        options={"require": ["jti", "iat"]}
    )

    return web.Response(body=json.dumps(data), headers={"contentType" : "application/json"})


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.post(r"/{path:\w*}", handle_post)
    ])
    web.run_app(app, port=8001)
