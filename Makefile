PYTEST_ARGS = -v -rs --disable-warnings -n auto --dist loadfile
PYTEST_ARGS_DEBUG = --runslow -vs -rs

DSI_PYTEST_ARGS = --run-dsi-tests
DSI_REPORT_ARGS = --json-report --json-report-file=reports/report.json

install_mindsdb:
	pip install -e .
	pip install -r requirements/requirements-dev.txt
	pre-commit install

install_handler:
	@if [[ -n "$(HANDLER_NAME)" ]]; then\
		pip install -e .[$(HANDLER_NAME)];\
	else\
		echo 'Please set $$HANDLER_NAME to the handler to install.';\
	fi
precommit:
	pre-commit install
	pre-commit run --files $$(git diff --cached --name-only)

format:
	pre-commit run --hook-stage manual

run_mindsdb:
	python -m mindsdb

run_mindsdb_full_apis:
	MINDSDB_APIS=http,mysql,jobs,tasks,ml_task_queue,litellm python -m mindsdb

check:
	python tests/scripts/check_requirements.py
	python tests/scripts/check_print_statements.py
	pre-commit install
	pre-commit run --files $$(git diff --cached --name-only)

build_docker:
	docker buildx build -t mdb --load -f docker/mindsdb.Dockerfile .

run_docker: build_docker
	docker run -it -p 47334:47334 mdb

# Docker Compose with custom remote database and config
# Usage: make run_docker_custom ENV=supabase
#        make run_docker_custom ENV=prod
#        make run_docker_custom ENV=dev
#        make run_docker_custom (defaults to dev)
run_docker_custom:
	@if [ -z "$(ENV)" ]; then \
		ENV=dev; \
	fi; \
	ENV_FILE="env/$$ENV.env"; \
	if [ ! -f "$$ENV_FILE" ]; then \
		echo "Error: Environment file $$ENV_FILE does not exist."; \
		echo "Available environments: dev, prod, supabase, local"; \
		echo "Usage: make run_docker_custom ENV=dev"; \
		exit 1; \
	fi; \
	echo "Using environment file: $$ENV_FILE"; \
	ENV_FILE=$$ENV_FILE docker-compose -f docker-compose.custom.yml up -d

stop_docker_custom:
	docker-compose -f docker-compose.custom.yml down

logs_docker_custom:
	docker-compose -f docker-compose.custom.yml logs -f

# Usage: make rebuild_docker_custom ENV=supabase
rebuild_docker_custom:
	@if [ -z "$(ENV)" ]; then \
		ENV=dev; \
	fi; \
	ENV_FILE="env/$$ENV.env"; \
	if [ ! -f "$$ENV_FILE" ]; then \
		echo "Error: Environment file $$ENV_FILE does not exist."; \
		echo "Available environments: dev, prod, supabase, local"; \
		echo "Usage: make rebuild_docker_custom ENV=dev"; \
		exit 1; \
	fi; \
	echo "Using environment file: $$ENV_FILE"; \
	ENV_FILE=$$ENV_FILE docker-compose -f docker-compose.custom.yml up -d --build

integration_tests:
	pytest $(PYTEST_ARGS) tests/integration/ -k "not test_auth"
	pytest $(PYTEST_ARGS) tests/integration/ -k test_auth  # Run this test separately because it alters the auth requirements, which breaks other tests

integration_tests_slow:
	pytest --runslow $(PYTEST_ARGS) tests/integration/ -k "not test_auth"
	pytest --runslow $(PYTEST_ARGS) tests/integration/ -k test_auth

integration_tests_debug:
	pytest $(PYTEST_ARGS_DEBUG) tests/integration/

datasource_integration_tests:
	@echo "--- Running Datasource Integration (DSI) Tests ---"
	# Ensure the reports directory exists before running tests
	mkdir -p reports
	# Added DSI_REPORT_ARGS to generate JSON report
	pytest $(PYTEST_ARGS) $(DSI_PYTEST_ARGS) $(DSI_REPORT_ARGS) tests/integration/handlers/

datasource_integration_tests_debug:
	@echo "--- Running Datasource Integration (DSI) Tests (Debug) ---"
	mkdir -p reports
	pytest $(PYTEST_ARGS_DEBUG) $(DSI_PYTEST_ARGS) $(DSI_REPORT_ARGS) tests/integration/handlers/

unit_tests:
	# We have to run executor tests separately because they do weird things that break everything else
	env PYTHONPATH=./ pytest $(PYTEST_ARGS) tests/unit/executor/
	pytest $(PYTEST_ARGS) --ignore=tests/unit/executor tests/unit/

unit_tests_slow:
	env PYTHONPATH=./ pytest --runslow $(PYTEST_ARGS) tests/unit/executor/  # We have to run executor tests separately because they do weird things that break everything else
	pytest --runslow $(PYTEST_ARGS) --ignore=tests/unit/executor tests/unit/

unit_tests_debug:
	env PYTHONPATH=./ pytest $(PYTEST_ARGS_DEBUG) tests/unit/executor/
	pytest $(PYTEST_ARGS_DEBUG) --ignore=tests/unit/executor tests/unit/

# BDD Tests (pytest-bdd-ng)
bdd_tests:
	@echo "--- Running pytest-bdd-ng Tests ---"
	mkdir -p reports
	pytest $(PYTEST_ARGS) tests/bdd/ --json-report --json-report-file=reports/pytest-bdd-report.json

bdd_tests_slow:
	@echo "--- Running pytest-bdd-ng Tests (Slow) ---"
	mkdir -p reports
	pytest --runslow $(PYTEST_ARGS) tests/bdd/ --json-report --json-report-file=reports/pytest-bdd-report.json

bdd_tests_debug:
	@echo "--- Running pytest-bdd-ng Tests (Debug) ---"
	mkdir -p reports
	pytest $(PYTEST_ARGS_DEBUG) tests/bdd/ --json-report --json-report-file=reports/pytest-bdd-report.json

bdd_coverage:
	@echo "--- Running pytest-bdd-ng Tests with Coverage ---"
	mkdir -p reports
	pytest $(PYTEST_ARGS) --cov=mindsdb --cov-report=html --cov-report=term tests/bdd/ --json-report --json-report-file=reports/pytest-bdd-report.json

# Behave Tests
behave_tests:
	@echo "--- Running Behave Tests ---"
	mkdir -p reports
	behave

behave_tests_slow:
	@echo "--- Running Behave Tests (Slow) ---"
	mkdir -p reports
	behave --tags=@slow

behave_tests_debug:
	@echo "--- Running Behave Tests (Debug) ---"
	mkdir -p reports
	behave --verbose

behave_tests_tags:
	@echo "--- Running Behave Tests with Tags ---"
	@if [ -z "$(TAGS)" ]; then \
		echo "Usage: make behave_tests_tags TAGS='@api,@mysql'"; \
		exit 1; \
	fi
	mkdir -p reports
	behave --tags=$(TAGS)

.PHONY: install_mindsdb install_handler precommit format run_mindsdb check build_docker run_docker run_docker_custom stop_docker_custom logs_docker_custom rebuild_docker_custom integration_tests integration_tests_slow integration_tests_debug datasource_integration_tests datasource_integration_tests_debug unit_tests unit_tests_slow unit_tests_debug bdd_tests bdd_tests_slow bdd_tests_debug bdd_coverage behave_tests behave_tests_slow behave_tests_debug behave_tests_tags