# rinnegan-db

## About

We are currently using `postgres:12.2-alpine` image from dockerhub for the database.
The current image size for database is `152MB` and is tagged as `postgres:development`

## Setup

1. Create a file named `/services/postgre/.env` using `/services/postgre/.env.example` as a template.
2. Edit your local db credentials in `/services/postgre/.env`
3. Edit `/services/postgre/db.sql` to rename the databases used for development and testing.
4. In the `docker-compose.yml` add the following volume mount `./services/postgre/data:/var/lib/postgresql/data/` so that data is persisted between sesssions.
5. To start the container run the following command
   ```bash
   $ docker-compose up --build --detach
   ```
   This will bring your database and the server up and running
6. The volume mount for storing data is owned by the root user so if you are running docker as a non-root user in your system,
   you can use the script provided at `/bin/orchestrate_container.sh`

## Contact-Us

[onlinejudge95](mailto:onlinejudge95@gmail.com)
