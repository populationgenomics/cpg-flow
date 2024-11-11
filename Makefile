# Environment Setup
venv:
	uv venv --python=python3.10
	uv sync

init: venv
	pre-commit install
	pre-commit install --hook-type commit-msg

# Actions
test:
	coverage run -m pytest tests --junitxml=test-execution.xml


.PHONY: venv init test
