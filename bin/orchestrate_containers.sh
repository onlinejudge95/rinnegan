#!/bin/zsh

docker-compose down
sudo docker-compose up --build --detach
docker-compose logs --follow
