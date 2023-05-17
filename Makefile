network:
	docker network create osakana_network

build:
	cd server && docker compose -p osakana build --no-cache
	cd dashboard && docker compose -p osakana build --no-cache

up:
	cd engine && docker compose -p osakana up -d
	cd server && docker compose -p osakana up -d
	cd dashboard && docker compose -p osakana up -d

down:
	cd engine && docker compose -p osakana down
	cd server && docker compose -p osakana down
	cd dashboard && docker compose -p osakana down

ps:
	@cd engine && docker compose -p osakana ps
