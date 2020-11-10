install:
	cp -n .env.example .env
	docker-compose run --rm backend sh -c "sleep 5 && python manage.py migrate"

test:
	docker-compose run --rm backend sh -c "sleep 5 && python manage.py test"

start:
	docker-compose up -d