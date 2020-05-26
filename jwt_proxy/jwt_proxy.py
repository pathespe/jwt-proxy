# -*- coding: utf-8 -*-
"""jwt_proxy.py docstring

"""

import os
import time
import json
import uuid
from datetime import datetime

import jwt
import requests
from dotenv import load_dotenv
from aiohttp import web


load_dotenv(dotenv_path=".env", verbose=True)


async def handle_status(request):
    """handle status request"""

    request.app["num_requests"] += 1
    body = {
        "uptime" : time.time() - request.app["start_time"],
        "numberRequests" : request.app["num_requests"]
    }
    return web.Response(body=json.dumps(body), headers={"contentType" : "application/json"})


async def create_jwt_header(data):
    """decode body and add claims"""
    data["iat"] = datetime.utcnow()
    data["jti"] = str(uuid.uuid4())
    return jwt.encode(
        data,
        os.environ["SECRET"],
        algorithm="HS512"
    )


async def handle_post(request):
    """
    handles posts made to server checks a body exists and then appends jwt header
    """

    request.app["num_requests"] += 1
    if request.body_exists:

        headers = dict(request.headers)
        headers["x-my-jwt"] = await create_jwt_header(await request.json())

        resp = requests.post(os.environ["SERVER"], headers=headers)
        return web.Response(
            body=resp.content,
            status=resp.status_code,
            headers=resp.headers
        )

    return web.Response(
        body=json.dumps({"message" : "client input error"}),
        status=400
    )
