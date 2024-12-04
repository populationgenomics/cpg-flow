#!/bin/bash

# Check that the most recent commit has been pushed to the remote
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
if test -n "$(git log --oneline origin/$BRANCH_NAME..$BRANCH_NAME)"
then
    echo "There are unpushed commits in the repository. Please push them before running the tests."
    exit 1
fi

# Variables
REGION="australia-southeast1"
REPO="cpg-common"
IMAGE_REPO="images-tmp"
IMAGE_NAME="cpg_flow"
SLEEP_DURATION=180  # Sleep for 3 minutes (in seconds)

# Get the latest commit SHA from the local Git repository
COMMIT_SHA=$(git rev-parse HEAD)

echo "Latest commit SHA: $COMMIT_SHA"

# Function to check if the tag exists
check_tag() {
    gcloud artifacts docker tags list "$REGION-docker.pkg.dev/$REPO/$IMAGE_REPO/$IMAGE_NAME" | grep -q "$COMMIT_SHA"
}

# Loop until the tag is found
while true; do
    echo "Checking for tag matching the latest commit SHA ($COMMIT_SHA)..."
    if check_tag; then
        echo "Tag matching the latest commit SHA ($COMMIT_SHA) exists in the repository."
        break
    else
        echo "No tag matching the latest commit SHA ($COMMIT_SHA) found. Retrying in $SLEEP_DURATION seconds..."
        sleep $SLEEP_DURATION
        SLEEP_DURATION=$((SLEEP_DURATION / 2))

        # Sleep duration should be minimum 10 seconds
        if test $SLEEP_DURATION -lt 10
        then
            SLEEP_DURATION=10
        fi
    fi
done


# Run the analysis-runner
IMAGE_FULLNAME="$REGION-docker.pkg.dev/$REPO/$IMAGE_REPO/$IMAGE_NAME:$COMMIT_SHA"

echo "Running the analysis-runner with the image: $IMAGE_FULLNAME"

echo "analysis-runner \
    --image "$IMAGE_FULLNAME" \
    --dataset "fewgenomes" \
    --description "cpg-flow_test" \
    --access-level "test" \
    --output-dir "cpg-flow_test" \
    --config "config.toml" \
    workflow.py"

analysis-runner \
    --image "$IMAGE_FULLNAME" \
    --dataset "fewgenomes" \
    --description "cpg-flow_test" \
    --access-level "test" \
    --output-dir "cpg-flow_test" \
    --config "config.toml" \
    workflow.py
