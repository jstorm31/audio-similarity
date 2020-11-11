build:
	DOCKER_BUILDKIT=1 docker-compose build

run:
	DOCKER_BUILDKIT=1 docker-compose up -d --remove-orphans --build

stop:
	docker-compose down

clean:
	docker-compose down -v --rmi all --remove-orphans

logs:
	docker-compose logs -f

db:
	docker-compose exec server python ./db.py
