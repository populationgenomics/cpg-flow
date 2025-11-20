FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:latest
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up working directory for the project
WORKDIR /cpg-flow

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
# Use bind mounts to avoid copying files into the layer (better cache invalidation)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy only the source code (dependencies are already installed above)
# This layer only invalidates when source code changes, not when dependencies change
COPY src /cpg-flow/src
COPY pyproject.toml uv.lock /cpg-flow/

# Install the project itself (fast since dependencies are already installed)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-deps

# Place executables in the environment at the front of the path
ENV PATH="/cpg-flow/.venv/bin:$PATH"
ENV PYTHONPATH="/cpg-flow:${PYTHONPATH}"
