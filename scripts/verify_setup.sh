#!/usr/bin/env bash

set -x
set -e

# Verify versions matches the git tag
SETUP_VERSION=$(grep -oP '(?<=version=")[^"]+' setup.py)
PKGBUILD_VERSION=$(grep -oP '(?<=pkgver=)[^ ]+' PKGBUILD)
PYPROJECT_VERSION=$(grep -oP '(?<=version = ")[^"]+' pyproject.toml)
GIT_TAG=$(git describe --tags --abbrev=0 || echo "")
if [ -z $GIT_TAG ]; then
    echo "No git tag found, skipping"
    exit 0
fi

test "$SETUP_VERSION" == "$GIT_TAG" || (echo "setup.py is version ${SETUP_VERSION} but should be ${GIT_TAG}" && exit 1)
test "$PKGBUILD_VERSION" == "$GIT_TAG" || (echo "PKGBUILD is version ${PKGBUILD_VERSION} but should be ${GIT_TAG}" && exit 1)
test "$PYPROJECT_VERSION" == "$GIT_TAG" || (echo "pyproject.toml is version ${PYPROJECT_VERSION} but should be ${GIT_TAG}" && exit 1)

# Verify setup.py requirements match requirements/base.txt
SETUP_REQUIREMENTS=$(sed -n -e '/requirements = """/,/"""/ p' setup.py | grep -v '"""' | grep -v '^$')

BASE_REQUIREMENTS=$(cat requirements/base.txt)
test "$SETUP_REQUIREMENTS" == "$BASE_REQUIREMENTS" || exit 1

if [[ `command -v makepkg` ]]; then
    makepkg --printsrcinfo > .SRCINFO
    git diff --exit-code .SRCINFO || (echo ".SRCINFO is out of date, run makepkg --printsrcinfo and commit the changes" && exit 1)
fi
