#!/usr/bin/env bash

function uninstall {
    pip freeze | grep nginx-static-analysis && pip uninstall -y nginx-static-analysis
}
trap uninstall EXIT

python setup.py install

# Tests
nginx-static-analysis directive server_name |& grep example.com && echo "OK"
nginx-static-analysis directive server_name --value example.com |& grep example.com && echo "OK"
nginx-static-analysis directive server_name --value banaan.com |& grep example.com || echo "OK"
