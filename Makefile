build:
	DOCKER_BUILDKIT=1 docker-compose build

run:
	DOCKER_BUILDKIT=1 docker-compose up -d --remove-orphans --build

stop:
	docker-compose down
	
bash_server:
	docker-compose exec server bash

clean:
	docker-compose down -v --rmi all --remove-orphans

logs:
	docker-compose logs -f
	
server:
	DOCKER_BUILDKIT=1 docker-compose up -d --remove-orphans --build server

db:
	docker-compose exec server python ./db.py -e chromaprint -c && docker-compose exec server python ./db.py -e mfcc
