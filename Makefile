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

init:
	python -m pip install --upgrade pip-tools pip wheel
	python -m pip install -r requirements/main.txt -r requirements/dev.txt -r requirements/test.txt -e .
	python -m pip check

update: update-deps install-deps

.PHONY: update-deps compile-deps install-deps update
