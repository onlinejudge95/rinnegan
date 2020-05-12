#!/bin/zsh

docker-compose down
sudo chown -R onlinejudge95:onlinejudge95 .
docker-compose up --build --detach
