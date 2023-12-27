# lint with ruff
.PHONY: lint
lint: format
	ruff check .

# format with ruff
.PHONY: format
format:
	ruff format .


.PHONY: launch
launch:
	./launch.bash ../tests/configs/quicktest/rapidui.yaml

.PHONY: launch-fly
launch-fly:
	./launch.bash ../tests/configs/fly/rapidui.yaml

.PHONY: install
install:
	pip install -e .


