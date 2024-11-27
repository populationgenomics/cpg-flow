#!/bin/bash

# Fail with warning if the most recent local commit is not pushed to the remote
if [ -n "$(git status --porcelain)" ]; then
    echo "There are uncommitted changes in the repository. Please commit and push them before running the tests."
    exit 1
fi

# Check that the most recent commit has been pushed to the remote
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
if [ -n "$(git log --oneline origin/$BRANCH_NAME..$BRANCH_NAME)" ]; then
    echo "There are unpushed commits in the repository. Please push them before running the tests."
    exit 1
fi

# Get commit sha
COMMIT_SHA=$(git rev-parse HEAD)
IMAGE_NAME="australia-southeast1-docker.pkg.dev/cpg-common/images-tmp/cpg_flow:$COMMIT_SHA"

analysis-runner \
    --image "$IMAGE_NAME" \
    --dataset "fewgenomes" \
    --description "cpg-flow_test" \
    --access-level "test" \
    --output-dir "cpg-flow_test" \
    --config "config.toml" \
    workflow.py
