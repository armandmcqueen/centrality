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
	./launch.bash configs/dev.yaml

