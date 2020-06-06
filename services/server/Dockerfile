FROM python:3.8.3-alpine as builder

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/app

RUN apk update && \
    apk add --no-cache build-base postgresql-dev libffi-dev

COPY ./Pipfile ./

RUN pip install pipenv==2018.11.26 && \
    pipenv lock --requirements > ./requirements.txt && \
    pipenv lock --dev --requirements > ./requirements-dev.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels --requirement ./requirements.txt && \
    pip install --requirement requirements-dev.txt

COPY . .

RUN black --check --config /usr/src/app/pyproject.toml /usr/src/app && \
    flake8 --config /usr/src/app/setup.cfg /usr/src/app && \
    isort --atomic --case-sensitive --check-only --force-alphabetical-sort-within-sections --force-single-line-imports --lines-after-imports 2 --lines-between-types 1 --line-width 79 --recursive --skip-glob "migrations/*" /usr/src/app

##############################################################################

FROM python:3.8.3-alpine

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
