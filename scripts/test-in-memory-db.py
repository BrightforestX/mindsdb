#!/usr/bin/env python3
"""
Test script for SurrealDB in-memory database using the official Python SDK.

This demonstrates using SurrealDB's embedded in-memory database which runs
directly within your Python application without needing a separate server.

Install: pip install surrealdb
Docs: https://github.com/surrealdb/surrealdb.py
"""

import asyncio
import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def log_step(step_num: int, description: str):
    """Log a test step."""
    logger.info(f"STEP {step_num}: {description}")


def log_success(message: str):
    """Log a success message."""
    logger.info(f"✅ SUCCESS: {message}")


def log_error(message: str):
    """Log an error message."""
    logger.error(f"❌ ERROR: {message}")


def log_data(label: str, data):
    """Log data with a label."""
    logger.info(f"   📊 {label}: {data}")


def log_schema(title: str, schema_data):
    """Log schema information with special formatting."""
    logger.info(f"   🏗️  {title}")
    if isinstance(schema_data, (list, dict)):
        import json
        logger.info(f"   {json.dumps(schema_data, indent=2, default=str)}")
    else:
        logger.info(f"   {schema_data}")


async def export_schema_async(db):
    """Export complete schema information to logs (async)."""
    logger.info("📋 EXPORTING DATABASE SCHEMA")
    logger.info("=" * 50)

    try:
        # Export namespace information
        log_step("SCHEMA-1", "Getting namespace information...")
        ns_info = await db.query("INFO FOR NS")
        log_success("Retrieved namespace info")
        log_schema("NAMESPACE INFO", ns_info)

        # Export database information
        log_step("SCHEMA-2", "Getting database information...")
        db_info = await db.query("INFO FOR DB")
        log_success("Retrieved database info")
        log_schema("DATABASE INFO", db_info)

        # Get table names from database info
        tables = db_info.get('tables', {}) if isinstance(db_info, dict) else {}
        table_names = list(tables.keys()) if isinstance(tables, dict) else []

        if table_names:
            logger.info(f"📊 Found {len(table_names)} tables: {', '.join(table_names)}")

            # Export schema for each table
            for i, table_name in enumerate(table_names, 1):
                log_step(f"SCHEMA-{i+2}", f"Getting schema for table '{table_name}'...")
                table_info = await db.query(f"INFO FOR TABLE {table_name}")
                log_success(f"Retrieved schema for '{table_name}'")
                log_schema(f"TABLE '{table_name}' SCHEMA", table_info)
        else:
            logger.info("📊 No tables found in database")

        logger.info("=" * 50)
        logger.info("✅ SCHEMA EXPORT COMPLETED")
        return True

    except Exception as e:
        log_error(f"Schema export failed: {type(e).__name__}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def export_schema_sync(db):
    """Export complete schema information to logs (sync)."""
    logger.info("📋 EXPORTING DATABASE SCHEMA")
    logger.info("=" * 50)

    try:
        # Export namespace information
        log_step("SCHEMA-1", "Getting namespace information...")
        ns_info = db.query("INFO FOR NS")
        log_success("Retrieved namespace info")
        log_schema("NAMESPACE INFO", ns_info)

        # Export database information
        log_step("SCHEMA-2", "Getting database information...")
        db_info = db.query("INFO FOR DB")
        log_success("Retrieved database info")
        log_schema("DATABASE INFO", db_info)

        # Get table names from database info
        tables = db_info.get('tables', {}) if isinstance(db_info, dict) else {}
        table_names = list(tables.keys()) if isinstance(tables, dict) else []

        if table_names:
            logger.info(f"📊 Found {len(table_names)} tables: {', '.join(table_names)}")

            # Export schema for each table
            for i, table_name in enumerate(table_names, 1):
                log_step(f"SCHEMA-{i+2}", f"Getting schema for table '{table_name}'...")
                table_info = db.query(f"INFO FOR TABLE {table_name}")
                log_success(f"Retrieved schema for '{table_name}'")
                log_schema(f"TABLE '{table_name}' SCHEMA", table_info)
        else:
            logger.info("📊 No tables found in database")

        logger.info("=" * 50)
        logger.info("✅ SCHEMA EXPORT COMPLETED")
        return True

    except Exception as e:
        log_error(f"Schema export failed: {type(e).__name__}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


async def test_async_in_memory():
    """Test async API with in-memory database."""
    logger.info("=" * 70)
    logger.info("🚀 Starting ASYNC in-memory database test")
    logger.info("=" * 70)

    try:
        from surrealdb import AsyncSurreal

        log_success("Imported AsyncSurreal from surrealdb")
    except ImportError as e:
        log_error(f"Failed to import surrealdb: {e}")
        log_error("Install with: pip install surrealdb")
        return False

    try:
        # Step 1: Connect to in-memory database
        log_step(1, "Connecting to in-memory database...")
        db = AsyncSurreal("mem://")
        await db.connect()
        log_success("Connected to in-memory database")

        # Step 2: Set namespace and database
        log_step(2, "Setting namespace and database...")
        await db.use("test_ns", "test_db")
        log_success("Set namespace='test_ns', database='test_db'")

        # Note: For embedded in-memory databases, no authentication is required

        # Step 3: Create a record
        log_step(3, "Creating a person record...")
        person = await db.create(
            "person",
            {
                "name": "John Doe",
                "age": 30,
                "email": "john@example.com",
                "tags": ["developer", "python"],
                "created_at": datetime.now().isoformat(),
            },
        )
        log_success("Created person record")
        log_data("Person", person)

        # Step 4: Create another record
        log_step(4, "Creating another person record...")
        person2 = await db.create(
            "person",
            {
                "name": "Jane Smith",
                "age": 25,
                "email": "jane@example.com",
                "tags": ["designer", "creative"],
                "created_at": datetime.now().isoformat(),
            },
        )
        log_success("Created second person record")
        log_data("Person", person2)

        # Step 5: Select all records
        log_step(5, "Selecting all person records...")
        people = await db.select("person")
        log_success(f"Retrieved {len(people)} records")
        for i, p in enumerate(people):
            log_data(f"Record {i + 1}", p)

        # Step 6: Query with SurrealQL
        log_step(6, "Querying with SurrealQL (age > 26)...")
        result = await db.query("SELECT * FROM person WHERE age > 26")
        log_success("Query executed")
        log_data("Query result", result)

        # Step 7: Update records
        log_step(7, "Updating all people (incrementing age by 1)...")
        update_result = await db.query("UPDATE person SET age = age + 1")
        log_success("Update executed")
        log_data("Update result", update_result)

        # Step 8: Verify update
        log_step(8, "Verifying update...")
        people = await db.select("person")
        for p in people:
            log_data(f"{p.get('name')}", f"age = {p.get('age')}")

        # Step 9: Export schema
        log_step(9, "Exporting database schema...")
        schema_exported = await export_schema_async(db)
        if schema_exported:
            log_success("Schema export completed")
        else:
            log_error("Schema export failed")

        # Step 10: Delete records
        log_step(9, "Deleting all person records...")
        await db.delete("person")
        remaining = await db.select("person")
        log_success(f"Deleted all records. Remaining: {len(remaining)}")

        # Close connection
        await db.close()
        log_success("Connection closed")

        logger.info("=" * 70)
        logger.info("✅ ASYNC test completed successfully!")
        logger.info("=" * 70)
        return True

    except Exception as e:
        log_error(f"Async test failed: {type(e).__name__}: {e}")
        import traceback

        logger.error(traceback.format_exc())
        return False


def test_sync_in_memory():
    """Test sync (blocking) API with in-memory database."""
    logger.info("")
    logger.info("=" * 70)
    logger.info("🚀 Starting SYNC in-memory database test")
    logger.info("=" * 70)

    try:
        from surrealdb import Surreal

        log_success("Imported Surreal from surrealdb")
    except ImportError as e:
        log_error(f"Failed to import surrealdb: {e}")
        return False

    try:
        # Step 1: Connect
        log_step(1, "Connecting to in-memory database (sync)...")
        with Surreal("mem://") as db:
            log_success("Connected to in-memory database")

            # Step 2: Set namespace and database
            log_step(2, "Setting namespace and database...")
            db.use("test_ns", "test_db")
            log_success("Set namespace='test_ns', database='test_db'")

            # Note: For embedded in-memory databases, no authentication is required

            # Step 3: Create records using SurrealQL
            log_step(3, "Creating product records with SurrealQL...")
            insert_result = db.query(
                """
                INSERT INTO product [
                    { name: 'Laptop', price: 999.99, stock: 50 },
                    { name: 'Phone', price: 699.99, stock: 100 },
                    { name: 'Tablet', price: 449.99, stock: 75 }
                ];
            """
            )
            log_success("Created 3 product records")
            log_data("Insert result", insert_result)

            # Step 4: Select all products
            log_step(4, "Selecting all products...")
            products = db.select("product")
            log_success(f"Retrieved {len(products)} products")
            for p in products:
                log_data(
                    "Product",
                    f"{p.get('name')}: ${p.get('price')} (stock: {p.get('stock')})",
                )

            # Step 5: Query with filter
            log_step(5, "Querying products over $500...")
            result = db.query("SELECT * FROM product WHERE price > 500")
            log_success("Query executed")
            log_data("Expensive products", result)

            # Step 6: Export schema
            log_step(6, "Exporting database schema...")
            schema_exported = export_schema_sync(db)
            if schema_exported:
                log_success("Schema export completed")
            else:
                log_error("Schema export failed")

            # Step 7: Cleanup
            log_step(6, "Deleting all product records...")
            db.delete("product")
            remaining = db.select("product")
            log_success(f"Cleanup complete. Remaining: {len(remaining)}")

        log_success("Connection closed (context manager)")

        logger.info("=" * 70)
        logger.info("✅ SYNC test completed successfully!")
        logger.info("=" * 70)
        return True

    except Exception as e:
        log_error(f"Sync test failed: {type(e).__name__}: {e}")
        import traceback

        logger.error(traceback.format_exc())
        return False


def main():
    """Run all tests."""
    logger.info("")
    logger.info("🔷" * 35)
    logger.info("   SurrealDB In-Memory Database Test")
    logger.info("   SDK: https://github.com/surrealdb/surrealdb.py")
    logger.info("🔷" * 35)
    logger.info("")

    results = {}

    # Run async test
    logger.info("Running async test...")
    results["async"] = asyncio.run(test_async_in_memory())

    # Run sync test
    logger.info("\nRunning sync test...")
    results["sync"] = test_sync_in_memory()

    # Summary
    logger.info("")
    logger.info("=" * 70)
    logger.info("📋 TEST SUMMARY")
    logger.info("=" * 70)

    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"   {test_name.upper()} test: {status}")
        if not passed:
            all_passed = False

    logger.info("=" * 70)
    if all_passed:
        logger.info("🎉 All tests passed!")
        return 0
    else:
        logger.error("💥 Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
