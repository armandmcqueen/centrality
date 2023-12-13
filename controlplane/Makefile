# lint with ruff
.PHONY: lint
lint: format
	ruff check .

# format with ruff
.PHONY: format
format:
	ruff format .

.PHONY: rundb
rundb:
	docker run -d --rm --name datastore-postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:16.1

.PHONY: stopdb
stopdb:
	docker stop datastore-postgres

.PHONY: resetdb
resetdb:
	python controlplane/cli.py reset-datastore

.PHONY: psql
psql:
	PGPASSWORD=postgres psql --no-password -h localhost -U postgres

.PHONY: gen-openapi-spec
gen-openapi-spec:
	python controlplane/cli.py openapi > ../common/common/sdks/controlplane/openapi.json

.PHONY: launch
launch:
	python controlplane/cli.py launch




