#!/usr/bin/env bash
set -e
set -x

export DEBIAN_FRONTEND=noninteractive

ARCH="amd64"
DIST="${DIST:-buster}"
BUILDAREA="/tmp/nsa-build"
BRANCH="main"
MESSAGE="chore: release version $VERSION"

if [ -z $VERSION ]; then
    echo "Specify a version first"
    exit 2
fi

# Install dependencies
sudo apt-get update && sudo apt-get install -y \
  build-essential git-buildpackage debhelper devscripts dh-python \
  dh-systemd debian-archive-keyring quilt cowbuilder pristine-tar fakeroot

if [ ! -z $CHANGELOG ]; then
  gbp dch --debian-branch=main --commit --commit-msg=$MESSAGE --release --spawn-editor=never --ignore-branch
fi

mkdir -p $BUILDAREA-$DIST

# Build base cow image
DIST=$DIST ARCH=$ARCH git-pbuilder create

gbp buildpackage --git-pbuilder --git-export-dir=$BUILDAREA-$DIST \
--git-dist=$DIST --git-arch=$ARCH \
--git-ignore-new --git-ignore-branch
