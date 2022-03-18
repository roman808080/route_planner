.PHONY: up down test build

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

test:
	docker-compose run --rm api pytest -v /tests

