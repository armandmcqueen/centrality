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
	ruff format --check . || true

.PHONY: typecheck
typecheck:
	mypy --strict .

.PHONY: install
install:
	pip install -e .

.PHONY: install-dev
install-dev:
	pip install -e .

.PHONY: codegen
codegen:
	dev codegen types
	dev codegen datastore-client
	dev codegen rest
