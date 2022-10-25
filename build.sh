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
  build-essential git-buildpackage debhelper devscripts dh-python dh-systemd debian-archive-keyring

gbp dch --debian-branch=main --commit --commit-msg=$MESSAGE --release --spawn-editor=never --ignore-branch
gbp buildpackage --git-pbuilder --git-export-dir=$BUILDAREA-$DIST --git-dist=$DIST --git-arch=$ARCH \
--git-debian-branch=$TEMPBRANCH --git-ignore-new

echo "Updating setup.py with version $VERSION"
perl -pi -e 's/version="[^"]*",/version=\"$ENV{"VERSION"}\",/g;' setup.py

echo "Adding setup.py to git index"
git add setup.py

echo "Committing setup.py version update"
git commit setup.py -m "Update version in setup.py to $VERSION"

echo "Generating changelog changelog"
gbp dch --debian-tag="%(version)s" --new-version=$VERSION --debian-branch $BRANCH --release --commit

echo "Building package for $DIST"

git checkout $BRANCH
TEMPBRANCH="$BRANCH-build-$DIST-$VERSION"
git checkout -b $TEMPBRANCH

mkdir -p $BUILDAREA-$DIST
gbp buildpackage --git-pbuilder --git-export-dir=$BUILDAREA-$DIST --git-dist=$DIST --git-arch=$ARCH \
--git-debian-branch=$TEMPBRANCH --git-ignore-new

git checkout $BRANCH
git branch -D $TEMPBRANCH

echo
echo "*************************************************************"
echo

echo "Creating tag $VERSION"
git tag $VERSION

echo "Now push the commit with the version update and the tag: git push; git push --tags"
