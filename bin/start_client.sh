#!/bin/zsh

export REACT_APP_USERS_SERVICE_URL=http://localhost:8000

nvm install 12.16.1

cd ./services/client

npm install

npm start
