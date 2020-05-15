FROM python:3.8.2-slim as builder

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y gcc python3-dev libpq-dev

COPY ./requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels --requirement requirements.txt

##############################################################################

FROM python:3.8.2-slim

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y python3-dev libpq-dev && \
    apt-get autoremove

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir /wheels/*

COPY . .

RUN chmod +x entrypoint.sh

CMD [ "./entrypoint.sh" ]
