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

if [[ ! $($NGINX_EXEC command -v pytest) ]]; then
    $NGINX_EXEC python3 -m pip install pytest
fi

$NGINX_EXEC coverage run -m pytest
$NGINX_EXEC coverage report
$NGINX_EXEC coverage xml -o coverage.xml
$NGINX_EXEC ./scripts/integration_tests.sh
