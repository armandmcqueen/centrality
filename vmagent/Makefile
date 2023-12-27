# lint with ruff
.PHONY: lint
lint: format
	ruff check .

# format with ruff
.PHONY: format
format:
	ruff format .

.PHONY: check-format
check-format:
	ruff format --check .

.PHONY: launch
launch:
	python vmagent/cli.py launch

.PHONY: install
install:
	pip install -e .

.PHONY: install-dev
install-dev:
	pip install -e ".[dev]"
