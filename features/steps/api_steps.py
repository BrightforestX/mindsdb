"""
Step definitions for Behave API tests.

These step definitions reuse existing test utilities from test_mysql_api.py
and use Behave's context object instead of pytest fixtures.
"""
import json
import mysql.connector
from behave import given, when, then
from tests.integration.conftest import MYSQL_API_ROOT, HTTP_API_ROOT
from tests.integration.flows.test_mysql_api import BaseStuff, Dlist


class BehaveBaseStuff(BaseStuff):
    """Extended BaseStuff for Behave tests with context storage."""

    def __init__(self, context):
        self.context = context
        self.use_binary = False
        self.query_result = None
        self.query_error = None

    def query(self, _query, encoding="utf-8", with_description=False):
        """Execute query and store result in context."""
        try:
            result = super().query(_query, encoding, with_description)
            self.query_result = result
            self.context.test_data["last_query_result"] = result
            return result
        except Exception as e:
            self.query_error = str(e)
            self.context.test_data["last_query_error"] = str(e)
            raise


def before_scenario(context, scenario):
    """Initialize context before each scenario."""
    context.test_data = {}
    context.bdd_stuff = None


@given("MindsDB MySQL API is running")
def step_mindsdb_mysql_api_running(context):
    """Verify MindsDB MySQL API is accessible."""
    assert MYSQL_API_ROOT is not None
    context.test_data["mysql_root"] = MYSQL_API_ROOT


@given("I have a MySQL connection to MindsDB")
def step_mysql_connection(context):
    """Create and store MySQL connection in context."""
    context.mysql_connection = mysql.connector.connect(
        host=MYSQL_API_ROOT,
        port=47335,
        database="mindsdb",
        user="mindsdb",
    )
    context.test_data["mysql_connection"] = context.mysql_connection


@given("I have a MySQL connection using binary protocol")
def step_mysql_connection_binary(context):
    """Set binary protocol flag."""
    context.bdd_stuff = BehaveBaseStuff(context)
    context.bdd_stuff.use_binary = True
    context.test_data["use_binary"] = True


@given('I execute the query "{query}"')
def step_execute_query(context, query):
    """Execute a SQL query."""
    if not context.bdd_stuff:
        context.bdd_stuff = BehaveBaseStuff(context)
        context.bdd_stuff.use_binary = context.test_data.get("use_binary", False)

    try:
        result = context.bdd_stuff.query(query)
        context.test_data["last_query_result"] = result
        context.test_data["last_query_error"] = None
    except Exception as e:
        context.test_data["last_query_error"] = str(e)
        context.test_data["last_query_result"] = None
        raise


@given("I have PostgreSQL connection details:")
def step_postgres_connection_details(context):
    """Store PostgreSQL connection details from data table."""
    table = context.table
    if table:
        row = table[0]
        connection_data = {
            "host": row.get("host", "samples.mindsdb.com"),
            "port": row.get("port", "5432"),
            "user": row.get("user", "demo_user"),
            "password": row.get("password", "demo_password"),
            "database": row.get("database", "demo"),
            "schema": row.get("schema", "demo"),
        }
        context.test_data["postgres_details"] = connection_data


@when('I create a datasource named "{name}" with type "{db_type}"')
def step_create_datasource(context, name, db_type):
    """Create a datasource using the stored connection details."""
    if not context.bdd_stuff:
        context.bdd_stuff = BehaveBaseStuff(context)

    details = context.test_data.get("postgres_details", {})
    db_data = {
        "type": db_type,
        "connection_data": details,
    }
    context.bdd_stuff.create_database(name, db_data)
    context.test_data["created_datasource"] = name


@when("the query fails")
def step_query_fails(context):
    """Verify that the query failed."""
    error = context.test_data.get("last_query_error")
    assert error is not None, "Expected query to fail, but it succeeded"


@then("the query should return results")
def step_query_returns_results(context):
    """Verify query returned results."""
    result = context.test_data.get("last_query_result")
    assert result is not None, "Expected query to return results"
    assert isinstance(result, (list, dict, Dlist)), "Result should be a list or dict"


@then("the results should contain at least {count:d} row")
def step_results_contain_rows(context, count):
    """Verify results contain at least N rows."""
    result = context.test_data.get("last_query_result")
    assert result is not None, "No query results found"
    if isinstance(result, list):
        assert len(result) >= count, f"Expected at least {count} rows, got {len(result)}"
    elif isinstance(result, Dlist):
        assert len(result) >= count, f"Expected at least {count} rows, got {len(result)}"


@then('the datasource "{name}" should be created successfully')
def step_datasource_created(context, name):
    """Verify datasource was created."""
    assert context.bdd_stuff is not None, "BDD context not initialized"
    context.bdd_stuff.validate_database_creation(name)


@then("I should be able to query the datasource")
def step_can_query_datasource(context):
    """Verify datasource can be queried."""
    name = context.test_data.get("created_datasource")
    assert name is not None, "No datasource was created"
    # Try to query information_schema to verify connection
    result = context.bdd_stuff.query(f"SELECT name FROM information_schema.databases WHERE name='{name}';")
    assert "name" in result or len(result) > 0, f"Datasource {name} not found"


@then("I should receive an error message")
def step_receive_error_message(context):
    """Verify an error message was received."""
    error = context.test_data.get("last_query_error")
    assert error is not None, "Expected an error message, but none was found"
    assert len(error) > 0, "Error message should not be empty"


@then("the error should indicate the table does not exist")
def step_error_indicates_table_not_found(context):
    """Verify error indicates table not found."""
    error = context.test_data.get("last_query_error", "").lower()
    assert (
        "table" in error or "not found" in error or "does not exist" in error
    ), f"Error should indicate table not found, got: {error}"


@then("the query should return results using binary protocol")
def step_query_returns_results_binary(context):
    """Verify query returned results using binary protocol."""
    result = context.test_data.get("last_query_result")
    assert result is not None, "Expected query to return results"
    assert isinstance(result, (list, dict, Dlist)), "Result should be a list or dict"


def after_scenario(context, scenario):
    """Cleanup after each scenario."""
    if hasattr(context, "mysql_connection") and context.mysql_connection:
        try:
            context.mysql_connection.close()
        except Exception:
            pass
