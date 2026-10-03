# Base image: cpg_hail_gcloud, built by CPG from its Hail fork, providing
# Python 3.11 and a Hail compiled against the image's Java/Spark.
#
# The image runs this base image's Hail, not PyPI's. The environment below is
# created with the base image's site-packages visible and everything in uv.lock is
# installed into it except Hail, so `import hail` resolves to the base image's
# build while every other package is the version the lock holds. uv.lock is held
# to this image's Hail by `[tool.uv] constraint-dependencies` in pyproject.toml.
# To move Hail versions, change the tag below and that constraint together, then
# re-lock.
FROM australia-southeast1-docker.pkg.dev/cpg-common/images/cpg_hail_gcloud:0.2.138.cpg2-2

# uv is pinned to an explicit version so that rebuilding a commit does not pick up
# a newer uv. Change it deliberately.
COPY --from=ghcr.io/astral-sh/uv:0.11.28 /uv /uvx /bin/

# Set up working directory for the project
WORKDIR /cpg-flow

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Use the base image's Python only. A Python that uv downloaded would have its own
# site-packages, not the base image's, and the environment below would not find
# the base image's Hail.
ENV UV_PYTHON_DOWNLOADS=never

# Record the base image's Hail version, commit hash included, before anything is
# installed. It is compared with the Hail in the finished environment at the end.
RUN python -c "import hail; print(hail.version())" > /tmp/hail_version_base

# Create the environment with the base image's site-packages visible, after its
# own, so that Hail resolves from the base image and every package that uv.lock
# holds is installed here and takes precedence over the base image's copy.
RUN uv venv --system-site-packages

# Install the project's dependencies using the lockfile and settings
# Copy `pyproject.toml` and `uv.lock` into `/cpg-flow` explicitly
COPY pyproject.toml uv.lock /cpg-flow/

# Install the project's dependencies using the lockfile and settings, except
# Hail, which only the base image supplies. The lock still resolves Hail (at the
# version of the base image, see above) so that its dependencies are locked.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-install-package hail

# Add the project source code from src/cpg-flow
ADD . /cpg-flow
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-package hail

# Place executables in the environment at the front of the path
ENV PATH="/cpg-flow/.venv/bin:$PATH"
ENV PYTHONPATH="/cpg-flow:${PYTHONPATH}"

# Fail the build, not a batch, if Hail in the finished environment is not the base
# image's, or aiohttp is 3.14 or later: from 3.14.0 aiohttp raises on the HTTP 308
# that GCS returns between hailtop's upload chunks, which fails every multi-chunk
# upload (aio-libs/aiohttp#12195, populationgenomics/talos#718; pyproject.toml
# caps aiohttp for this). `python` here is the environment's, since PATH is set above.
RUN python -c "\
import pathlib, sys; \
import aiohttp, hail; \
base = pathlib.Path('/tmp/hail_version_base').read_text().strip(); \
print('hail', hail.version(), hail.__file__, 'aiohttp', aiohttp.__version__, aiohttp.__file__); \
aiohttp_minor = tuple(int(part) for part in aiohttp.__version__.split('.')[:2]); \
checks = [ \
    (hail.version() == base, f'hail is {hail.version()} but the base image has {base}'), \
    (aiohttp_minor < (3, 14), f'aiohttp {aiohttp.__version__} is 3.14 or later (populationgenomics/talos#718)')]; \
sys.exit('; '.join(message for ok, message in checks if not ok) or None)" \
    && rm /tmp/hail_version_base
