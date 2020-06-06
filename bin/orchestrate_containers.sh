#!/bin/sh

sudo docker-compose build --compress --force-rm --parallel
sudo docker-compose up --detach --remove-orphans
sudo docker-compose logs --follow
