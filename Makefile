.PHONY: check up down build logs migrate seed reset test

check:
	bash scripts/check-project.sh

up: check
	docker compose up -d --build

down:
	docker compose down

build: check
	docker compose build

logs:
	docker compose logs -f

migrate:
	docker compose exec api alembic upgrade head

seed:
	docker compose exec api python -m app.seed

reset:
	docker compose down -v --remove-orphans
	docker compose up -d --build
	docker compose exec api python -m app.seed

test:
	docker compose exec api pytest -q
