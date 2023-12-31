.PHONY: docker-build
docker-build:
	docker build -t armandmcqueen/centrality-dev:latest .

.PHONY: docker-run
docker-run:
	docker run -it --rm armandmcqueen/centrality-dev:latest bash

.PHONY: docker-push
docker-push:
	docker push armandmcqueen/centrality-dev:latest

.PHONY: test
test:
	pytest tests/e2e/

.PHONY: test-verbose
test-verbose:
	pytest --capture=no tests/e2e/

.PHONY: lint
lint:
	make -C common lint
	make -C controlplane lint
	make -C cli lint
	make -C deploy lint
	make -C rapidui lint
	make -C scripts lint
	make -C tests lint
	make -C vmagent lint

.PHONY: formatcheck
formatcheck:
	make -C common formatcheck
	make -C controlplane formatcheck
	make -C cli formatcheck
	make -C deploy formatcheck
	make -C rapidui formatcheck
	make -C scripts formatcheck
	make -C tests formatcheck
	make -C vmagent formatcheck

.PHONY: typecheck
typecheck:
	make -C common typecheck
	make -C controlplane typecheck
	make -C cli typecheck
	make -C deploy typecheck
	make -C rapidui typecheck
	make -C scripts typecheck
	make -C tests typecheck
	make -C vmagent typecheck

.PHONY: install
install:
	make -C common install
	make -C controlplane install
	make -C cli install
	make -C deploy install
	make -C rapidui install
	make -C scripts install
	make -C tests install
	make -C vmagent install

.PHONY: install-dev
install-dev:
	make -C common install-dev
	make -C controlplane install-dev
	make -C cli install-dev
	make -C deploy install-dev
	make -C rapidui install-dev
	make -C scripts install-dev
	make -C tests install-dev
	make -C vmagent install-dev



