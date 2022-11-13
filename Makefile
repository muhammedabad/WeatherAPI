up:
	@docker-compose up

dup:
	@docker-compose up -d

build:
	@docker-compose build

stop:
	@docker-compose stop

down:
	@docker-compose down

test:
	@docker-compose run --rm web pytest --cov=. --cov-report=xml --cov-report=term-missing

makemigrations:
	@docker-compose run --rm web ./manage.py makemigrations

migrate:
	@docker-compose run --rm web ./manage.py migrate

shell:
	@docker-compose run --rm web ./manage.py shell

createsuperuser:
	@docker-compose run --rm web ./manage.py createsuperuser

logs:
	@docker-compose logs -tf web

ssh_web:
	@docker exec -it weather_api_web_1 /bin/bash

update-packages:
	@docker-compose run --rm web ./update-packages.sh

reset: down build dup
