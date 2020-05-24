#!/bin/sh

DIR="/var/log/gunicorn"

if [ ! -d "$DIR" ]; then
    echo "Info: ${DIR} does not exists. Creating\n"
    mkdir -p ${DIR}
else
    echo "${DIR} exists\n"
fi

if [ $STAGE != "local" ]; then
    flask db upgrade
fi

gunicorn --config /usr/src/app/gunicorn.conf.py manage:app
