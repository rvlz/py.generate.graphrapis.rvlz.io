build:
	docker-compose build

up:
	docker-compose up -d generator-api

up-test:
	docker-compose up -d generator-test-api

tests: up-test
	docker-compose run --rm --no-deps generator-api python cli.py test

unit-tests: up-test
	docker-compose run --rm --no-deps generator-api python cli.py test --unit

integration-tests: up-test
	docker-compose run --rm --no-deps generator-api python cli.py test --integration

e2e-tests: up-test
	docker-compose run --rm --no-deps generator-api python cli.py test --e2e

down:
	docker-compose down --remove-orphans

all: down build up test

logs-api:
	docker-compose logs -f generator-api

logs-test-api:
	docker-compose logs -f generator-test-api

logs-db:
	docker-compose logs -f generator-db

logs:
	docker-compose logs -f

create-tables:
	docker-compose exec generator-api python cli.py create-tables

create-test-tables:
	docker-compose exec generator-api python cli.py create-tables --test

drop-tables:
	docker-compose exec generator-api python cli.py drop-tables

drop-test-tables:
	docker-compose exec generator-api python cli.py drop-tables --test

postgres-shell:
	docker-compose exec generator-db psql -U docker -d generator_api_dev

format:
	docker-compose exec generator-api black --line-length 79 app cli.py manage.py

lint:
	docker-compose exec generator-api flake8 app cli.py manage.py
 