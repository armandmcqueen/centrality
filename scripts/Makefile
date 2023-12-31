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

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: install-dev
install-dev:
	pip install -r requirements.txt
