up:
	docker-compose up
build:
	docker-compose build
black:
	poetry run black .
isort:
	poetry run isort ./*