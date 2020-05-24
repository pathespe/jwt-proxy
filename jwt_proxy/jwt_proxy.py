import os
import time
import json
from pathlib import Path
import aiohttp
from aiohttp import web
from dotenv import load_dotenv
import jwt
import requests



env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

num_requests = 0
start_time = time.time()


print(os.getenv("SECRET"))


async def handle_status(request):

    body = {
        "uptime" : time.time() - start_time,
        "numberRequests" : num_requests
    }
    return web.Response(body=json.dumps(body), headers={"contentType" : "application/json"})


async def handle_post(request):

    if request.body_exists:

        empty_bytes = b''
        result = empty_bytes
        while True:
            chunk = await request.content.read(8)
            if chunk == empty_bytes:
                break
            result += chunk

        encoded_jwt = jwt.encode(
            json.loads(result.decode("utf-8")), 
            os.environ["SECRET"], 
            algorithm='HS512'
        )

        headers = {
            'x-my-jwt' : encoded_jwt
        }


        resp = requests.post("http://server:8001", data=result, headers=headers)
        print(resp.content, resp.status_code)
        return web.Response(
            body=resp.content,
            status=resp.status_code,
            # content_type=resp.content_type,
            headers=resp.headers
        )


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.get("/status", handle_status),
        web.post('/{path:\w*}',handle_post)
        ]
    )
    web.run_app(app, port=8000)
