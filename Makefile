update-deps:
	pre-commit autoupdate
	python -m pip install --upgrade pip-tools pip wheel
	python -m piptools compile --strip-extras --upgrade --resolver backtracking -o requirements/main.txt pyproject.toml
	python -m piptools compile --strip-extras --extra dev --upgrade --resolver backtracking -o requirements/dev.txt pyproject.toml
	python -m piptools compile --strip-extras --extra test --upgrade --resolver backtracking -o requirements/test.txt pyproject.toml

compile-deps:
	python -m piptools compile --strip-extras -o requirements/main.txt pyproject.toml
	python -m piptools compile --strip-extras --extra dev -o requirements/dev.txt pyproject.toml
	python -m piptools compile --strip-extras --extra test -o requirements/test.txt pyproject.toml

install-deps:
	python -m pip install --upgrade pip-tools pip wheel
	python -m pip install -r requirements/main.txt -r requirements/dev.txt -r requirements/test.txt -e .
	python -m pip check

update: update-deps compile-deps install-deps
compile: compile-deps install-deps

init: install-deps
	pre-commit install
	pre-commit install --hook-type commit-msg

clean:
	rm -rf build dist *.egg-info
	rm -rf src/__pycache__ src/*/__pycache__ src/*/*/__pycache__
	rm -rf src/*.egg-info src/*/*.egg-info src/*/*/*.egg-info

build: clean
	python -m build --sdist --wheel

upload: clean build
	python -m twine check dist/*
	python -m twine upload -r testpypi dist/*

install-local:
	pip install --force-reinstall -e .

install-build: build
	pip install --force-reinstall dist/*.whl

run:
	python main.py


.PHONY: update-deps compile-deps install-deps compile update init build install-local install-build run clean
