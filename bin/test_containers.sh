#!/bin/zsh

FLAG=$1

if [ $FLAG = "server" ]; then
    docker-compose exec server black --config /usr/src/app/pyproject.toml /usr/src/app
    docker-compose exec server flake8 --config /usr/src/app/setup.cfg /usr/src/app
    docker-compose exec server isort --atomic --case-sensitive --force-alphabetical-sort-within-sections --force-single-line-imports --lines-after-imports 2 --lines-between-types 1 --line-width 79 --recursive --skip-glob "migrations/*" /usr/src/app
    docker-compose exec server pytest -c /usr/src/app/app/tests/pytest.ini
    
    elif [ $FLAG = "client" ]; then
    docker-compose exec client npm run lint
    docker-compose exec client npm run prettier:check
    docker-compose exec client npm test
else
    docker-compose exec server black --config /usr/src/app/pyproject.toml /usr/src/app
    docker-compose exec server flake8 --config /usr/src/app/setup.cfg /usr/src/app
    docker-compose exec server isort --atomic --case-sensitive --force-alphabetical-sort-within-sections --force-single-line-imports --lines-after-imports 2 --lines-between-types 1 --line-width 79 --recursive --skip-glob "migrations/*" /usr/src/app
    docker-compose exec server pytest -c /usr/src/app/app/tests/pytest.ini
    
    docker-compose exec client npm run lint
    docker-compose exec client npm run prettier:check
    docker-compose exec client npm test
fi
