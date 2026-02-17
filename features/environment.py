"""
Behave environment configuration.

This file contains hooks that run before and after scenarios,
providing setup and teardown functionality.
"""
from behave import before_scenario, after_scenario


def before_scenario(context, scenario):
    """Initialize context before each scenario."""
    context.test_data = {}
    context.bdd_stuff = None


def after_scenario(context, scenario):
    """Cleanup after each scenario."""
    if hasattr(context, "mysql_connection") and context.mysql_connection:
        try:
            context.mysql_connection.close()
        except Exception:
            pass
