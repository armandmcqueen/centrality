# lint with ruff
.PHONY: lint
lint: format
	ruff check . --fix

.PHONY: lintcheck
lintcheck:
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

.PHONY: launch-quick
launch-quick:
	python vmagent/cli.py launch -f ../tests/configs/quicktest/vmagent.yaml

.PHONY: install
install:
	pip install -e .

.PHONY: install-dev
install-dev:
	pip install -e ".[dev]"
