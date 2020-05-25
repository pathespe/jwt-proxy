import os
import json
from datetime import datetime

import aiohttp
import jwt
import requests
from dotenv import load_dotenv
from aiohttp import web


load_dotenv(dotenv_path='.env', verbose=True)


async def handle_post(request):
    data = jwt.decode(
        request.headers["x-my-jwt"],
        os.environ["SECRET"],
        algorithm='HS512',
        options={'require': ['jti', 'iat']}
    )

    return web.Response(body=json.dumps(data), headers={"contentType" : "application/json"})


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.post('/{path:\w*}',handle_post)
        ]
    )
    web.run_app(app, port=8001)
