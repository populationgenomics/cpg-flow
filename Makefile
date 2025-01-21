# Environment Setup
venv:
	uv sync

init: venv
	uv run pre-commit install

init-dev: init install-local
	uv run pre-commit install --hook-type commit-msg

# Actions
test:
	uv run coverage run -m pytest tests --junitxml=test-execution.xml
	uv run coverage xml

clean:
	rm -rf build dist *.egg-info
	rm -rf src/__pycache__ src/*/__pycache__ src/*/*/__pycache__
	rm -rf src/*.egg-info src/*/*.egg-info src/*/*/*.egg-info
	rm -rf docs/generated

readme:
	uv run python docs/update_readme.py

# Pass the git branch as an argument to the pdoc command
# This will allow us to generate the documentation for the current branch
# and not the default branch
BRANCH ?= $(shell git rev-parse --abbrev-ref HEAD)
docs:
	@echo "Branch is '$(BRANCH)'"
	uv run pdoc cpg_flow --output-dir "docs/generated/$(BRANCH)"
	ls -la docs/
	ls -la docs/generated/

ci-build: clean
	python -m pip install build "setuptools>=42" setuptools-scm wheel
	SETUPTOOLS_SCM_PRETEND_VERSION="$$NEW_VERSION" python -m build --sdist --wheel

build: clean
	uv build --sdist --wheel

install-build: build
	uv pip install dist/*.whl

install-local:
	uv pip install -e .

upload: clean build
	uv run twine check dist/*
	uv run twine upload -r testpypi dist/*

.PHONY: venv init test docs clean ci-build build install-build install-local upload
