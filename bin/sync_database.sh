#!/bin/zsh

docker-compose exec server python manage.py flush
docker-compose exec server python manage.py seed
