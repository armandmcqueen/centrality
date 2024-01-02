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
	ruff format --check .

.PHONY: typecheck
typecheck:
	mypy --strict .

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
	python controlplane/cli.py openapi > openapi.json

.PHONY: launch
launch:
	python controlplane/cli.py launch --postgres-host localhost

.PHONY: install
install:
	pip install -e .

.PHONY: install-dev
install-dev:
	pip install -e ".[dev]"



