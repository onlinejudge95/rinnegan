#!/bin/zsh


docker-compose exec server pytest -c /usr/src/app/app/tests/pytest.ini
