FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:latest

ENV PATH=/venv/bin:$PATH
ENV PATH=/root/.cargo/bin:$PATH

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# set up a virtual env to use for whatever app is destined for this container.
RUN $HOME/.local/bin/uv venv --python 3.10 /venv
COPY README.md .
COPY . .
RUN UV_PROJECT_ENVIRONMENT=venv $HOME/.local/bin/uv sync
RUN $HOME/.local/bin/uv pip install -e .

# activate the virtual environment
ENV PATH="/venv/bin:$PATH"
