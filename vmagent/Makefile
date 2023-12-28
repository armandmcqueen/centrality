# lint with ruff
.PHONY: lint
lint: format
	ruff check .

# format with ruff
.PHONY: format
format:
	ruff format .

.PHONY: formatcheck
formatcheck:
	ruff format --check .

.PHONY: typecheck
typecheck:
	mypy --strict .

.PHONY: launch
launch:
	python vmagent/cli.py launch

.PHONY: install
install:
	pip install -e .

.PHONY: install-dev
install-dev:
	pip install -e ".[dev]"
