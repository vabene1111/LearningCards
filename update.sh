#!/usr/bin/env bash
docker-compose run web_quiz python3 manage.py migrate
docker-compose run web_quiz python3 manage.py collectstatic --noinput
