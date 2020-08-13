FROM node:14.8.0-alpine as builder

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/builder

ENV PATH /usr/src/builder/node_modules/.bin:$PATH

COPY package*.json ./

RUN npm install -g react-scripts@3.4.1 && \
    npm install

COPY . .

# RUN npm run build

# RUN npm run prettier:check && \
#     npm run lint

############################################################################

# FROM nginx:stable-alpine

# LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

# WORKDIR /usr/src/app

# COPY --from=builder /usr/src/builder/build /usr/share/nginx/html
# COPY --from=builder /usr/src/builder/nginx.conf /etc/nginx/conf.d/default.conf
# COPY --from=builder /usr/src/builder/entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
