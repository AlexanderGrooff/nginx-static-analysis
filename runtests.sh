#!/usr/bin/env bash

NGINX_EXEC="docker-compose exec nginx"

if [[ ! $(docker-compose ps --services --filter status=running nginx | grep nginx) ]]; then
    docker-compose up -d nginx
fi

$NGINX_EXEC "pytest"
