#!/bin/zsh

sudo docker-compose up --build --detach
docker-compose logs --follow
