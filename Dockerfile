FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:latest
COPY --from=ghcr.io/astral-sh/uv:0.5.5 /uv /uvx /bin/

# set up a virtual env to use for whatever app is destined for this container.
# RUN $HOME/.local/bin/uv venv --python 3.10 /venv
# COPY README.md .
# COPY . .
# RUN UV_PROJECT_ENVIRONMENT=venv $HOME/.local/bin/uv sync
# RUN $HOME/.local/bin/uv pip install -e .

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []
