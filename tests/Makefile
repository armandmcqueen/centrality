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

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: install-dev
install-dev:
	pip install -r requirements.txt


