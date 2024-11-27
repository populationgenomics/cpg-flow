#!/bin/bash

# Fail with warning if the most recent local commit is not pushed to the remote
if test -n "$(git status --porcelain)"
then
    echo "There are uncommitted changes in the repository. Please commit and push them before running the tests."
    exit 1
fi

# Check that the most recent commit has been pushed to the remote
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
if test -n "$(git log --oneline origin/$BRANCH_NAME..$BRANCH_NAME)"
then
    echo "There are unpushed commits in the repository. Please push them before running the tests."
    exit 1
fi

# Confirm that the image for this commit has been built and deployed
DOCKER_IMAGE="australia-southeast1-docker.pkg.dev/cpg-common/images-tmp/cpg_flow"
COMMIT_SHA=$(git rev-parse HEAD)
WAIT_TIME=180  # 3 minutes

function check_image_exists {
    found=$(gcloud artifacts docker tags list $DOCKER_IMAGE | grep "$COMMIT_SHA")
    if [ -n "$found" ]
    then
        return 0
    else
        return 1
    fi
}

while ! check_image_exists
do
    echo "The Docker image for this commit has not been built and deployed. Please wait for deploy to complete before running the test."
    sleep $WAIT_TIME
    WAIT_TIME=$((WAIT_TIME / 2))
done

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
