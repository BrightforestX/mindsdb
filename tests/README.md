## Test Structure

Our tests are organized into several subdirectories, each focusing on different aspects of our application:

* api: Contains tests related to the MindsDB's API endpoints.
* bdd: Contains Behavior-Driven Development (BDD) tests using pytest-bdd-ng
* integration: Contains the integration tests
* load: Contains the load tests
* scripts: Scripts and utilitis used for tests
* unit: This directory contains the unit tests:
        * handlers: A subset of unit tests specifically targeting data handlers.
        * ml_handlers: A subset of unit tests specifically targeting ML handlers.

## Installation

To run the tests, you need to install the necessary dependencies. You can do this by running the following command:

```
pip install -r requirements/requirements.txt -r requirements/requirements-test.txt
```

This command will install all the required packages as listed in requirements-test.txt and the requirements.txt files.

> Note: You will also need to install the dependencies required by any of the integrations that the tests you are running use. This can be done by running `pip install .[<integration_name>]` in the root directory of the repository. 

## Runing tests

### Unit and Integration Tests

To execute unit or integration tests, use the following pytest command:

```
pytest -vx <test_dir>
```

For example, to run the unit tests for the handlers, use the following command:

```
pytest -vx tests/unit/handlers
```

### Load Tests

For load testing, we use `locust`:
```
locust -f test_start.py --headless -u <number_of_users> -r <spawn_rate>
```
Options:

 *   --headless: Runs Locust in headless mode without the web UI.
 *   -u: Specifies the total number of users to simulate.
 *   -r: Defines the spawn rate of users, i.e the number of users to spawn per second.

 > Note: The load tests require an environment variable called `INTEGRATIONS_CONFIG` to be set containing information related to the testing environments used. These environments will also need be pre-loaded with the necessary data for the tests to run successfully.

## Generating Test Reports

We use `pytest` for running tests and `coveralls` for generating test coverage reports. To run the tests and generate a coverage report, use the following command:

```
pytest --cov=<code_dir> <test_dir> && coveralls
```

For example, to run tests for the HTTP API, use the following command:

```
pytest --cov=mindsdb/api/http tests/unit/api/http && coveralls
```

For the above command to be successful, you need to either have the `COVERALLS_REPO_TOKEN` environment variable set to your Coveralls token or have a `.coveralls.yml` file in the root directory of the repository with the token.

Otherwise, you simply run the following command:

```
pytest --cov=<code_dir> <test_dir>
```

## BDD Testing

We use Behavior-Driven Development (BDD) for all new features, providing human-readable specifications of system behavior. BDD tests complement existing unit and integration tests.

### BDD Frameworks

We support two BDD frameworks:

1. **pytest-bdd-ng** - Integrated with pytest, located in `tests/bdd/`
2. **Behave** - Standalone BDD framework, located in `features/`

### Running BDD Tests

#### pytest-bdd-ng Tests

```bash
# Run all pytest-bdd-ng tests
make bdd_tests

# Run with coverage
make bdd_coverage

# Run in debug mode
make bdd_tests_debug

# Run specific feature
pytest tests/bdd/features/api/mysql_api.feature
```

#### Behave Tests

```bash
# Run all Behave tests
make behave_tests

# Run with specific tags
make behave_tests_tags TAGS='@api,@mysql'

# Run in debug mode
make behave_tests_debug
```

### When to Use BDD vs Unit Tests

- **BDD Tests**: Use for new features, integration scenarios, and user-facing behavior
- **Unit Tests**: Use for testing individual functions, classes, and components
- **Integration Tests**: Use for testing component interactions (existing tests remain unchanged)

### BDD Documentation

- **pytest-bdd-ng**: See [tests/bdd/README.md](bdd/README.md)
- **Behave**: See [features/README.md](../features/README.md)

### Roadmap Generation

Generate a BDD-aligned roadmap from feature files and test results:

```bash
# Generate roadmap (uses test results if available)
python scripts/generate_bdd_roadmap.py

# With options
python scripts/generate_bdd_roadmap.py --verbose --test-results-dir reports/
```

This generates `docs/BDD_ROADMAP.md` with:
- All features and scenarios
- Test status indicators: `[x]` passing, `[ ]` failing/not implemented, `[~]` partial, `[S]` skipped
- Coverage statistics (passing/failing/not implemented percentages)
- Unmapped scenarios (scenarios without corresponding tests)

**Status Indicators:**
- `[x]` - Scenario passing all tests
- `[ ]` - Scenario failing or not implemented
- `[~]` - Scenario partially passing (some steps failing)
- `[S]` - Scenario skipped

The roadmap automatically updates based on test execution results from `reports/pytest-bdd-report.json` and `reports/behave.json`.