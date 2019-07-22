#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# This file is part of COUNTER-Robots.
# Copyright (C) 2019 CERN.
#
# COUNTER-Robots is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
# Run an update for the user-agent lists.
# If there are updates, create and tag a new release.
set -e

# Setup the Git credentials for committing and tagging as Invenio.
setup_git () {
    git config user.name "Invenio"
    git config user.email "info@inveniosoftware.org"
}

# Commit all changes for this travis build.
# Because the update script may create new files we use `git add .`
commit_changes () {
    git add .
    git commit -am "data: update the user-agent lists in build $TRAVIS_BUILD_NUMBER"
}

# Create a new version by changing the version number
# and creating a tagged commit.
commit_release () {
    sed -i "s/__version__ =.*/__version__ = '$VERSION'/" counter_robots/version.py
    git add .
    git commit -m "release: $VERSION"
    git tag -a $TAG -m "release: counter-robots $VERSION"
}

# In case we run the script locally we have to set the build number.
if [ -z "$TRAVIS_BUILD_NUMBER" ]; then TRAVIS_BUILD_NUMBER="local"; fi

# Run the update-lists script to check for any updates. If we have any updates
# then we update the version number, commit the changes, and add a new tag in
# a vYYYY.MM format.
python scripts/update-lists.py
VERSION="$(date +'%Y.%m.%d')"
TAG="v$VERSION"
if [ -z "$(git diff --name-only)" ]
then
    echo "No changes found."
elif [ "$(git tag list $TAG)" ]
then
    echo "Tag $TAG already exists"
    exit 1
else
    echo "Changes found. Commiting and releasing $VERSION."
    setup_git
    commit_changes
    commit_release
fi

