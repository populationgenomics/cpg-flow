FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:latest
FROM ghcr.io/astral-sh/uv:0.2.12 as uv

RUN --mount=from=uv,source=/uv,target=./uv \
    ./uv venv /opt/venv
# We need to set this environment variable so that uv knows where
# the virtual environment is to install packages
ENV VIRTUAL_ENV=/opt/venv
# Make sure that the virtual environment is in the PATH so
# we can use the binaries of packages that we install such as pip
# without needing to activate the virtual environment explicitly
ENV PATH="/opt/venv/bin:$PATH"

# Copy the files into the container
COPY README.md .
COPY . .

# Install the packages with uv using --mount=type=cache to cache the downloaded packages
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=from=uv,source=/uv,target=./uv \
    ./uv pip install metamist

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=from=uv,source=/uv,target=./uv \
    ./uv pip install -e .
