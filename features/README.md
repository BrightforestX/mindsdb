# Behave BDD Testing Guide

## Overview

This directory contains Behavior-Driven Development (BDD) tests using `Behave`, a standalone BDD framework for Python. Behave tests are separate from pytest tests and provide an alternative approach to BDD testing.

## Directory Structure

```
features/
├── api/              # API-related feature files
├── models/           # Model prediction and training features
├── handlers/         # Data handler features
├── integrations/     # Integration features
└── steps/            # Step definition implementations
```

## Configuration

Behave is configured in `behave.ini`:

```ini
[behave]
paths = features
step_definitions = features/steps
format = json.pretty,html
outfiles = reports/behave.json,reports/behave.html
```

## Writing Feature Files

Feature files use Gherkin syntax and are located in the `features/` directory:

```gherkin
Feature: MySQL API Connection
  As a developer
  I want to test MySQL API functionality
  So that I can ensure API behavior matches requirements

  Background:
    Given MindsDB MySQL API is running

  Scenario: Execute a simple query
    When I execute the query "SHOW DATABASES"
    Then the query should return results
```

### Feature File Organization

- **api/** - API endpoint testing
- **models/** - Model training and prediction
- **handlers/** - Data source handlers
- **integrations/** - Integration scenarios

## Step Definitions

Step definitions are located in `features/steps/` and use Behave's decorators:

```python
from behave import given, when, then

@given("MindsDB MySQL API is running")
def step_mindsdb_api_running(context):
    """Verify MindsDB MySQL API is accessible."""
    assert MYSQL_API_ROOT is not None
```

### Context Object

Behave uses a `context` object to share data between steps:

```python
@given("I execute the query {query}")
def step_execute_query(context, query):
    """Execute a SQL query."""
    context.test_data["last_query"] = query
    result = execute_sql(query)
    context.test_data["last_result"] = result
```

## Running Tests

### Basic Usage

```bash
# Run all Behave tests
make behave_tests

# Or directly
behave

# Run specific feature
behave features/api/mysql_api.feature

# Run with specific tags
behave --tags=@api
behave --tags=@api,@mysql
behave --tags=~@slow  # Exclude slow tests
```

### Debug Mode

```bash
# Run in verbose mode
make behave_tests_debug

# Or directly
behave --verbose
```

### Slow Tests

```bash
# Run only slow tests
make behave_tests_slow

# Or directly
behave --tags=@slow
```

### Custom Tags

```bash
# Run tests with custom tags
make behave_tests_tags TAGS='@api,@mysql'
```

## Environment Configuration

Behave uses `features/environment.py` for setup and teardown:

```python
def before_scenario(context, scenario):
    """Initialize context before each scenario."""
    context.test_data = {}

def after_scenario(context, scenario):
    """Cleanup after each scenario."""
    # Cleanup code here
```

## Reports

Behave generates multiple report formats:

- **JSON Report**: `reports/behave.json` - Machine-readable format
- **HTML Report**: `reports/behave.html` - Human-readable format

Reports are automatically generated when running tests.

## Integration with Existing Tests

### Reusing Test Utilities

Step definitions can import and use existing test utilities:

```python
from tests.integration.flows.test_mysql_api import BaseStuff

class BehaveBaseStuff(BaseStuff):
    """Extended BaseStuff for Behave tests."""
    def __init__(self, context):
        self.context = context
        super().__init__()
```

### Using Test Infrastructure

Step definitions can use existing test infrastructure:

```python
from tests.integration.conftest import MYSQL_API_ROOT, HTTP_API_ROOT

@given("I have a MySQL connection")
def step_mysql_connection(context):
    """Create MySQL connection."""
    context.mysql_connection = mysql.connector.connect(
        host=MYSQL_API_ROOT,
        port=47335,
        database="mindsdb",
        user="mindsdb",
    )
```

## When to Use Behave vs pytest-bdd-ng

### Use Behave when:
- You want a standalone BDD framework
- You prefer Behave's context object model
- You need Behave-specific features
- You want to keep BDD tests completely separate from pytest

### Use pytest-bdd-ng when:
- You want tight integration with pytest
- You need to use existing pytest fixtures
- You want to run BDD tests alongside unit/integration tests
- You prefer pytest's plugin ecosystem

## Best Practices

1. **Write clear scenarios** - Use descriptive language that non-technical stakeholders can understand
2. **Use Background** - Common setup steps should go in Background
3. **Tag appropriately** - Use tags to organize and filter tests
4. **Keep scenarios independent** - Each scenario should be able to run standalone
5. **Clean up resources** - Use `after_scenario` to clean up connections, files, etc.
6. **Reuse step definitions** - Don't duplicate step logic
7. **Document complex steps** - Add docstrings to step definitions

## Troubleshooting

### Step Definition Not Found

- Ensure step definition file is in `features/steps/`
- Check that step text matches exactly (case-sensitive)
- Verify step definition is imported

### Context Issues

- Ensure context is initialized in `before_scenario`
- Check that context attributes are set before use
- Verify context cleanup in `after_scenario`

### Import Errors

- Ensure Python path includes project root
- Check that imports use absolute paths from project root
- Verify all dependencies are installed

## Resources

- [Behave Documentation](https://behave.readthedocs.io/)
- [Gherkin Syntax Reference](https://cucumber.io/docs/gherkin/)
- [Behave Examples](https://github.com/behave/behave.example)
