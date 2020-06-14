#!/bin/zsh

MIGRATIONS_DIR=`pwd`/services/server/migrations
MIGRATION_MESSAGE=$1
REVISION_ID=$2

ls -la $MIGRATIONS_DIR | grep -i version

if [ $? != 0 ]; then
    docker-compose exec server flask db init
fi

docker-compose exec server flask db migrate --message $MIGRATION_MESSAGE --rev-id $REVISION_ID
docker-compose exec server flask db upgrade
