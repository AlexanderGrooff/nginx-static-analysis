#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

set -e

# Check if we're running in the Github Actions runner
if [[ -z "$GITHUB_ACTIONS" ]]; then
    NGINX_EXEC="docker-compose exec nginx"
else
    # Run without TTY in Github Actions
    NGINX_EXEC="docker-compose exec -T nginx"
fi

if [[ ! $(docker-compose ps --services --filter status=running nginx | grep nginx) ]]; then
    docker-compose up -d nginx
fi

$NGINX_EXEC ./scripts/integration_tests.sh
