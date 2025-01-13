# Environment Setup
venv:
	uv sync

init: venv
	pre-commit install
	pre-commit install --hook-type commit-msg

# Actions
test:
	uv run coverage run -m pytest tests --junitxml=test-execution.xml
	uv run coverage xml

clean:
	rm -rf build dist *.egg-info
	rm -rf src/__pycache__ src/*/__pycache__ src/*/*/__pycache__
	rm -rf src/*.egg-info src/*/*.egg-info src/*/*/*.egg-info

docs:
	pwd
	ls
	ls docs/
	uv run python docs/update_readme.py
	uv run pdoc cpg_flow --output-dir "docs/$(shell git rev-parse --abbrev-ref HEAD)"
	pre-commit run --all-files
	exit 1

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

.PHONY: venv init test docs clean ci-build build install-build install-local upload
