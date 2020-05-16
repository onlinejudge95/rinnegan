FROM python:3.8.2-alpine as builder

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/app

RUN apk update && \
    apk add --no-cache build-base postgresql-dev

COPY ./requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels --requirement requirements.txt

##############################################################################

FROM python:3.8.2-alpine

WORKDIR /usr/src/app

RUN apk update && \
    apk add --no-cache build-base postgresql-dev libffi-dev && \
    rm -rf /var/cache/apk/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir /wheels/*

COPY . .

RUN chmod +x entrypoint.sh

CMD [ "./entrypoint.sh" ]
