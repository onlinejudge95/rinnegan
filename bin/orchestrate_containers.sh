#!/bin/zsh

docker-compose down
sudo chown -R $USER:$USER .
docker-compose up --build --detach
