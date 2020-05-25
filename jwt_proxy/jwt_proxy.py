import os
import time
import json
import uuid

from datetime import datetime
import aiohttp
import jwt
import requests
from dotenv import load_dotenv
from aiohttp import web


load_dotenv(dotenv_path='.env', verbose=True)


async def handle_status(request):

    request.app['num_requests'] += 1
    body = {
        "uptime" : time.time() - request.app["start_time"],
        "numberRequests" : request.app['num_requests']
    }
    return web.Response(body=json.dumps(body), headers={"contentType" : "application/json"})


async def read_stream(request):
    empty_bytes = b''
    result = empty_bytes
    while True:
        chunk = await request.content.read(8)
        if chunk == empty_bytes:
            break
        result += chunk
    return result



async def handle_post(request):


    request.app['num_requests'] =+ 1
    if request.body_exists:

        body = await read_stream(request)
        data = json.loads(body.decode("utf-8"))
        data["iat"] = datetime.utcnow()
        data["jti"] = str(uuid.uuid4())
        encoded_jwt = jwt.encode(
            data, 
            os.environ["SECRET"], 
            algorithm='HS512'
        )

        headers = {
            'x-my-jwt' : encoded_jwt
        }
    
        resp = requests.post(os.environ["SERVER"], headers=headers)
        return web.Response(
            body=resp.content,
            status=resp.status_code,
            headers=resp.headers
        )

        # except:
        #     return web.Response(
        #         body=json.dumps({"message" : "client input error"}),
        #         status=400
        #     )


if __name__ == '__main__':
    app = web.Application()
    app["num_requests"] = 0
    app["start_time"] = time.time()
    app.add_routes([
        web.get("/status", handle_status),
        web.post('/{path:\w*}',handle_post)
        ]
    )
    web.run_app(app, port=8000)
