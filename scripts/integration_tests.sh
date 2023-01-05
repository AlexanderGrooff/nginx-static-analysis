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

echo "Ensure the basic functionality works"
$NSA --help || (echo "NOT OK" && exit 1)
$NSA -d server_name || (echo "NOT OK" && exit 1)

echo "Check if only unique lines are returned"
test $($NSA -d server_name |& grep example.com | wc -l) = 1 || (echo "NOT OK" && exit 1)

echo "Garbage in --> no matches"
$NSA -d blabla |& grep "Found no matches" || (echo "NOT OK" && exit 1)

echo "Value should show the value in table format"
$NSA -d server_name -f server_name=example.com |& grep example.com || (echo "NOT OK" && exit 1)

echo "Value should not show other values"
$NSA -d server_name -f server_name=banaan.com |& grep example.com && (echo "NOT OK" && exit 1)

echo "Multiple filters should show the most specific match"
$NSA -f location=/ -f server_name=example.com |& grep "/etc/nginx/servers/example.com.conf:8" || (echo "NOT OK" && exit 1)

echo "Show directives next to the direct match"
$NSA -f server_name=example.com |& grep "listen" | grep -v "default_server" || (echo "NOT OK" && exit 1)
$NSA -f server_name=testalex.hypernode.io |& grep "listen" | grep "default_server" || (echo "NOT OK" && exit 1)

echo "Don't show nested children of parent neighbours of direct match"
$NSA -f server_name=testalex.hypernode.io |& grep "/etc/nginx/servers/example.com.conf" && (echo "NOT OK" && exit 1)
$NSA -f server_name=example.com |& grep "/etc/nginx/servers/testalex.hypernode.io.conf" && (echo "NOT OK" && exit 1)

echo "Show nested includes"
$NSA -f server_name=testalex.hypernode.io |& grep "/nested" && (echo "NOT OK" && exit 1)
$NSA -f server_name=example.com |& grep "/nested" || (echo "NOT OK" && exit 1)

echo "All tests passed"
