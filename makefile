# HTTP_PORT=8000


build:
	docker-compose build 

run:
	docker-compose up

test:
	pytest tests/

lint:
	pylint jwt_proxy/

coverage:
	coverage run -m pytest tests/
	coverage report -m jwt_proxy/ --source=jwt_proxy/