# Environment Setup
venv:
	uv venv
	uv sync

init: venv
	pre-commit install
	pre-commit install --hook-type commit-msg

# Actions
test:
	coverage run -m pytest tests --junitxml=test-execution.xml

install:
	uv pip install dist/*.whl

clean:
	rm -rf build dist *.egg-info
	rm -rf src/__pycache__ src/*/__pycache__ src/*/*/__pycache__
	rm -rf src/*.egg-info src/*/*.egg-info src/*/*/*.egg-info

build: clean
	python -m build --sdist --wheel

upload: clean build
	uv run twine check dist/*
	uv run twine upload -r testpypi dist/*

install-local:
	uv install -e .

install-build: build
	uv pip install dist/*.whl

.PHONY: venv init test
