#!/usr/bin/env bash

set -x
set -e

# Verify setup.py version matches the git tag
SETUP_VERSION=$(grep -oP '(?<=version=")[^"]+' setup.py)
GIT_TAG=$(git describe --tags --abbrev=0)
test "$SETUP_VERSION" == "$GIT_TAG" || exit 1

# Verify setup.py requirements match requirements/base.txt
SETUP_REQUIREMENTS=$(sed -n -e '/requirements = """/,/"""/ p' setup.py | grep -v '"""' | grep -v '^$')

BASE_REQUIREMENTS=$(cat requirements/base.txt)
test "$SETUP_REQUIREMENTS" == "$BASE_REQUIREMENTS" || exit 1
