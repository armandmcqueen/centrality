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
	# TODO: Incorporate CentralityCommon tests
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
	make -C vmagent lint

.PHONY: lintcheck
lintcheck:
	make -C common lintcheck
	make -C controlplane lintcheck
	make -C cli lintcheck
	make -C deploy lintcheck
	make -C rapidui lintcheck
	make -C scripts lintcheck
	make -C tests lintcheck
	make -C vmagent lintcheck

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

.PHONY: check
check:
	make formatcheck
	make lintcheck
	#make typecheck  # TODO: Enable once mypy passes

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
generate-sdk:
	make -C controlplane gen-openapi-spec
	openapi-generator generate \
	  --input-spec controlplane/openapi.json \
	  --generator-name python \
	  --output sdk_controlplane \
	  --additional-properties=packageName=controlplane_sdk,packageVersion=0.0.1,projectName=centrality-controlplane-sdk
	#  --additional-properties=packageName=controlplane_sdk,packageVersion=0.0.1,projectName=centrality-controlplane-sdk,generateSourceCodeOnly=true
#	openapi-generator generate \
#	  --input-spec controlplane/openapi.json \
#	  --generator-name python-pydantic-v1 \
#	  --output sdk_controlplane \
#	  --additional-properties=packageName=controlplane_sdk,packageVersion=0.0.1,projectName=centrality-controlplane-sdk
	#  --additional-properties=packageName=controlplane_sdk,packageVersion=0.0.1,projectName=centrality-controlplane-sdk,generateSourceCodeOnly=true

.PHONY: delete-sdk
delete-sdk:
	#rm -rf common/common/sdks/controlplane/gen
	rm -rf sdk_controlplane
