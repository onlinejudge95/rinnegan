FROM node:14.2.0-alpine

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/app

ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY package*.json ./

RUN npm ci

RUN npm install react-scripts@3.4.0

COPY . .

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
