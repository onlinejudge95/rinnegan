#!/bin/sh

gunicorn --config /usr/src/app/gunicorn.conf.py manage:app && \
sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
nginx -g 'daemon off;'
