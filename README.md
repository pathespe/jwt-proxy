# async jwt proxy server

[![Build Status](https://travis-ci.com/pathespe/async-proxy-server.svg?branch=master)](https://travis-ci.com/pathespe/async-proxy-server)

a HTTP proxy that takes a `POST` request and appends a `JSON Web Token` with the following claims:

`iat` - Timestamp of the request as specified by the specification

`jti`- A cryptographic nonce that should be unique

`payload` - A json payload of the structure:`{"user": "username", "date": "todays date"}`

The JWT should be signed with the following hex string secret using the `HS512` alogrithm as in the JWT spec.

Append the JWT as the `x-my-jwt` header to the upstream post request.The upstream post endpoint can be any dummy endpoint. 

## assumptions


## repo structure
 - proxy_server/ *the actual app*
    - requirements.txt *dependencies of this application*
 - tests/ *tests using aiohttp test client*
 - .travis.yml *travis CI, runs tests and linting atm*
 - ./docker-compose.yml *docker compose file, contains flask app and a redis container for caching*
 - ./Dockerfile *docker file for the flask application*


## build and run docker container

```
$ make build
```

## testing
run pytest from root directory, it will discover tests in tests/
```
$ make test
```

## linting
run linting on files in proxy_server app
```
$ make lint 
```

## further improvements

 - separate out dev dependencies and deploy deps from requirements.txt
 - more tests/integration testing
 - terraform infra to host container
 - more docs, sphinx, swagger etc.