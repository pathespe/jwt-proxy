import json
import time

from aiohttp import web
from aiohttp.test_utils import make_mocked_request
import pytest

from jwt_proxy.jwt_proxy import handle_post, handle_status, create_jwt_header


def handler(request):
    assert request.headers.get('token') == 'x'
    return web.Response(body=b'data')


async def previous(request):
    if request.method == 'POST':
        request.app['value'] = (await request.post())['value']
        return web.Response(body=b'thanks for the data')
    return web.Response(
        body='value: {}'.format(request.app['value']).encode('utf-8'))


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app["num_requests"] = 0
    app["start_time"] = time.time()
    app.router.add_get('/status', handle_status)
    app.router.add_post('/', handle_post)
    return loop.run_until_complete(aiohttp_client(app))


async def test_set_value(cli):
    resp = await cli.post('/', data={"user": "joe", "date": "2020-05-25T20:03:16.090206"})
    assert resp.status == 200


async def test_get_value(cli):
    cli.server.app['num_requests'] = 0
    resp = await cli.get('/status')
    assert resp.status == 200
    resp_obj = json.loads(await resp.text())
    assert  resp_obj["num_requests"] == 1


def test_handler():
    req = make_mocked_request('GET', '/', headers={'x-my-jwt' : create_jwt_header(content)})
    resp = handler(req)
    assert resp.body == b'data'
