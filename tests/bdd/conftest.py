"""
Shared fixtures for pytest-bdd-ng tests.

This module provides fixtures that reuse existing test infrastructure
from tests/conftest.py and tests/integration/conftest.py.
"""
import pytest
import os
from filelock import FileLock

# Import existing test infrastructure
from tests.integration.conftest import (
    HTTP_API_ROOT,
    MYSQL_API_ROOT,
    train_finetune_lock,
)

# Re-export existing fixtures for BDD tests
__all__ = [
    "HTTP_API_ROOT",
    "MYSQL_API_ROOT",
    "train_finetune_lock",
    "bdd_context",
    "mysql_connection",
]


@pytest.fixture(scope="function")
def bdd_context():
    """
    BDD-specific context fixture that provides a shared context object
    for storing test data between steps.
    """
    context = {
        "api_root": HTTP_API_ROOT,
        "mysql_root": MYSQL_API_ROOT,
        "test_data": {},
        "cleanup": [],
    }
    yield context
    # Cleanup after test
    for cleanup_func in context.get("cleanup", []):
        try:
            cleanup_func()
        except Exception as e:
            print(f"Cleanup error: {e}")


@pytest.fixture(scope="function")
def mysql_connection():
    """
    MySQL connection fixture for BDD tests.
    Reuses the same connection pattern from existing integration tests.
    """
    import mysql.connector

    connection = mysql.connector.connect(
        host=MYSQL_API_ROOT,
        port=47335,
        database="mindsdb",
        user="mindsdb",
    )
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def use_binary(request):
    """
    Fixture to control whether to use binary protocol in MySQL connections.
    Can be parametrized in BDD tests.
    """
    return getattr(request, "param", False)
