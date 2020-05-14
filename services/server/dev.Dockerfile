FROM python:3.8.2-slim

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/app

COPY ./requirements.txt .

COPY ./requirements-dev.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --requirement requirements-dev.txt

COPY . .

RUN chmod +x entrypoint.sh

CMD [ "python", "manage.py", "run", "-h", "0.0.0.0" ]
