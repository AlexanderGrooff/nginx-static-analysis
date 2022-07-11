#!/usr/bin/env bash
set -e

ARCH="amd64"
DIST="${DIST:-buster}"
BUILDAREA="/tmp/nsa-build"
BRANCH="main"

if [ -z $VERSION ];
    echo "Specify a version first"
    exit 2
fi

if [ "$(git rev-parse --abbrev-ref HEAD)" != $BRANCH ]; then
    echo "You are not on the $BRANCH branch, aborting"
    /bin/false
fi;

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
