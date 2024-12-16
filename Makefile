# Environment Setup
venv:
	uv sync

init: venv
	pre-commit install
	pre-commit install --hook-type commit-msg

init-dev: init
	uv sync --dev

# Actions
test:
	coverage run -m pytest tests --junitxml=test-execution.xml

clean:
	rm -rf build dist *.egg-info
	rm -rf src/__pycache__ src/*/__pycache__ src/*/*/__pycache__
	rm -rf src/*.egg-info src/*/*.egg-info src/*/*/*.egg-info

readme:
	python docs/document_readme.py

docs: readme
	@BRANCH_NAME=$(shell git rev-parse --abbrev-ref HEAD) && \
	echo "Building docs for branch $$BRANCH_NAME" && \
	uv run pdoc cpg_flow --output-dir "docs/$$BRANCH_NAME"

docs-serve: readme
	@BRANCH_NAME=$(shell git rev-parse --abbrev-ref HEAD) && \
	echo "Serving docs for branch $$BRANCH_NAME" && \
	uv run pdoc cpg_flow

ci-build: clean docs
	python -m pip install build "setuptools>=42" setuptools-scm wheel
	SETUPTOOLS_SCM_PRETEND_VERSION="$$NEW_VERSION" python -m build --sdist --wheel

build: clean
	uv build --sdist --wheel

install-build: build
	uv pip install dist/*.whl

install-local:
	uv install -e .

upload: clean build
	uv run twine check dist/*
	uv run twine upload -r testpypi dist/*

.PHONY: venv init test docs readme clean ci-build build install-build install-local upload
