"""
Step definitions for pytest-bdd-ng API tests.

These step definitions reuse existing test utilities from test_mysql_api.py
and leverage the BaseStuff class patterns.
"""
import json
import mysql.connector
from pytest_bdd import given, when, then, parsers
from tests.integration.conftest import MYSQL_API_ROOT, HTTP_API_ROOT
from tests.integration.flows.test_mysql_api import BaseStuff, Dlist


class BDDBaseStuff(BaseStuff):
    """Extended BaseStuff for BDD tests with context storage."""

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
            self.context["test_data"]["last_query_result"] = result
            return result
        except Exception as e:
            self.query_error = str(e)
            self.context["test_data"]["last_query_error"] = str(e)
            raise


@given("MindsDB MySQL API is running")
def mindsdb_mysql_api_running(bdd_context):
    """Verify MindsDB MySQL API is accessible."""
    # This is a background step - API should be running
    assert MYSQL_API_ROOT is not None
    bdd_context["test_data"]["mysql_root"] = MYSQL_API_ROOT


@given("I have a MySQL connection to MindsDB")
def mysql_connection(bdd_context, mysql_connection):
    """Store MySQL connection in context."""
    bdd_context["test_data"]["mysql_connection"] = mysql_connection


@given("I have a MySQL connection using binary protocol")
def mysql_connection_binary(bdd_context):
    """Set binary protocol flag."""
    bdd_stuff = BDDBaseStuff(bdd_context)
    bdd_stuff.use_binary = True
    bdd_context["test_data"]["bdd_stuff"] = bdd_stuff
    bdd_context["test_data"]["use_binary"] = True


@given(parsers.parse('I execute the query "{query}"'))
def execute_query(bdd_context, query):
    """Execute a SQL query."""
    bdd_stuff = bdd_context["test_data"].get("bdd_stuff")
    if not bdd_stuff:
        bdd_stuff = BDDBaseStuff(bdd_context)
        bdd_stuff.use_binary = bdd_context["test_data"].get("use_binary", False)
        bdd_context["test_data"]["bdd_stuff"] = bdd_stuff

    try:
        result = bdd_stuff.query(query)
        bdd_context["test_data"]["last_query_result"] = result
        bdd_context["test_data"]["last_query_error"] = None
    except Exception as e:
        bdd_context["test_data"]["last_query_error"] = str(e)
        bdd_context["test_data"]["last_query_result"] = None
        raise


@given(parsers.parse('I have PostgreSQL connection details:'))
def postgres_connection_details(bdd_context, datatable):
    """Store PostgreSQL connection details from data table."""
    details = {}
    for row in datatable:
        details[row["host"]] = row["host"]
        details[row["port"]] = row["port"]
        details[row["user"]] = row["user"]
        details[row["password"]] = row["password"]
        details[row["database"]] = row["database"]
        details[row["schema"]] = row["schema"]
        break  # Take first row

    # Convert to proper format
    connection_data = {
        "host": details.get("host", "samples.mindsdb.com"),
        "port": details.get("port", "5432"),
        "user": details.get("user", "demo_user"),
        "password": details.get("password", "demo_password"),
        "database": details.get("database", "demo"),
        "schema": details.get("schema", "demo"),
    }
    bdd_context["test_data"]["postgres_details"] = connection_data


@when(parsers.parse('I create a datasource named "{name}" with type "{db_type}"'))
def create_datasource(bdd_context, name, db_type):
    """Create a datasource using the stored connection details."""
    bdd_stuff = bdd_context["test_data"].get("bdd_stuff")
    if not bdd_stuff:
        bdd_stuff = BDDBaseStuff(bdd_context)
        bdd_context["test_data"]["bdd_stuff"] = bdd_stuff

    details = bdd_context["test_data"].get("postgres_details", {})
    db_data = {
        "type": db_type,
        "connection_data": details,
    }
    bdd_stuff.create_database(name, db_data)
    bdd_context["test_data"]["created_datasource"] = name


@when("the query fails")
def query_fails(bdd_context):
    """Verify that the query failed."""
    error = bdd_context["test_data"].get("last_query_error")
    assert error is not None, "Expected query to fail, but it succeeded"


@then("the query should return results")
def query_returns_results(bdd_context):
    """Verify query returned results."""
    result = bdd_context["test_data"].get("last_query_result")
    assert result is not None, "Expected query to return results"
    assert isinstance(result, (list, dict, Dlist)), "Result should be a list or dict"


@then(parsers.parse('the results should contain at least {count:d} row'))
def results_contain_rows(bdd_context, count):
    """Verify results contain at least N rows."""
    result = bdd_context["test_data"].get("last_query_result")
    assert result is not None, "No query results found"
    if isinstance(result, list):
        assert len(result) >= count, f"Expected at least {count} rows, got {len(result)}"
    elif isinstance(result, Dlist):
        assert len(result) >= count, f"Expected at least {count} rows, got {len(result)}"


@then(parsers.parse('the datasource "{name}" should be created successfully'))
def datasource_created(bdd_context, name):
    """Verify datasource was created."""
    bdd_stuff = bdd_context["test_data"].get("bdd_stuff")
    assert bdd_stuff is not None, "BDD context not initialized"
    bdd_stuff.validate_database_creation(name)


@then("I should be able to query the datasource")
def can_query_datasource(bdd_context):
    """Verify datasource can be queried."""
    name = bdd_context["test_data"].get("created_datasource")
    assert name is not None, "No datasource was created"
    # Try to query information_schema to verify connection
    bdd_stuff = bdd_context["test_data"].get("bdd_stuff")
    result = bdd_stuff.query(f"SELECT name FROM information_schema.databases WHERE name='{name}';")
    assert "name" in result or len(result) > 0, f"Datasource {name} not found"


@then("I should receive an error message")
def receive_error_message(bdd_context):
    """Verify an error message was received."""
    error = bdd_context["test_data"].get("last_query_error")
    assert error is not None, "Expected an error message, but none was found"
    assert len(error) > 0, "Error message should not be empty"


@then("the error should indicate the table does not exist")
def error_indicates_table_not_found(bdd_context):
    """Verify error indicates table not found."""
    error = bdd_context["test_data"].get("last_query_error", "").lower()
    assert (
        "table" in error or "not found" in error or "does not exist" in error
    ), f"Error should indicate table not found, got: {error}"


@then("the query should return results using binary protocol")
def query_returns_results_binary(bdd_context):
    """Verify query returned results using binary protocol."""
    result = bdd_context["test_data"].get("last_query_result")
    assert result is not None, "Expected query to return results"
    # Binary protocol should still return results
    assert isinstance(result, (list, dict, Dlist)), "Result should be a list or dict"
