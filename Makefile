build:
	docker-compose build

run:
	docker-compose up -d --remove-orphans --build

stop:
	docker-compose down

logs:
	docker-compose logs -f
