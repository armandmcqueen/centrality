.PHONY: docker-build
docker-build:
	docker build -t armandmcqueen/centrality-dev:latest .

.PHONY: docker-run
docker-run:
	docker run -it --rm armandmcqueen/centrality-dev:latest bash

.PHONY: docker-push
docker-push:
	docker push armandmcqueen/centrality-dev:latest

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

.PHONY: check-format
check-format:
	make -C common check-format
	make -C controlplane check-format
	make -C cli check-format
	make -C deploy check-format
	make -C rapidui check-format
	make -C scripts check-format
	make -C tests check-format
	make -C vmagent check-format

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


