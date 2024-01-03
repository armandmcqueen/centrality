.PHONY: install
install:
ifdef GITHUB_ACTIONS
	@echo "Running on GitHub Actions - Normal Install"
	pip install .
else
	@echo "Not running on GitHub Actions - Editable Install"
	pip install -e .
endif

.PHONY: install-dev
install-dev:
ifdef GITHUB_ACTIONS
	@echo "Running on GitHub Actions - Normal Install"
	pip install .
else
	@echo "Not running on GitHub Actions - Editable Install"
	pip install -e .
endif
