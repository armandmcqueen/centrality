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
	make -C vmagent lint
	make -C cli lint
	make -C tests lint
	make -C deploy lint

.PHONY: install
install:
	make -C cli install
	make -C common install
	make -C controlplane install
	make -C deploy install
	make -C rapidui install
	make -C vmagent install


