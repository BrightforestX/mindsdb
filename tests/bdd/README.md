# pytest-bdd-ng Testing Guide

## Overview

This directory contains Behavior-Driven Development (BDD) tests using `pytest-bdd-ng`, a modern pytest plugin that provides full Gherkin syntax support. These tests complement existing unit and integration tests by providing a human-readable specification of system behavior.

## Directory Structure

```
tests/bdd/
├── features/          # Gherkin feature files (.feature)
│   ├── api/          # API-related features
│   ├── models/       # Model prediction and training features
│   ├── handlers/     # Data handler features
│   └── integrations/ # Integration features
├── step_defs/        # Step definition implementations
└── conftest.py       # Shared pytest fixtures
```

## Writing Feature Files

Feature files use Gherkin syntax to describe behavior in plain language:

```gherkin
Feature: MySQL API Connection
  As a developer
  I want to test MySQL API functionality
  So that I can ensure API behavior matches requirements

  Scenario: Execute a simple query
    Given MindsDB MySQL API is running
    When I execute the query "SHOW DATABASES"
    Then the query should return results
```

### Feature File Best Practices

1. **Use descriptive feature names** that clearly indicate what is being tested
2. **Include user stories** in the Feature description (As a... I want... So that...)
3. **Tag scenarios** appropriately:
   - `@api` - API-related tests
   - `@slow` - Tests that take longer to run
   - `@mysql` - MySQL-specific tests
   - `@skip` - Tests to skip (use `~@skip` to exclude)
4. **Keep scenarios focused** - Each scenario should test one specific behavior
5. **Use Background** for common setup steps

## Step Definitions

Step definitions map Gherkin steps to Python code. They are located in `tests/bdd/step_defs/`.

### Example Step Definition

```python
from pytest_bdd import given, when, then, parsers

@given(parsers.parse('I execute the query "{query}"'))
def execute_query(bdd_context, query):
    """Execute a SQL query."""
    bdd_stuff = bdd_context["test_data"].get("bdd_stuff")
    result = bdd_stuff.query(query)
    bdd_context["test_data"]["last_query_result"] = result
```

### Reusing Existing Test Code

Step definitions should reuse existing test utilities:

- **BaseStuff class** from `tests/integration/flows/test_mysql_api.py` - For database operations
- **Fixtures** from `tests/conftest.py` and `tests/integration/conftest.py`
- **Test infrastructure** like `MYSQL_API_ROOT`, `HTTP_API_ROOT`

### Step Definition Patterns

1. **Given** - Setup steps (preconditions)
2. **When** - Action steps (what we're testing)
3. **Then** - Assertion steps (expected outcomes)
4. **And/But** - Continuation of previous step type

## Running Tests

### Basic Usage

```bash
# Run all BDD tests
make bdd_tests

# Run with pytest directly
pytest tests/bdd/

# Run specific feature
pytest tests/bdd/features/api/mysql_api.feature

# Run tests with specific tags
pytest tests/bdd/ -m "api and mysql"
```

### Debug Mode

```bash
# Run in debug mode (verbose, stops on first failure)
make bdd_tests_debug

# Or with pytest
pytest -vs tests/bdd/
```

### Coverage

```bash
# Generate coverage report
make bdd_coverage

# Or with pytest
pytest --cov=mindsdb --cov-report=html tests/bdd/
```

### Slow Tests

```bash
# Include slow tests
make bdd_tests_slow

# Or with pytest
pytest --runslow tests/bdd/
```

## Integration with Existing Tests

### Reusing Fixtures

BDD tests can use existing pytest fixtures:

```python
# In conftest.py
from tests.integration.conftest import train_finetune_lock

@pytest.fixture
def bdd_context(train_finetune_lock):
    """BDD context with existing fixtures."""
    context = {"lock": train_finetune_lock}
    return context
```

### Sharing Test Utilities

Step definitions can import and use existing test utilities:

```python
from tests.integration.flows.test_mysql_api import BaseStuff

class BDDBaseStuff(BaseStuff):
    """Extended BaseStuff for BDD tests."""
    def __init__(self, context):
        self.context = context
        super().__init__()
```

## Best Practices for New Features

1. **Write BDD scenarios first** - Define behavior before implementation
2. **Keep scenarios independent** - Each scenario should be able to run standalone
3. **Use tags effectively** - Tag scenarios for easy filtering
4. **Reuse step definitions** - Don't duplicate step logic
5. **Clean up after tests** - Use context cleanup functions
6. **Document complex steps** - Add docstrings to step definitions

## Configuration

pytest-bdd-ng is configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
bdd_features_base_dir = "tests/bdd/features"
bdd_steps_base_dir = "tests/bdd/step_defs"
```

## JSON Reports

Tests generate JSON reports for roadmap generation:

```bash
pytest --json-report --json-report-file=reports/pytest-bdd-report.json tests/bdd/
```

Reports are stored in `reports/pytest-bdd-report.json` and can be used by the roadmap generation script.

## Test Result Integration

The roadmap generator automatically reads test results and updates scenario status:

### Status Indicators

- `- [x]` - Scenario implemented and passing
- `- [ ]` - Scenario not implemented or failing
- `- [~]` - Scenario partially implemented (some steps failing)
- `- [S]` - Scenario skipped

### Coverage Statistics

The roadmap includes coverage statistics showing:
- Total scenarios
- Passing scenarios (percentage)
- Failing scenarios (percentage)
- Not implemented scenarios (percentage)
- Skipped scenarios (percentage)
- Overall coverage percentage

### Generating Roadmap with Test Results

```bash
# Run tests first to generate reports
make bdd_tests
make behave_tests

# Generate roadmap (automatically uses test results)
python scripts/generate_bdd_roadmap.py

# With custom test results directory
python scripts/generate_bdd_roadmap.py --test-results-dir custom/reports

# Verbose mode (shows matching details)
python scripts/generate_bdd_roadmap.py --verbose

# Strict mode (only mark passing if all tests pass)
python scripts/generate_bdd_roadmap.py --strict
```

### Troubleshooting

**Unmapped Scenarios**: If scenarios appear as "not implemented" but tests exist:
- Check that test result files are in the correct location (`reports/`)
- Verify scenario names match between feature files and test results
- Use `--verbose` flag to see detailed matching information
- Check that test nodeids/URIs match feature file paths

**Missing Test Results**: If test results are not found:
- Ensure tests have been run: `make bdd_tests` and `make behave_tests`
- Check that JSON reports are being generated
- Verify `reports/` directory exists
- Use `--test-results-dir` to specify custom location

## Troubleshooting

### Step Definition Not Found

- Ensure step definition file is in `tests/bdd/step_defs/`
- Check that step definition is imported in `__init__.py` or directly
- Verify step text matches exactly (case-sensitive)

### Fixture Not Found

- Check that fixture is defined in `tests/bdd/conftest.py`
- Ensure fixture is imported from existing conftest files if needed
- Verify fixture scope matches test requirements

### Context Not Available

- Ensure `bdd_context` fixture is used in step definition
- Check that context is initialized in Background or Given steps
- Verify context keys match what step definitions expect

## Resources

- [pytest-bdd-ng Documentation](https://github.com/cucumber/pytest-bdd-ng)
- [Gherkin Syntax Reference](https://cucumber.io/docs/gherkin/)
- [pytest Documentation](https://docs.pytest.org/)
