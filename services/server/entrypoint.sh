#!/bin/sh

create_log_dir() {
    ACCESS_LOG_DIR_PATH="$1"/access
    ERROR_LOG_DIR_PATH="$1"/error
    
    if [ ! -d "$ACCESS_LOG_DIR_PATH" ]; then
        echo "Info: ${ACCESS_LOG_DIR_PATH} does not exists. Creating\n"
        mkdir -p ${ACCESS_LOG_DIR_PATH}
    else
        echo "${ACCESS_LOG_DIR_PATH} exists\n"
    fi
    
    if [ ! -d "$ERROR_LOG_DIR_PATH" ]; then
        echo "Info: ${ERROR_LOG_DIR_PATH} does not exists. Creating\n"
        mkdir -p ${ERROR_LOG_DIR_PATH}
    else
        echo "${ERROR_LOG_DIR_PATH} exists\n"
    fi
}

create_log_dir "/var/log/gunicorn"
create_log_dir "/var/log/server"

if [ $STAGE != "local" ]; then
    flask db upgrade
fi

gunicorn --config /usr/src/app/gunicorn.conf.py manage:app
