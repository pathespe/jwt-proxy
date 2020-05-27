
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
	coverage run --source=jwt_proxy -m pytest tests/
	coverage report -m 