FROM python:3.8.5-alpine as builder

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/app

RUN apk update && \
    apk add --no-cache build-base postgresql-dev libffi-dev

COPY ./Pipfile ./

RUN pip install pipenv==2018.11.26 && \
    pipenv lock --requirements > ./requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels --requirement ./requirements.txt

##############################################################################

FROM python:3.8.5-alpine

WORKDIR /usr/src/app

RUN apk update && \
    apk add --no-cache build-base postgresql-dev libffi-dev && \
    rm -rf /var/cache/apk/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder /usr/src/app/wheels /wheels

RUN pip install --no-cache-dir /wheels/*

COPY . .

RUN chmod +x entrypoint.sh

CMD [ "./entrypoint.sh" ]
