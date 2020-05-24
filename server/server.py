import json
import aiohttp
from aiohttp import web


async def handle_post(request):
    
    return web.Response(body=json.dumps({"ayo": "a"}), headers={"contentType" : "application/json"})


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.post('/{path:\w*}',handle_post)
        ]
    )
    web.run_app(app, port=8001)
