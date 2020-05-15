# rinnegan-server

## About

We are currently using `python:3.8.2-slim` image from dockerhub for the database.
The current image size for server is `411MB` and is tagged as `server:development`

Server for rinnegan is written in `Flask` using `Flask-RESTX` as swagger support.
We currently have a single pipeline involving following stages

1. **build** the docker image is build
2. **test** the build image is used to run the tests
3. **deploy** the tested image is pushed to heroku container registry for deployment

## Setup

1. Create a file named `/services/server/.env` using `/services/server/.env.example` as a template.
2. Edit your database url string for development and test environment by using the values derived in `/services/db/.env` [file](../db/README.md#Setup)
3. In the `docker-compose.yml` add the following volume mount `./services/server:/usr/src/app` to support hot reloading.
4. To start the container run the following command
   ```bash
   $ docker-compose up --build --detach
   ```
   This will bring your database and the server up and running
5. The volume mount for storing data is owned by the root user so if you are running docker as a non-root user in your system,
   you can use the script provided at `/bin/orchestrate_container.sh`
6. Once the DB is up and running you need to run the script `/bin/sync_database.sh` to bring the database to current schema.
7. To run the tests use the following script `/bin/test_server.sh`

## TODO:-

- Add migration support

## Contact-Us

[onlinejudge95](mailto:onlinejudge95@gmail.com)
