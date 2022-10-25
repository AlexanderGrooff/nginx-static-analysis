#!/usr/bin/env bash

NGINX_EXEC="docker-compose exec -T nginx"

if [[ ! $(docker-compose ps --services --filter status=running nginx | grep nginx) ]]; then
    docker-compose up -d nginx
fi

if [[ ! $($NGINX_EXEC command -v pytest) ]]; then
    $NGINX_EXEC python3 -m pip install pytest
fi

$NGINX_EXEC python3 -m pytest
$NGINX_EXEC ./tests/integration_tests.sh
