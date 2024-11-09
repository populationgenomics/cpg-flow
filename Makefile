remove-deps:
	rm -f requirements/main.txt requirements/dev.txt requirements/test.txt

update-deps:
	pre-commit autoupdate
	uv pip compile --upgrade --resolver backtracking -o requirements/main.txt pyproject.toml
	uv pip compile --extra dev --upgrade --resolver backtracking -o requirements/dev.txt pyproject.toml
	uv pip compile --extra test --upgrade --resolver backtracking -o requirements/test.txt pyproject.toml

compile-deps:
	uv pip compile -o requirements/main.txt pyproject.toml
	uv pip compile --extra dev -o requirements/dev.txt pyproject.toml
	uv pip compile --extra test -o requirements/test.txt pyproject.toml

install-test:
	uv pip install -r requirements/test.txt

install-main:
	uv pip install -r requirements/main.txt

install-dev:
	uv pip install -r requirements/dev.txt

install-deps: install-dev install-test install-main
	uv run pip check

init:
	uv venv --python=python3.10
	pre-commit install
	pre-commit install --hook-type commit-msg
	make compile

activate:
	uv activate

update: update-deps install-deps
compile: compile-deps install-deps

.PHONY: activate compile compile-deps init install-deps install-dev install-main install-test remove-deps update update-deps
