import pytest
from aiohttp import web
from jwt_proxy.jwt_proxy import handle_post

@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    # app.router.add_get('/', previous)
    # app.router.add_post('/', previous)
    return loop.run_until_complete(aiohttp_client(app))

async def test_set_value(cli):
    resp = await cli.post('/', data={'value': 'foo'})
    assert resp.status == 200
    assert await resp.text() == 'thanks for the data'
    assert cli.server.app['value'] == 'foo'

async def test_get_value(cli):
    cli.server.app['value'] = 'bar'
    resp = await cli.get('/')
    assert resp.status == 200
    assert await resp.text() == 'value: bar'