FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:latest

ENV PATH=/venv/bin:$PATH
ENV PATH=/root/.cargo/bin:$PATH

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# set up a virtual env to use for whatever app is destined for this container.
RUN source $HOME/.local/bin/env
RUN uv venv --python 3.10 /venv

RUN uv pip install metamist
COPY README.md .
COPY . .
RUN uv pip install -e .
