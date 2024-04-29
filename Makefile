APP_NAME = flask-app
DOCKER_COMPOSE_FILE = docker-compose.yml

build:
	docker-compose -f $(DOCKER_COMPOSE_FILE) build
up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d
down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down
test:
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm $(APP_NAME) pytest
run-tests-inside-container:
	docker exec -it $$(docker-compose -f $(DOCKER_COMPOSE_FILE) ps -q $(APP_NAME)) pytest

cycle: down build up run-tests-inside-container
