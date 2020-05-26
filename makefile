# HTTP_PORT=8000

build:
	docker-compose build 

run:
	docker-compose up

test:
	pytest 

lint:
	pylint jwt_proxy/
	pylint server/

coverage:
	coverage run -m pytest tests/
	coverage report -m jwt_proxy/ --source=.