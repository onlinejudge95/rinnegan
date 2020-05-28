#!/bin/zsh

sudo docker-compose build --compress --force-rm --parallel
sudo docker-compose up --detach
docker-compose logs --follow
