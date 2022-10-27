#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

set -e
set -x

function uninstall {
    pip freeze | grep nginx-static-analysis && pip uninstall -y nginx-static-analysis
}
trap uninstall EXIT

python setup.py install

# Ensure the basic functionality works
nginx-static-analysis directive server_name || (echo "NOT OK" && exit 1)
# Value should show the value in table format
nginx-static-analysis directive server_name --value example.com |& grep example.com || (echo "NOT OK" && exit 1)
# Value should not show other values
nginx-static-analysis directive server_name --value banaan.com |& grep example.com && (echo "NOT OK" && exit 1)
# Accept multiple directives
nginx-static-analysis directive server_name location || (echo "NOT OK" && exit 1)
# Accept multiple directives with n-1 values
nginx-static-analysis directive server_name location --value example.com || (echo "NOT OK" && exit 1)
# Raise error on >n-1 values
nginx-static-analysis directive server_name location --value example.com /static && (echo "NOT OK" && exit 1)

echo "All tests passed"
