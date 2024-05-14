#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

set -e

bash scripts/verify_setup.sh

if type -p docker-compose > /dev/null; then
    DC_BIN="docker-compose"
else
    DC_BIN="docker compose"
fi
echo "Using '$DC_BIN'"

# Check if we're running in the Github Actions runner
if [[ -z "$GITHUB_ACTIONS" ]]; then
    NGINX_EXEC="$DC_BIN exec nginx"
else
    # Run without TTY in Github Actions
    NGINX_EXEC="$DC_BIN exec -T nginx"
fi

if [[ ! $($DC_BIN ps --services --filter status=running nginx | grep nginx) ]]; then
    $DC_BIN up -d nginx
fi

$NGINX_EXEC ./scripts/integration_tests.sh
