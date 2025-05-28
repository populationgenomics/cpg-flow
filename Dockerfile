FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:latest
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up working directory for the project
WORKDIR /cpg-flow

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /cpg-flow
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/cpg-flow/.venv/bin:$PATH"
ENV PYTHONPATH="/cpg-flow:${PYTHONPATH}"
