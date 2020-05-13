FROM python:3.8.2 as builder

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y gcc python3-dev libpq-dev

COPY ./requirements.txt .

COPY ./requirements-dev.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels --requirement requirements.txt

# COPY . .

# RUN pip install --requirement requirements-dev.txt

# RUN black --check --config pyproject.toml . && \
#     flake8 --config setup.cfg . && \
#     isort \
#     --atomic \
#     --case-sensitive \
#     --check-only \
#     --force-alphabetical-sort-within-sections \
#     --lines-after-imports 2 \
#     --lines-between-types 1 \
#     --recursive \
#     --force-single-line-imports \
#     --line-width 79 . && \
#     pytest -c /usr/src/app/app/tests/pytest.ini

FROM python:3.8.2

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir /wheels/*

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
