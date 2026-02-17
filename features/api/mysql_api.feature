Feature: MySQL API Connection and Query Execution
  As a developer
  I want to test MySQL API functionality through BDD
  So that I can ensure API behavior matches requirements

  Background:
    Given MindsDB MySQL API is running
    And I have a MySQL connection to MindsDB

  @api @mysql
  Scenario: Execute a simple SELECT query
    Given I execute the query "SHOW DATABASES"
    Then the query should return results
    And the results should contain at least 1 row

  @api @mysql @slow
  Scenario: Create a PostgreSQL datasource
    Given I have PostgreSQL connection details:
      | host | samples.mindsdb.com |
      | port | 5432 |
      | user | demo_user |
      | password | demo_password |
      | database | demo |
      | schema | demo |
    When I create a datasource named "test_demo_postgres" with type "postgres"
    Then the datasource "test_demo_postgres" should be created successfully
    And I should be able to query the datasource

  @api @mysql
  Scenario: Handle invalid query syntax
    Given I execute the query "SELECT * FROM invalid_table"
    When the query fails
    Then I should receive an error message
    And the error should indicate the table does not exist

  @api @mysql
  Scenario: Query with binary protocol
    Given I have a MySQL connection using binary protocol
    When I execute the query "SHOW TABLES"
    Then the query should return results using binary protocol
