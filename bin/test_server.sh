#!/bin/zsh

docker-compose exec server black --config /usr/src/app/pyproject.toml /usr/src/app
docker-compose exec server flake8 --config /usr/src/app/setup.cfg /usr/src/app
docker-compose exec server isort --atomic --case-sensitive --force-alphabetical-sort-within-sections --force-single-line-imports --lines-after-imports 2 --lines-between-types 1 --line-width 79 --recursive --skip-glob "migrations/*" /usr/src/app
docker-compose exec server pytest -c /usr/src/app/app/tests/pytest.ini
