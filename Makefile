WORKERS := 3

all: up submit

all-build: up-build submit

submit:
	docker compose exec spark-master ./submit.sh

up:
	docker compose up --detach --remove-orphans --scale spark-worker=$(WORKERS)

up-build:
	docker compose up --detach --remove-orphans --scale spark-worker=$(WORKERS) --build

down:
	docker compose down

re: down up

re-build: down up-build

build:
	docker compose build