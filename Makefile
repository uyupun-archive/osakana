project_name = osakana

network:
	docker network create $(project_name)_network

build:
	cd server && docker compose -p $(project_name) build --no-cache
	cd dashboard && docker compose -p $(project_name) build --no-cache

up:
	cd engine && docker compose -p $(project_name) up -d
	cd server && docker compose -p $(project_name) up -d
	cd server && docker compose -p $(project_name) exec server python -m db.migrations.run 01 up
	cd dashboard && docker compose -p $(project_name) up -d

down:
	cd engine && docker compose -p $(project_name) down

ps:
	@cd engine && docker compose -p $(project_name) ps
