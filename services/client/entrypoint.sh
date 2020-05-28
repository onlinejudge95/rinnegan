#!/bin/sh

sed -i -e 's/PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf
sed -i -e 's~SERVER_URL_PLACEHOLDER~'"$REACT_APP_SERVER_URL"'~g' /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'
