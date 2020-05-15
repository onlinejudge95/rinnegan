# rinnegan-db

## About

We are currently using `postgres:12.2-alpine` image from dockerhub for the database.
The current image size for database is `152MB` and is tagged as `postgres:development`

## Setup

1. Create a file named `services/db/.env` using `services/db/.env.example` as a template.
2. Edit your local db credentials in `services/db/.env`
3. Edit `services/db/db.sql` to rename the databases used for development and testing.
4. In the `docker-compose.yml` add the following volume mount `./services/db/data:/var/lib/postgresql/data/` so that data is persisted between sesssions.

## Contact-Us

[onlinejudge95](mailto:onlinejudge95@gmail.com)
