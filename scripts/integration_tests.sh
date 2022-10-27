#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

set -e
set -x

function uninstall {
    pip freeze | grep nginx-static-analysis && pip uninstall -y nginx-static-analysis
}
trap uninstall EXIT

python setup.py install
NSA=/usr/local/bin/nginx-static-analysis

# Ensure the basic functionality works
$NSA --help || (echo "NOT OK" && exit 1)
$NSA directive server_name || (echo "NOT OK" && exit 1)
# Garbage in --> no matches
$NSA directive blabla |& grep "Found no matches" || (echo "NOT OK" && exit 1)
# Value should show the value in table format
$NSA directive server_name --values example.com |& grep example.com || (echo "NOT OK" && exit 1)
# Value should not show other values
$NSA directive server_name --values banaan.com |& grep example.com && (echo "NOT OK" && exit 1)
# Accept multiple directives with n-1 values
$NSA directive server_name location --values example.com || (echo "NOT OK" && exit 1)
# Raise error on <n-1 values
$NSA directive server_name location && (echo "NOT OK" && exit 1)
# Raise error on >n values
$NSA directive server_name location --values example.com /static bla && (echo "NOT OK" && exit 1)

echo "All tests passed"
