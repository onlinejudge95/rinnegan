FROM node:14.3.0-alpine AS build-client

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/app

ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY ./services/client/package*.json ./

RUN npm ci

RUN npm install react-scripts@3.4.0

COPY ./services/client .

RUN npm run build

##############################################################################

FROM python:3.8.3-alpine as build-server

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/app

RUN apk update && \
    apk add --no-cache build-base=0.5-r1 postgresql-dev=12.2-r0 libffi-dev=3.2.1-r6

COPY ./services/server/Pipfile ./

RUN pip install pipenv==2018.11.26 && \
    pipenv lock --requirements > ./requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels --requirement ./requirements.txt

# ##############################################################################

FROM nginx:stable-alpine as production

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/app

RUN apk update && \
    apk add --no-cache openssl-dev=1.1.1g-r0 libffi-dev=3.2.1-r6 gcc=9.2.0-r4 python3-dev=3.8.2-r0 musl-dev=1.1.24-r2 \
    postgresql-dev=12.2-r0 netcat-openbsd=1.130-r1

RUN python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

COPY --from=build-client /usr/src/app/build /usr/share/nginx/html
COPY --from=build-server /usr/src/app/wheels /wheels
COPY ./services/nginx/default.conf /etc/nginx/conf.d/default.conf

RUN pip install --no-cache-dir /wheels/*

COPY ./services/server .

RUN chmod +x entrypoint.sh

CMD ./entrypoint.sh && \
    sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
    nginx -g 'daemon off;'
