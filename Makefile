.PHONY: docker-build
docker-build:
	docker build -t armandmcqueen/centrality-dev:latest .

.PHONY: docker-run
docker-run:
	docker run -it --rm armandmcqueen/centrality-dev:latest bash

.PHONY: docker-push
docker-push:
	docker push armandmcqueen/centrality-dev:latest

.PHONY: docker-compose-mount-up
docker-compose-mount-up:
	docker rm -f centrality-postgres-1
	docker compose -f compose.yaml -f compose-override-mountcode.yaml up $(ARGS)

.PHONY: docker-compose-mount-up-controlplane
docker-compose-mount-up-controlplane:
	make docker-compose-mount-up ARGS="postgres controlplane rapidui"

.PHONY: docker-compose-mount-up-solo
docker-compose-mount-up-solo:
	make docker-compose-mount-up ARGS="postgres controlplane rapidui machineagent-gpu"


.PHONY: test
test:
	# TODO: Incorporate CentralityConfig tests
	make -C tests/e2e test
	make -C tests/datastore test

.PHONY: test-verbose
test-verbose:
	make -C tests/e2e test-verbose
	make -C tests/datastore test-verbose

.PHONY: lint
lint:
	make -C common lint
	make -C controlplane lint
	make -C cli lint
	make -C deploy lint
	make -C rapidui lint
	make -C scripts lint
	make -C tests lint
	make -C machineagent lint

.PHONY: lintcheck
lintcheck:
	make -C common lintcheck
	make -C controlplane lintcheck
	make -C cli lintcheck
	make -C deploy lintcheck
	make -C rapidui lintcheck
	make -C scripts lintcheck
	make -C tests lintcheck
	make -C machineagent lintcheck

.PHONY: formatcheck
formatcheck:
	make -C common formatcheck
	make -C controlplane formatcheck
	make -C cli formatcheck
	make -C deploy formatcheck
	make -C rapidui formatcheck
	make -C scripts formatcheck
	make -C tests formatcheck
	make -C machineagent formatcheck

.PHONY: typecheck
typecheck:
	make -C common typecheck
	make -C controlplane typecheck
	make -C cli typecheck
	make -C deploy typecheck
	make -C rapidui typecheck
	make -C scripts typecheck
	make -C tests typecheck
	make -C machineagent typecheck

.PHONY: check
check:
	make formatcheck
	make lintcheck
	#make typecheck  # TODO: Enable once mypy passes

.PHONY: install
install:
	make -C sdk_controlplane install
	make -C common install
	make -C controlplane install
	make -C cli install
	make -C deploy install
	make -C rapidui install
	make -C scripts install
	make -C tests install
	make -C machineagent install

.PHONY: install-dev
install-dev:
	make -C sdk_controlplane install-dev
	make -C common install-dev
	make -C controlplane install-dev
	make -C cli install-dev
	make -C deploy install-dev
	make -C rapidui install-dev
	make -C scripts install-dev
	make -C tests install-dev
	make -C machineagent install-dev


.PHONY: pre-commit-install
pre-commit-install:
	cp pre-commit .git/hooks/pre-commit

.PHONY: pre-commit-uninstall
pre-commit-uninstall:
	rm .git/hooks/pre-commit


.PHONY: validate-openapi-spec
validate-openapi-spec:
	openapi-generator validate -i controlplane/openapi.json

.PHONY: generate-sdk
generate-sdk: delete-sdk
	make -C controlplane gen-openapi-spec
	openapi-generator generate \
	  --input-spec controlplane/openapi.json \
	  --generator-name python \
	  --output sdk_controlplane \
	  --additional-properties=packageName=centrality_controlplane_sdk,packageVersion=0.0.1,projectName=centrality-controlplane-sdk
	  cp Makefile_sdk_controlplane sdk_controlplane/Makefile

.PHONY: delete-sdk
delete-sdk:
	rm -rf sdk_controlplane


.PHONY: delete-dump-db
delete-dump-db:
	find . -name 'dump.db' -type f -delete

# Run all codegen steps to ensure that the the current code is up-to-date
# NOTE: the order matters because generate-sdk depends on the openapi.json file which is generated from the FastAPI
# code which is partially codegen'd.
.PHONY: codegen
codegen:
	make -C scripts codegen
	make generate-sdk


.PHONY: clean
clean:
	make delete-dump-db
	docker compose down
	docker compose rm -f
	make pre-commit-install
	make codegen
	make install-dev
	docker compose build


