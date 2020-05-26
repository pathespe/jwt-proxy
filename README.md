# async jwt proxy 

[![Build Status](https://travis-ci.com/pathespe/jwt-proxy.svg?branch=master)](https://travis-ci.com/pathespe/jwt-proxy)

a HTTP proxy that takes a `POST` request and appends a `JSON Web Token` with the following claims:

`iat` - Timestamp of the request as specified by the specification

`jti`- A cryptographic nonce that should be unique

`payload` - A json payload of the structure:`{"user": "username", "date": "todays date"}`

The JWT should be signed with the following hex string secret using the `HS512` alogrithm as in the JWT spec.

Append the JWT as the `x-my-jwt` header to the upstream post request. The upstream post endpoint can be any dummy endpoint. 

## setup

this project runs using docker compose, before building you must create a .env using the template provided and place the secret for signing the tokens there
```
cp template.env .env
# update .env file with secret
```


## build 
builds application to run with docker compose
```
$ make build
```

## run 
jwt proxy binds on port 8000 and upstream server on port 8001
```
$ make run
```

## testing
pytest has been used to test the project
```
$ make test
```

## linting
run linting on files in both apps
```
$ make lint 
```
## useful stuff

testing any post made to the server
```
curl --location --request POST 'http://localhost:8000/' \
--header 'Content-Type: application/json' \
--data-raw '{"user": "joe", "date": "2020-05-25T20:03:16.090206"}'
```

checking status of jwt proxy server
```
curl --location --request GET 'http://localhost:8000/status'
```

## repo structure
 - jwt_proxy/ *the actual app*
    - requirements.txt *dependencies of this application*
    - ./Dockerfile *docker file for the aiohttp application*
 - server/ *the actual app*
    - requirements.txt *dependencies of this application*
    - ./Dockerfile *docker file for the aiohttp application*
 - tests/ *tests using aiohttp test client*
 - .travis.yml *travis CI, runs tests and linting atm*
 - ./docker-compose.yml *docker compose file, contains aiohttp apps*


## further improvements

 - separate out dev dependencies and deploy deps from requirements.txt
 - more tests/integration testing
 - terraform infra to host container
 - more docs, swagger etc.