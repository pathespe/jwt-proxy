import os
import json
import time

from aiohttp import web
from aiohttp.test_utils import make_mocked_request
import jwt
import pytest
from dotenv import load_dotenv


from app import create_app
from jwt_proxy.jwt_proxy import (
    handle_post, 
    handle_status, 
    create_jwt_header
)


load_dotenv("../.env")


@pytest.fixture
def cli(loop, aiohttp_client):
    app = create_app()
    return loop.run_until_complete(aiohttp_client(app))


async def test_set_value(cli):
    resp = await cli.post("/")
    assert resp.status == 400
    resp = await cli.post("/")
    assert resp.status == 400


async def test_get_value(cli):

    cli.server.app["num_requests"] = 0

    resp = await cli.get("/status")
    assert resp.status == 200
    resp_obj = json.loads(await resp.text())
    assert  resp_obj["numberRequests"] == 1

    resp = await cli.get("/status")
    assert resp.status == 200
    resp_obj = json.loads(await resp.text())
    assert  resp_obj["numberRequests"] == 2

    cli.server.app["num_requests"] = 0

    resp = await cli.get("/status")
    assert resp.status == 200
    resp_obj = json.loads(await resp.text())
    assert  resp_obj["numberRequests"] == 1


async def test_jwt_creation():

    content = {"user": "joe", "date": "2020-05-25T20:03:16.090206"}
    jwtoken = await create_jwt_header(content)
    data = jwt.decode(
        jwtoken,
        os.environ["SECRET"],
        algorithm="HS512",
        options={"require": ["jti", "iat"]}
    )
    assert len(data.keys()) == 4
    assert "jti" in data.keys()
    assert "iat" in data.keys()
    assert data["user"] == "joe"
    assert data["date"] == "2020-05-25T20:03:16.090206"
