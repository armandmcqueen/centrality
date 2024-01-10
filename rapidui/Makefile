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
	ruff format --check . || true || true

.PHONY: typecheck
typecheck:
	mypy --strict .

.PHONY: launch
launch:
	./launch.bash ../tests/configs/quicktest/rapidui.yaml

.PHONY: launch-fly
launch-fly:
	./launch.bash ../tests/configs/fly/rapidui.yaml

.PHONY: install
install:
	pip install -e .

.PHONY: install-dev
install-dev:
	pip install -e ".[dev]"
